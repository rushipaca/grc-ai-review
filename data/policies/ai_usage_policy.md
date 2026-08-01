# AI Usage Policy

- **Policy ID:** POL-AIU
- **Owner:** Security & GRC (with Legal)
- **Version:** 1.3
- **Last reviewed:** 2026-03-10
- **Applies to:** Any tool that uses AI or machine learning to process
  Northwind data.

This policy sets additional controls for AI-enabled tools, on top of the
Software Security Review and Vendor Risk policies.

## AIU-01 — Approved use

AI tools may be used to draft, summarize, and assist with work, provided the
data entered is classified and permitted for that tool's approved tier. A tool
approved for DC-02 Internal data must not receive DC-03 or DC-04 data.

## AIU-02 — Prohibited data in unapproved AI tools

Do not enter DC-03 Confidential or DC-04 Restricted data into any AI tool that
has not completed review for that tier. This includes pasting source code,
financials, contracts, or any employee or customer personal data into public
AI chatbots.

## AIU-03 — AI applied to personal data

Any tool that applies AI to employee or customer personal data (DC-04
Restricted) is **High** risk and requires Security, IT, and Legal review. This
includes AI note-takers, performance-summary tools, and any tool ingesting
free-text that may contain employee names tied to feedback, compensation, or
health.

## AIU-04 — Model training and data-use disclosure

Vendors must disclose whether Northwind data is used to train or improve their
models. For DC-03 and above, training on Northwind data must be contractually
disabled. If the training-use disclosure is unavailable, the request is flagged
as missing documentation and cannot be approved for Confidential or Restricted
data.

## AIU-05 — Human in the loop

AI tools must not make final employment, financial, or compliance decisions.
Output is a recommendation for a human. Any tool that would auto-approve,
auto-reject, or auto-action without human review is prohibited.
