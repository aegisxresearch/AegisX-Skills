# Incident Response & SRE

## Goal
Reduce user impact first, preserve evidence, communicate , and improve the system without blame.

## Severity
Define severity by user impact, scope, data/security risk, and recovery urgency. Preassign escalation paths and response targets. Security incidents may require a separate restricted process.

## Roles
- Incident commander: makes priority and coordination decisions.
- Operations lead: executes mitigation and validates system state.
- Communications lead: updates stakeholders and status page.
- Scribe: records timeline, decisions, and evidence.

One person may hold multiple roles in a small incident, but ownership must be explicit.

## Triage Flow
```text
Detect → acknowledge → assess scope → stabilize → communicate → recover → verify → learn
```
Prioritize rollback, feature disablement, traffic shaping, failover, or graceful degradation over speculative fixes. Do not delete logs or restart systems without understanding evidence needs.

## Runbook Template
```markdown
# Alert: elevated API errors
## Impact
Which users and operations are affected?
## Signals
Dashboard, logs, traces, and related alerts.
## Immediate mitigation
Safe reversible actions in order.
## Escalation
Owner, backup, and service dependencies.
## Recovery validation
SLO, business metric, and data integrity checks.
## Follow-up
Permanent fix and review owner.
```

## Communication
State facts, impact, current action, next update time, and uncertainty. Avoid assigning blame or promising a root cause before evidence supports it. Notify affected users according to the incident policy.

## Postmortem
Include timeline, detection, contributing conditions, what worked, what failed, impact, and prioritized corrective actions. Actions need owners, due dates, and verification criteria.

## Checklist
- [ ] Severity and incident commander are declared.
- [ ] User impact and scope are measured.
- [ ] Mitigation is reversible and evidence-preserving.
- [ ] Stakeholders receive time-bounded updates.
- [ ] Data integrity and security implications are checked.
- [ ] Recovery is verified using user-visible signals.
- [ ] Postmortem is blameless and action-oriented.
- [ ] Repeated incidents feed reliability priorities.

## References
- https://sre.google/sre-book/managing-incidents/
- https://sre.google/resources/practices-and-processes/incident-management-guide/
- https://www.usenix.org/conference/srecon

---

*Dokumentasi ini bagian dari [AegisX Skills Collection](https://aegisxresearch.github.io/AegisX-Skills/). Dikelola oleh AegisX Research.*
