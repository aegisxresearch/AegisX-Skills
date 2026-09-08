# STRIDE Threat Modeling

## Goal
Find high-impact abuse paths before implementation and keep mitigations tied to verifiable requirements.

## Workflow
```text
Scope → assets → actors → data flows → trust boundaries → STRIDE threats → risk → mitigations → verification
```
Start with the smallest diagram that captures users, services, data stores, external providers, and boundaries where trust changes.

## STRIDE Categories
| Category | Question | Typical control |
|---|---|---|
| Spoofing | Can an actor impersonate another? | MFA, secure sessions, key rotation |
| Tampering | Can data/code be modified? | Integrity checks, authorization, signed artifacts |
| Repudiation | Can actions be denied? | Audit logs, time sync, request IDs |
| Information disclosure | Can sensitive data leak? | Least privilege, encryption, redaction |
| Denial of service | Can availability be exhausted? | Quotas, rate limits, isolation, autoscaling |
| Elevation of privilege | Can permissions be escalated? | RBAC, object authorization, separation of duties |

## Risk Record
```yaml
id: THREAT-004
asset: customer-export
actor: authenticated-user
boundary: api-to-object-storage
threat: information-disclosure
impact: high
likelihood: medium
mitigation: signed-download-url-with-short-expiry
verification: authorization-integration-test
owner: platform-security
status: open
```
Use a consistent risk method and prioritize exploitable paths affecting sensitive assets or many users.

## Abuse Cases
For each critical flow, document unauthorized access, replay, tampering, resource exhaustion, malicious input, dependency compromise, and failure-mode abuse. Include tenant isolation and administrative misuse where relevant.

## Design Controls
Prefer controls at the architecture boundary: explicit authorization, parameterized queries, validation, rate limiting, network segmentation, secure defaults, auditability, and safe failure. Do not rely on an undocumented operator habit.

## Verification
Map every high-risk threat to a test, policy, scanner, monitoring signal, or review. Revisit the model when authentication, data classification, external integrations, deployment topology, or major dependencies change.

## Checklist
- [ ] Assets and data classifications are named.
- [ ] External actors and trust boundaries are visible.
- [ ] All STRIDE categories are considered.
- [ ] Tenant/object authorization is explicit.
- [ ] High-risk threats have owners and verification.
- [ ] Abuse cases include replay and resource exhaustion.
- [ ] Security logging avoids sensitive payloads.
- [ ] Threat model is reviewed with architecture changes.

## References
- https://learn.microsoft.com/en-us/azure/security/develop/threat-modeling-tool-threats
- https://owasp.org/www-community/Threat_Modeling
- https://csrc.nist.gov/publications/detail/sp/800-154/final

---

*Dokumentasi ini bagian dari [AegisX Skills Collection](https://aegisxresearch.github.io/AegisX-Skills/). Dikelola oleh AegisX Research.*
