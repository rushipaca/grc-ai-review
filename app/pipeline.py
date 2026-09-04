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
import time
from google.genai import errors as genai_errors

load_dotenv()
client = genai.Client(api_key=os.environ["GEMINI_API_KEY"])
MODEL = "gemini-flash-lite-latest"

def _generate_with_retry(**kwargs):
    """Call Gemini, retrying on transient 429/503 with backoff."""
    for attempt in range(4):
        try:
            return client.models.generate_content(**kwargs)
        except genai_errors.APIError as e:
            code = getattr(e, "code", None)
            if code in (429, 503) and attempt < 3:
                time.sleep(2 ** attempt * 5)   # 5s, 10s, 20s
                continue
            raise

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
    r = _generate_with_retry(
        model=MODEL,
        contents=text,
        config={
                "system_instruction": (
                "You are a GRC analyst building a software request profile from the "
                "software name and purpose. Infer these fields from your knowledge of "
                "the software and how it is used for the stated purpose:\n"
                "- vendor: the company that makes the software.\n"
                "- data_types: the kinds of data this software would realistically "
                "process for this purpose. ALWAYS infer this. Example: an HR notetaker "
                "summarizing performance reviews processes ['employee personal data', "
                "'performance review content']; a color picker processes [].\n"
                "- uses_ai: true if the software applies AI/ML to data, else false.\n"
                "- integrations: likely integrations (e.g. SSO) if implied, else [].\n"
                "Base every inference on the software and purpose. Only leave a field "
                "empty if it genuinely cannot be inferred."
            ),
            "response_mime_type": "application/json",
            "response_schema": RequestFields,
        },
    )
    return r.parsed

# The two-bucket "missing" logic — intake fields only
REQUIRED = ["software_name", "business_purpose",]

def still_needed(f: RequestFields) -> list:
    """Return the list of required intake fields the requester hasn't provided."""
    missing = []
    for name in REQUIRED:
        value = getattr(f, name)
        if value is None or value == []:
            missing.append(name)
    return missing

class CrossCheck(BaseModel):
    policy_findings: list[str]     # applicable controls + what each requires (cited)
    flags: list[str]               # concrete conditions where the request may NOT meet a cited requirement
    missing_documents: list[str]   # required vendor documents not shown as provided
    reviewer_notes: str            # neutral one-line summary of what to verify (NOT a verdict)

SYS = ("You are a GRC analyst assembling information for a human reviewer. Using ONLY "
       "the provided policy controls and trust-center findings:\n"
       "- policy_findings: state which controls apply and what each requires, citing "
       "the control ID in brackets, e.g. '[DC-04] Restricted data requires a SOC 2 "
       "Type II and a DPA.'\n"
       "- flags: list concrete conditions where the request may NOT meet a cited "
       "requirement, or where a policy-defined risk condition is present. Each flag "
       "must cite the control(s) it relates to and state the specific gap, e.g. "
       "'[AIU-03] AI is applied to employee personal data, which triggers a mandatory "
       "Legal review that is not yet recorded' or '[VR-02] A DPA is required but the "
       "vendor's trust center does not list one.' If nothing is out of line, return an "
       "empty list.\n"
       "- missing_documents: required vendor documents the trust center does not show "
       "as provided.\n"
       "- reviewer_notes: one neutral sentence on what the reviewer should verify.\n"
       "Do NOT assign a risk level and do NOT approve or reject. Flag conditions and "
       "cite policy; the human decides. Never invent controls or reports.")

def cross_check(f: RequestFields, policy_hits: list, trust: dict) -> CrossCheck:
    context = "POLICY CONTROLS:\n" + "\n".join(
        f"[{h['control_id']}] {h['text']}" for h in policy_hits)
    context += f"\n\nTRUST CENTER for {f.vendor}: {trust}"
    context += f"\n\nREQUEST FIELDS: {f.model_dump()}"
    r = _generate_with_retry(
        model=MODEL,
        contents=context,
        config={
            "system_instruction": SYS,
            "response_mime_type": "application/json",
            "response_schema": CrossCheck,
        },
    )
    return r.parsed

def review(text: str) -> dict:
    f = extract(text)
    gaps = still_needed(f)

    if gaps:
        cc = CrossCheck(
            policy_findings=[],
            flags=[],
            missing_documents=[],
            reviewer_notes="Request incomplete — provide a software name and purpose.",
        )
        hits, trust = [], {"status": "not checked"}
    else:
        hits = search_policy(f"{f.business_purpose} {f.data_types}", k=6)
        trust = check_trust_center(f.vendor)
        cc = cross_check(f, hits, trust)

    ticket = {
        "id": "SR-AUTO",
        "status": "In Review",
        "software": f.software_name,
        "vendor": f.vendor,
        "flags": cc.flags,
        "missing_documents": cc.missing_documents,
        "notes": cc.reviewer_notes,
    }
    json.dump(ticket, open("store/last_ticket.json", "w"), indent=2)

    return {
        "summary": f.model_dump(),
        "still_needed": gaps,
        "trust_center": trust,
        "policy_citations": [h["control_id"] for h in hits],
        "policy_findings": cc.policy_findings,
        "flags": cc.flags,
        "missing_documents": cc.missing_documents,
        "reviewer_notes": cc.reviewer_notes,
        "ticket": ticket,
    }