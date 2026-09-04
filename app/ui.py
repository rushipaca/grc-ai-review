# app/ui.py
import streamlit as st
from app.pipeline import review

st.title("GRC Software-Request Review")
st.caption("Reviewer tool: enter a software name and purpose to assemble the "
           "policy cross-check and trust-center findings. The reviewer decides.")

software = st.text_input("Software name", placeholder="e.g. Otter.ai")
purpose = st.text_area("Purpose / business use case", height=100,
                       placeholder="e.g. transcribe and summarize HR review meetings")

if st.button("Review request") and software and purpose:
    request_text = f"Software: {software}. Purpose: {purpose}."
    with st.spinner("Reviewing..."):
        out = review(request_text)
    s = out["summary"]

    # ---- Summary ----
    st.subheader("Summary")
    st.write(f"**Software:** {s['software_name'] or 'not stated'}")
    st.write(f"**Vendor:** {s['vendor'] or 'not stated'}")
    st.write(f"**Purpose:** {s['business_purpose'] or 'not stated'}")

    # ---- Assessment ----
    st.subheader("Assessment")

    st.markdown("**Internal Policy Cross-Check**")
    st.caption("What internal policy requires for this request, cited to control IDs.")
    if out["policy_findings"]:
        for finding in out["policy_findings"]:
            st.write("- " + finding)
    else:
        st.write("No applicable policy findings.")

    st.markdown("**Trust Center Review**")
    tc = out["trust_center"]
    status = tc.get("status", "unknown")
    if status == "none":
        st.write("Trust center: **Not found**")
        st.write("Action: request SOC 2 Type II and other relevant documents from the vendor.")
    elif status == "gated":
        st.write("Trust center: **Found** — access required (NDA/login).")
        st.write("Action: request access to view the vendor's reports.")
    elif status == "not checked":
        st.write("Not checked — request incomplete.")
    else:
        st.write("Trust center: **Found** — documents available.")
        available = [k for k, v in tc.items() if k != "status" and v]
        if available:
            st.write("Available: " + ", ".join(available))
        if out["missing_documents"]:
            st.write("**Still to gather:** " + ", ".join(out["missing_documents"]))

    if out["reviewer_notes"]:
        st.info(out["reviewer_notes"])

    # ---- Relevant Documents ----
    st.subheader("Relevant Documents")
    st.write("SOC 2 Type II and other relevant documents are gathered here for the reviewer.")