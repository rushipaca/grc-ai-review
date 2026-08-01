# Access Management Policy

- **Policy ID:** POL-AM
- **Owner:** IT
- **Version:** 2.0
- **Last reviewed:** 2026-02-01
- **Applies to:** Any tool authenticated with a Northwind identity or connected
  to a Northwind system.

This policy defines the access controls a tool must support based on the
classification of data it handles.

## AM-01 — Single sign-on (SSO)

- SSO via the company identity provider (SAML or OIDC) is **required** for any
  tool handling DC-03 Confidential or DC-04 Restricted data.
- A tool that cannot support SSO for Confidential or higher data is flagged for
  IT review and treated as missing a required control.

## AM-02 — Automated provisioning (SCIM)

- Tools handling DC-04 Restricted data should support automated user
  provisioning and deprovisioning (SCIM) so access is removed at offboarding.
- Absence of SCIM is a reviewer flag, not an automatic tier increase.

## AM-03 — Multi-factor authentication (MFA)

- MFA is required for all tools handling DC-03 or above. Where SSO is in place,
  the identity provider's MFA satisfies this control.

## AM-04 — Least privilege

- Access is granted by role. Tools must support role-based access so users
  receive only the access needed for their function.

## AM-05 — Offboarding

- Access must be removable within one business day of a user leaving or
  changing roles. Tools without SSO or SCIM require a documented manual
  offboarding process for DC-03 and above.
