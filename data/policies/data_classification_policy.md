# Data Classification Policy

- **Policy ID:** POL-DC
- **Owner:** Security & GRC
- **Version:** 2.1
- **Last reviewed:** 2026-03-01
- **Applies to:** All employees, contractors, and third-party software.

This policy defines how Northwind Industries classifies data. Every software
review must assign the highest classification of data the tool will store,
process, or transmit. Classification drives vendor documentation and access
requirements (see Vendor Risk Policy and Access Management Policy).

## DC-01 — Public

Information approved for public release. No harm results from disclosure.
Examples: marketing pages, published datasheets, public pricing, open-source
code. Tools handling only Public data are eligible for the Low risk tier.

## DC-02 — Internal

Non-sensitive business information intended for employees. Limited harm from
disclosure. Examples: internal wikis, org charts, general project notes,
non-sensitive meeting notes. Default classification when no higher category
applies.

## DC-03 — Confidential

Sensitive business information that would cause material harm if disclosed.
Examples: financial figures, budgets and forecasts, contracts, non-public
product roadmaps, supplier pricing, source code. Tools handling Confidential
data require a completed vendor security review (see Vendor Risk Policy).

## DC-04 — Restricted

The most sensitive data, including regulated personal data. Disclosure causes
severe harm and may trigger legal or regulatory obligations. Examples:
employee personal data (names tied to performance, compensation, health,
national ID), customer PII, authentication secrets, security findings. Tools
handling Restricted data require the full review path including Legal (see
Software Security Review Policy SSR-05).

## DC-05 — Assigning classification

- Assign the **highest** applicable tier across all data the tool touches.
- If the requester cannot state what data will be entered, classification is
  **undetermined** and the request cannot proceed (see SSR-04).
- Employee personal data is always DC-04 Restricted, even in small amounts.
- Free-text fields that could contain sensitive data are classified at the
  highest tier that text could plausibly hold.
