# evals/run_eval.py
import json
from app.pipeline import review

cases = json.load(open("evals/gold.json", encoding="utf-8-sig"))

correct = 0
print(f"Running {len(cases)} eval cases...\n")

for c in cases:
    request = f"Software: {c['software']}. Purpose: {c['purpose']}."
    result = review(request)
    actual = result["assessment"]["risk_level"]
    expected = c["expected_risk"]
    ok = actual == expected
    correct += ok
    mark = "PASS" if ok else "FAIL"
    print(f"[{mark}] {c['software']}: expected {expected}, got {actual}")

pct = round(100 * correct / len(cases))
print(f"\nRisk-level accuracy: {correct}/{len(cases)} ({pct}%)")