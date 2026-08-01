# Vendor Risk Policy

- **Policy ID:** POL-VR
- **Owner:** Security & GRC
- **Version:** 2.4
- **Last reviewed:** 2026-01-20
- **Applies to:** All third-party SaaS vendors and software suppliers.

This policy defines the documentation a vendor must provide based on the
classification of data the tool will handle (see Data Classification Policy).

## VR-01 — SOC 2 requirement

- A current SOC 2 Type II report is **required** for any vendor handling
  DC-03 Confidential or DC-04 Restricted data.
- Vendors handling only DC-01 Public or DC-02 Internal data do not require a
  SOC 2 report.
- If SOC 2 is required and not available, the request is **High** risk and
  routed to Security review with a missing-document flag.

## VR-02 — Data Processing Agreement (DPA)

- A signed DPA is **required** for any vendor that processes DC-04 Restricted
  personal data (employee or customer PII).
- If a DPA is required but not in place, Legal review is mandatory (SSR-05).

## VR-03 — Subprocessor list

- Vendors handling DC-04 Restricted data must provide a current subprocessor
  list identifying any downstream providers with access to the data.
- A missing subprocessor list for Restricted data triggers Legal review.

## VR-04 — Data retention and deletion

- Vendors must document data retention periods and a deletion process on
  contract termination for DC-03 and above.
- Absence of a documented deletion process is a missing-document flag for the
  reviewer but does not by itself raise the risk tier.

## VR-05 — Required vendor documents by tier

- **DC-01 / DC-02:** No vendor documentation required.
- **DC-03 Confidential:** SOC 2 Type II.
- **DC-04 Restricted:** SOC 2 Type II, signed DPA, subprocessor list, and a
  documented retention/deletion process.

Any required document that is missing is listed in the review packet under
"Missing documentation."
