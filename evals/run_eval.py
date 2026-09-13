# evals/run_eval.py
import json, time
from app.pipeline import review

cases = json.load(open("evals/gold.json", encoding="utf-8-sig"))

total_recall = 0.0
total_precision = 0.0
print(f"Running {len(cases)} citation eval cases...\n")

for c in cases:
    request = f"Software: {c['software']}. Purpose: {c['purpose']}."
    result = review(request)
    actual = set(result["policy_citations"])
    expected = set(c["expected_controls"])

    hits = actual & expected
    recall = len(hits) / len(expected) if expected else 1.0
    precision = len(hits) / len(actual) if actual else 0.0
    total_recall += recall
    total_precision += precision

    missed = expected - actual
    print(f"{c['software']}:")
    print(f"  expected: {sorted(expected)}")
    print(f"  surfaced: {sorted(actual)}")
    print(f"  recall {recall:.0%}  precision {precision:.0%}"
          + (f"   MISSED {sorted(missed)}" if missed else ""))
    print()
    time.sleep(4)   # spacing to respect free-tier rate limits

n = len(cases)
print(f"Average recall:    {total_recall/n:.0%}   (did we surface the right controls?)")
print(f"Average precision: {total_precision/n:.0%}   (how much of what we surfaced was relevant?)")