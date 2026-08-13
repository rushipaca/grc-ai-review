# app/pipeline.py
import os
from typing import Optional
from pydantic import BaseModel
from google import genai
from dotenv import load_dotenv
from typing import Literal
from app.rag import search_policy
from app.trust import check_trust_center
import json

load_dotenv()
client = genai.Client(api_key=os.environ["GEMINI_API_KEY"])
MODEL = "gemini-3.6-flash"

# The "form" the model must fill in from the request
class RequestFields(BaseModel):
    software_name: Optional[str]    
    vendor: Optional[str]
    business_purpose: Optional[str]
    data_types: list[str]
    uses_ai: Optional[bool]
    integrations: list[str]
    vendor_docs_provided: list[str]

def extract(text: str) -> RequestFields:
    """Read a plain-English software request and return structured fields."""
    r = client.models.generate_content(
        model=MODEL,
        contents=text,
        config={
            "system_instruction": (
                "Extract the fields from this software request. "
                "Use null or an empty list when a field is not stated. Never guess."
            ),
            "response_mime_type": "application/json",
            "response_schema": RequestFields,
        },
    )
    return r.parsed

# The two-bucket "missing" logic — intake fields only
REQUIRED = ["software_name", "vendor", "business_purpose",
            "data_types", "uses_ai", "integrations"]

def still_needed(f: RequestFields) -> list:
    """Return the list of required intake fields the requester hasn't provided."""
    missing = []
    for name in REQUIRED:
        value = getattr(f, name)
        if value is None or value == []:
            missing.append(name)
    return missing

class Assessment(BaseModel):
    reasons: list[str]            # each reason should cite a control id like [VR-02]
    missing_documents: list[str]  # vendor docs required but not provided
    risk_level: Literal["Low", "Medium", "High", "Not Enough Information"]
    recommended_next_action: str

SYS = ("You are a GRC assistant. Decide the risk level ONLY from the provided policy "
       "controls and trust-center findings. Cite control IDs in brackets in each reason, "
       "e.g. [VR-02]. List any required vendor documents that are missing. Never invent "
       "controls or reports.")

def classify(f: RequestFields, policy_hits: list, trust: dict) -> Assessment:
    context = "POLICY CONTROLS:\n" + "\n".join(
        f"[{h['control_id']}] {h['text']}" for h in policy_hits)
    context += f"\n\nTRUST CENTER for {f.vendor}: {trust}"
    context += f"\n\nREQUEST FIELDS: {f.model_dump()}"
    r = client.models.generate_content(
        model=MODEL,
        contents=context,
        config={
            "system_instruction": SYS,
            "response_mime_type": "application/json",
            "response_schema": Assessment,
        },
    )
    return r.parsed

def review(text: str) -> dict:
    # Step 1: read the request into fields
    f = extract(text)

    # Step 2: check what's missing from the requester
    gaps = still_needed(f)

    # Step 3: if intake is incomplete, stop here -> Not Enough Information
    if gaps:
        assessment = Assessment(
            reasons=["Required intake information is missing."],
            missing_documents=[],
            risk_level="Not Enough Information",
            recommended_next_action="Ask the requester for: " + ", ".join(gaps),
        )
        hits, trust = [], {"status": "not checked"}
    else:
        # Step 4: search policy + check the vendor, then classify
        hits = search_policy(f"{f.business_purpose} {f.data_types}", k=6)
        trust = check_trust_center(f.vendor)
        assessment = classify(f, hits, trust)

    # Step 5: build the mock ticket
    ticket = {
        "id": "SR-AUTO",
        "status": "In Review",
        "risk_level": assessment.risk_level,
        "software": f.software_name,
        "vendor": f.vendor,
        "missing_documents": assessment.missing_documents,
        "next_action": assessment.recommended_next_action,
    }
    json.dump(ticket, open("store/last_ticket.json", "w"), indent=2)

    # Step 6: return the full five-part packet
    return {
        "summary": f.model_dump(),
        "still_needed": gaps,
        "trust_center": trust,
        "policy_citations": [h["control_id"] for h in hits],
        "assessment": assessment.model_dump(),
        "ticket": ticket,
    }