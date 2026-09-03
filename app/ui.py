# app/ui.py
import streamlit as st
from app.pipeline import review

st.title("GRC Software-Request Review")
st.caption("Reviewer tool: enter the software and its purpose to assemble a "
           "first-pass compliance assessment. Decision support — the reviewer "
           "makes the final call.")

software = st.text_input("Software name", placeholder="e.g. Acme AI Notetaker")
purpose = st.text_area("Purpose / business use case", height=100,
                       placeholder="e.g. so HR can summarize performance review meetings")

if st.button("Review request") and software and purpose:
    request_text = f"Software: {software}. Purpose: {purpose}."
    with st.spinner("Reviewing..."):
        out = review(request_text)
    a = out["assessment"]
    s = out["summary"]

    # ---- Summary ----
    st.subheader("Summary")
    st.write(f"**Software:** {s['software_name'] or 'not stated'}")
    st.write(f"**Vendor:** {s['vendor'] or 'not stated'}")
    st.write(f"**Purpose:** {s['business_purpose'] or 'not stated'}")

    # ---- Assessment ----
    st.subheader("Assessment")

    st.markdown("**Internal Policy Cross-Check**")
    st.caption("Comparison against internal policy; deviations cited to a control ID.")
    if a["reasons"]:
        for reason in a["reasons"]:
            st.write("- " + reason)
    else:
        st.write("No policy deviations identified.")
    st.info(f"Suggested risk level: {a['risk_level']}  (reviewer confirms)")

    st.markdown("**Trust Center Review**")
    tc = out["trust_center"]
    status = tc.get("status", "unknown")

    if status == "none":
        st.write("Trust center: **Not found**")
        st.write("Action: request SOC 2 Type II and other relevant documents "
                 "directly from the vendor.")
    elif status == "gated":
        st.write("Trust center: **Found**")
        st.write("Access: **Required** (NDA/login)")
        st.write("Action: request access to view the vendor's reports.")
    else:  # public / has reports
        st.write("Trust center: **Found**")
        st.write("Access: **Not required** — documents are downloadable.")
        available = [k for k, v in tc.items() if k != "status" and v]
        if available:
            st.write("Documents available: " + ", ".join(available))
        if a["missing_documents"]:
            st.write("**Still to gather:** " + ", ".join(a["missing_documents"]))

    # ---- Relevant Documents ----
    st.subheader("Relevant Documents")
    st.write("SOC 2 Type II and other relevant documents are gathered here for "
             "the reviewer.")