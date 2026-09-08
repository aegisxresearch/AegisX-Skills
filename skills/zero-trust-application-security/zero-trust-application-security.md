# Zero Trust Application Security

## Goal
Do not trust a network location, service name, or prior authentication by default. Verify identity, authorization, context, and resource access for every sensitive operation.

## Principles
1. Verify explicitly.
2. Use least privilege.
3. Assume breach.
4. Minimize blast radius.
5. Log and evaluate access continuously.

## Request Decision
```text
principal identity + workload identity + resource + action + tenant + context
        ↓
policy evaluation → allow / deny / step-up / audit
```
Authorization must be enforced server-side at the object and action level. A valid session does not imply access to every resource.

## Service Identity
Use short-lived, cryptographically verifiable workload identities and mutual TLS or signed tokens where appropriate. Validate issuer, audience, expiry, key ID, and revocation/rotation policy. Avoid shared static credentials between services.

## Segmentation
Restrict network paths, egress, data-store roles, namespaces, and administrative access. Network controls reduce blast radius but do not replace application authorization.

## Session and Context
Re-evaluate sensitive actions based on user, tenant, device/session risk, recent authentication, transaction amount, and resource sensitivity. Use step-up authentication where risk warrants it.

## Assume-Breach Controls
Design for compromised credentials or services: minimize permissions, isolate tenants, rate-limit, detect unusual access, encrypt data, maintain audit trails, and have revocation and recovery procedures.

## Checklist
- [ ] User and workload identities are explicit.
- [ ] Authorization checks resource and action, not only route.
- [ ] Tokens validate issuer, audience, expiry, and rotation.
- [ ] Service credentials are short-lived where possible.
- [ ] Network segmentation limits blast radius.
- [ ] Sensitive actions support step-up verification.
- [ ] Access decisions are auditable without sensitive payloads.
- [ ] Detection and revocation runbooks are tested.
- [ ] Tenant isolation is tested with negative cases.

## References
- https://www.nist.gov/publications/zero-trust-architecture
- https://csrc.nist.gov/pubs/sp/800/207/final
- https://owasp.org/www-project-top-ten/

---

*Dokumentasi ini bagian dari [AegisX Skills Collection](https://aegisxresearch.github.io/AegisX-Skills/). Dikelola oleh AegisX Research.*
