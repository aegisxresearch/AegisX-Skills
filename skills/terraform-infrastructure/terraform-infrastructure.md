# `Terraform` Infrastructure Engineering

## Goal
Manage infrastructure changes as reviewed, reproducible plans without exposing secrets or losing state.

## State
Use a remote backend with encryption, locking, versioning, and restricted access. Treat state as sensitive because it may contain resource attributes. Never commit state files or plan files containing secrets.

## Module Design
Create modules around stable capabilities and ownership, not every resource. Keep interfaces small, validate variables, pin provider versions, and document outputs and replacement behavior.

```hcl
variable "environment" {
  type        = string
  description = "Deployment environment"
  validation {
    condition     = contains(["staging", "production"], var.environment)
    error_message = "Environment must be staging or production."
  }
}
```

## Change Workflow
```text
format/validate → static analysis → plan → human review → apply → verify → drift check
```
Use separate identities and approval rules for plan and apply. Review destroys, replacements, public exposure, IAM changes, and data-store modifications explicitly.

## Environments
Prefer separate state per environment and a consistent module version. Do not use workspaces as the only isolation boundary for accounts, credentials, or blast radius.

## Secrets
Pass secret references rather than plaintext where possible. Mark variables sensitive, but remember that `sensitive` hides output; it does not remove values from state. Use a secret manager and rotate credentials.

## Drift and Import
Run scheduled plan checks. Investigate drift rather than blindly overwriting manual changes. Import existing resources with ownership and lifecycle documentation.

## Destruction Safety
Use deletion protection, `prevent_destroy` only for deliberately protected resources, backups, and multi-person review. Test recovery for databases and object stores.

## Checklist
- [ ] Remote encrypted state and locking are configured.
- [ ] Providers and modules are version-pinned.
- [ ] Plan and apply identities are separated.
- [ ] IAM, public exposure, and destructive changes are gated.
- [ ] Secrets are not committed and state access is restricted.
- [ ] CI runs format, validation, scan, and policy checks.
- [ ] Drift detection is scheduled.
- [ ] Backups and restore paths are verified.
- [ ] Ownership and lifecycle are documented.

## References
- https://developer.hashicorp.com/terraform/docs
- https://developer.hashicorp.com/terraform/language/state
- https://developer.hashicorp.com/terraform/cloud-docs/policy-enforcement

---

*Dokumentasi ini bagian dari [AegisX Skills Collection](https://aegisxresearch.github.io/AegisX-Skills/). Dikelola oleh AegisX Research.*
