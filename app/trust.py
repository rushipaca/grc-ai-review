# app/trust.py
import json

# Load the seeded vendor data once, when the file is imported
TRUST_CENTER = json.load(open("data/trust_center.json"))

def check_trust_center(vendor: str) -> dict:
    """Return what security reports a vendor lists. 'none' if we have no record."""
    return TRUST_CENTER.get(vendor, {"status": "none"})