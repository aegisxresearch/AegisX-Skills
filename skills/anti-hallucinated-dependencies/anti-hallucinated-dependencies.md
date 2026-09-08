# Anti-Hallucinated Dependencies

## Goal
Never introduce an unverified dependency or API based on model memory alone.

## Discovery Protocol
```text
Inspect manifests → inspect lockfile → search existing imports → inspect installed package/docs → verify version API → implement minimal change
```
Check `package.json`, `pyproject.toml`, lockfiles, build files, and existing usage before adding a package. Follow the repository's package manager; do not substitute npm, yarn, pnpm, bun, pip, or another tool without evidence.

## Verification Requirements
Before using a library, confirm:
- package name and import path;
- installed or approved version;
- exported symbol and function signature;
- runtime/environment compatibility;
- license and security posture;
- whether existing project code already solves the problem.

If a fact cannot be verified, state the uncertainty and use a standard-library or existing-project solution when reasonable.

## Dependency Decision Record
```markdown
Package: example-library
Need: signed URL generation
Existing alternative checked: yes/no
Version/API verified: yes/no
Security/license reviewed: yes/no
Reason new dependency is necessary: ...
```

## Common Hallucinations
- Importing a symbol that belongs to a different package.
- Mixing APIs from incompatible major versions.
- Assuming framework configuration exists without checking.
- Adding a package solely to perform a few lines of simple logic.
- Copying a command that silently uses a different package manager.

## Safe Failure
Do not replace an uncertain API with invented code that looks plausible. Pause, inspect local evidence, or implement behind a narrow adapter with explicit assumptions and tests.

## Checklist
- [ ] Existing manifests and imports were inspected.
- [ ] Package manager and lockfile are respected.
- [ ] Package, version, export, and runtime API are verified.
- [ ] New dependency is necessary and justified.
- [ ] License and vulnerability policy are satisfied.
- [ ] No package or API is invented from memory.
- [ ] Build and tests use the actual installed dependency.
- [ ] Uncertainty is reported instead of hidden.
