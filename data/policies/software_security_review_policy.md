# Software Security Review Policy

- **Policy ID:** POL-SSR
- **Owner:** Security & GRC
- **Version:** 3.0
- **Last reviewed:** 2026-02-15
- **Applies to:** Any request to adopt, purchase, or use new software or a new
  SaaS vendor.

This policy defines when a review is required, how risk is tiered, what intake
information is mandatory, and which teams must review each tier.

## SSR-01 — When a review is required

A review is required before any of the following:
- Signing up for a new SaaS product or browser extension used for work.
- Entering any DC-02 or higher data into a tool not already approved.
- Connecting a tool to a Northwind system (SSO, calendar, email, storage, APIs).
- Using a tool that applies AI to Northwind data (see AI Usage Policy).

Personal use of public tools with no Northwind data does not require review.

## SSR-02 — Risk tiers

- **Low:** Handles only DC-01 Public data. No login with Northwind identity,
  no integrations, no AI processing of Northwind data.
- **Medium:** Handles up to DC-03 Confidential data, has required vendor
  documentation on file, and supports required access controls.
- **High:** Handles DC-04 Restricted data, applies AI to employee or customer
  data, or is missing required vendor documentation for its data tier.
- **Not Enough Information:** The requester has not provided the fields required
  in SSR-04. The request cannot be tiered until these are supplied.

## SSR-03 — Required reviews by tier

- **Low:** Reviewer confirmation only. No additional teams.
- **Medium:** Security review and IT review.
- **High:** Security review, IT review, and Legal review (SSR-05).
- **Not Enough Information:** No review proceeds; the assistant requests the
  missing fields.

## SSR-04 — Mandatory intake fields

A request cannot be tiered unless all of the following are provided:
1. Software name and vendor.
2. Business purpose.
3. Data types the tool will handle (used to assign classification, DC-05).
4. Whether the tool applies AI to Northwind data.
5. System integrations requested (SSO, email, calendar, storage, APIs).
6. Vendor documentation available (see Vendor Risk Policy VR-01).

If any of fields 1-5 are missing, the request is **Not Enough Information**.

## SSR-05 — When Legal review is required

Legal review is mandatory when any of the following is true:
- The tool handles DC-04 Restricted data.
- The tool applies AI to employee or customer personal data (AIU-03).
- A Data Processing Agreement is required but not yet in place (VR-02).
- The vendor's subprocessor list is unavailable for Restricted data (VR-03).

## SSR-06 — Reviewer authority

The assistant produces a recommendation and a review packet. It never approves
or rejects software. Final approval rests with the human reviewer.
