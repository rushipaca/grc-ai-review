# app/pipeline.py
import os
from typing import Optional
from pydantic import BaseModel
from google import genai
from dotenv import load_dotenv

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