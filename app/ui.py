# app/ui.py
import streamlit as st
from app.pipeline import review

st.title("GRC Software-Request Review")
st.caption("Paste a software request. The assistant checks it against policy and drafts an assessment.")

text = st.text_area("Software request", height=150,
                    placeholder="e.g. We want to use Acme AI Notetaker for HR to summarize reviews...")

if st.button("Review request") and text:
    with st.spinner("Reviewing..."):
        out = review(text)
    a = out["assessment"]

    # Headline risk level
    st.header(f"Risk: {a['risk_level']}")

    # 1. Request summary
    st.subheader("1. Request summary")
    s = out["summary"]
    st.write(f"**Software:** {s['software_name']}  |  **Vendor:** {s['vendor']}")
    st.write(f"**Purpose:** {s['business_purpose']}")
    st.write(f"**Data types:** {', '.join(s['data_types']) or 'none stated'}")
    st.write(f"**Uses AI:** {s['uses_ai']}  |  **Integrations:** {', '.join(s['integrations']) or 'none'}")
    if out["still_needed"]:
        st.warning("Still needed from requester: " + ", ".join(out["still_needed"]))

    # 2. Trust center
    st.subheader("2. Trust center findings")
    st.json(out["trust_center"])

    # 3. Policy check
    st.subheader("3. Policy check")
    for reason in a["reasons"]:
        st.write("- " + reason)
    st.caption("Controls retrieved: " + ", ".join(out["policy_citations"]))

    # 4. Assessment
    st.subheader("4. Assessment")
    st.write(f"**Risk level:** {a['risk_level']}")
    st.write("**Missing documents:** " + (", ".join(a["missing_documents"]) or "none"))
    st.write(f"**Recommended next action:** {a['recommended_next_action']}")

    # 5. Mock ticket
    st.subheader("5. Mock ticket")
    st.json(out["ticket"])