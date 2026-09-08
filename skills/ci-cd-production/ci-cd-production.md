# Production CI/CD Engineering

## Goal
Make every release traceable, repeatable, secure, and reversible.

## Pipeline Stages
```text
validate → lint/typecheck → unit/integration → security scan → build artifact → deploy staging → smoke test → approval → production → verify
```
Keep build and test inputs pinned. Produce one immutable artifact and promote the same artifact across environments; do not rebuild differently for production.

## Supply Chain
Use lockfiles, trusted base images, dependency scanning, SBOM generation, provenance, and signed artifacts where supported. Pin actions and reusable pipeline dependencies by immutable reference.

## Secrets
Inject secrets at runtime through the platform secret store. Mask logs, restrict environments, rotate credentials, and never place secrets in repository variables that every workflow can read. Pull requests from untrusted forks must not receive deployment credentials.

## Deployment Strategies
- **Rolling:** simple, but mixed versions must be compatible.
- **Blue/green:** quick switch and rollback, higher capacity cost.
- **Canary:** limits blast radius and needs representative traffic metrics.
- **Feature flags:** decouple code deployment from user exposure.

Choose based on database compatibility, session behavior, migration safety, and rollback requirements.

## Database Changes
Use expand-and-contract migrations: add compatible schema, deploy code that supports both forms, backfill safely, switch reads/writes, then remove old schema in a later release.

## Verification
Smoke tests should verify health, authentication boundary, critical reads/writes, queue publication, and dependency behavior without destructive production data. Monitor error rate, latency, saturation, and business metrics after deployment.

## Rollback
Define whether rollback means artifact rollback, feature disablement, traffic switch, or forward migration. Test rollback and ensure schema changes remain backward compatible.

## Checklist
- [ ] Same immutable artifact is promoted across environments.
- [ ] Tests and security scans run before deployment.
- [ ] SBOM/provenance policy is defined.
- [ ] Secrets are runtime-injected and least-privileged.
- [ ] Untrusted workflow contexts cannot access deploy credentials.
- [ ] Migrations are backward compatible.
- [ ] Smoke checks and post-deploy monitoring exist.
- [ ] Rollback is documented and tested.
- [ ] Pipeline logs and artifacts have retention/access policies.

## References
- https://slsa.dev/spec/v1.0/
- https://docs.github.com/en/actions/security-guides/security-hardening-for-github-actions
- https://martinfowler.com/bliki/BlueGreenDeployment.html

---

*Dokumentasi ini bagian dari [AegisX Skills Collection](https://aegisxresearch.github.io/AegisX-Skills/). Dikelola oleh AegisX Research.*
