# Software Supply-Chain Security

## Goal
Make software provenance visible and make unauthorized dependency, build, and release changes difficult to introduce or distribute.

## Dependency Controls
- Use lockfiles and review dependency updates.
- Pin actions, plugins, base images, and package sources.
- Restrict registries and configure trusted publishers where supported.
- Scan direct and transitive dependencies, but triage by exploitability and reachability.
- Maintain an exception owner, reason, expiry, and compensating control.

## Build Provenance
Generate an SBOM for release artifacts and record source revision, builder identity, dependencies, configuration, and timestamp. Prefer isolated, ephemeral builders and minimal permissions.

```text
source revision → isolated build → tests/scans → signed artifact + SBOM + provenance → verified deployment
```

## Signing and Verification
Sign container images, packages, and release metadata with protected keys or keyless workload identity. Deployment systems should verify expected issuer, repository, artifact digest, and provenance policy before running artifacts.

## CI/CD Threats
Protect against pull request secret exposure, compromised runners, untrusted build scripts, dependency confusion, artifact substitution, mutable tags, and overly broad deployment tokens. Separate build, publish, and deploy permissions.

## Reproducibility
Pin toolchains, use deterministic inputs, record environment metadata, and compare outputs where practical. Reproducibility is a control for investigation and confidence, not a guarantee that all builds are identical.

## Vulnerability Response
Classify severity, exploitability, exposure, and available mitigation. Patch reachable critical issues quickly, rotate compromised credentials, rebuild from trusted inputs, and verify deployed digests rather than assuming a tag moved safely.

## Checklist
- [ ] Dependencies, actions, tools, and base images are pinned.
- [ ] Lockfiles and dependency changes receive review.
- [ ] SBOM and provenance are produced for releases.
- [ ] Artifacts are signed and deployment verifies them.
- [ ] Build and deploy credentials have separate least-privilege scopes.
- [ ] CI runners and pull request trust boundaries are documented.
- [ ] Vulnerability exceptions expire and have owners.
- [ ] Incident response includes rebuild and credential rotation.
- [ ] Deployed artifact digests are auditable.

## Kesalahan Umum / Pitfalls

- No SBOM — you cannot know what is in your software.
- No dependency pinning — builds break or get hijacked.
- No signature verification — tampered artifacts.
- Ignoring known CVEs in transitive dependencies.

## Trade-off dan Kapan Tidak Pakai

- SBOMs add process overhead — start with critical services.
- Pinning everything prevents drift but blocks updates — balance.
- Signature verification is important but adds key management.

## References
- https://slsa.dev/spec/v1.0/
- https://www.cisa.gov/topics/cyber-threats-and-advisories/software-supply-chain-security
- https://cyclonedx.org/

---

*Dokumentasi ini bagian dari [AegisX Skills Collection](https://aegisxresearch.github.io/AegisX-Skills/). Dikelola oleh AegisX Research.*
