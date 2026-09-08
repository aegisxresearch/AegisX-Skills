# Secrets Management Engineering

## Goal
Ensure credentials are discoverable, short-lived where possible, least-privileged, rotatable, and absent from source and logs.

## Classify Secrets
Examples include database credentials, signing keys, API tokens, encryption keys, certificates, and personal data. Assign owner, environment, scope, expiry, rotation method, and incident contact.

## Storage and Injection
Use a dedicated secret manager or cloud KMS-backed store. Applications should retrieve secrets at runtime through workload identity or a tightly scoped bootstrap credential. Do not bake secrets into images, source maps, client bundles, or `Terraform` state unnecessarily.

```text
workload identity → secret manager → short-lived credential → application memory
```

## Access Control
Grant access by workload identity, environment, and secret path. Separate read, rotate, and administer permissions. Audit reads and alert on unusual access. Do not copy production secrets into development.

## Rotation
Support overlapping credentials: create new, deploy consumers, verify usage, revoke old. Rotation must be tested and should not require simultaneous downtime. Prefer dynamic database credentials, workload identity, and short-lived tokens.

## Leak Prevention
Use pre-commit and CI secret scanners, repository push protection, log redaction, restricted debugging, and dependency/source-map review. Scanner findings require validation and revocation when exposure is plausible.

## Incident Response
1. Revoke or disable the exposed credential.
2. Preserve evidence without redistributing the secret.
3. Identify access and affected resources.
4. Rotate dependent credentials and invalidate sessions/tokens.
5. Remove the secret from reachable history/artifacts where appropriate.
6. Document cause and prevention.

## Checklist
- [ ] Every secret has owner, scope, expiry, and rotation path.
- [ ] Production secrets use managed storage and workload identity.
- [ ] Access is least-privileged and audited.
- [ ] Secrets are never logged or shipped to clients.
- [ ] Rotation supports overlap and has been tested.
- [ ] CI and repository scanning are enabled.
- [ ] Leak response includes revocation and impact analysis.
- [ ] Development uses separate credentials and safe fixtures.

## Kesalahan Umum / Pitfalls

- Secrets in code or config files committed to git.
- No rotation — a leaked secret is valid forever.
- Broad access to the vault — least privilege forgotten.
- No audit log — you cannot know who accessed what.

## Trade-off dan Kapan Tidak Pakai

- Vault adds operational complexity — start with environment variables for small apps.
- Rotation is disruptive — balance frequency with risk.
- Centralized vaults are a single point of failure — plan for availability.

## References
- https://owasp.org/www-project-application-security-verification-standard/
- https://csrc.nist.gov/publications/detail/sp/800-57-part-1/rev-5/final
- https://slsa.dev/spec/v1.0/threats

---

*Dokumentasi ini bagian dari [AegisX Skills Collection](https://aegisxresearch.github.io/AegisX-Skills/). Dikelola oleh AegisX Research.*
