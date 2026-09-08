# Anti-Slop Agent Output

## Goal
Ensure an agent's final response is an accurate record of what it inspected, changed, verified, and could not verify.

## Evidence Model
Separate statements into:
- **Observed:** directly found in files or command output.
- **Changed:** modified by the agent.
- **Verified:** confirmed by a test, build, lint, or inspection.
- **Assumed:** plausible but not confirmed.
- **Blocked:** could not be checked and why.

Never present an assumption as a verification result.

## Required Summary
```text
Implemented:
- concrete files and behavior changed

Verification:
- exact commands or checks run
- outcome of each check

Risks/limitations:
- unverified environment behavior
- remaining edge cases

Next step:
- only if a concrete follow-up is needed
```

## Prohibited Claims
Do not claim:
- tests passed when they were not run;
- deployment succeeded without deployment output;
- security audit completed from a superficial read;
- a library exists without checking the repository or documentation;
- code is siap diuji di lingkungan staging without stating verification scope;
- all requirements are satisfied when ambiguous requirements remain.

## Scope Discipline
Report unrelated pre-existing changes separately. Do not silently rewrite files outside the requested scope. If a generated file changes, identify the generator or explain why it was edited directly.

## Concision
Prefer specific bullets over celebratory prose. Include file paths and meaningful behavior, not a long restatement of the task. Mention failures plainly and preserve the original error context.

## Handoff Checklist
- [ ] Changed files are named accurately.
- [ ] Behavior is described without exaggeration.
- [ ] Commands and results are reported exactly.
- [ ] Unverified assumptions are labeled.
- [ ] Limitations and remaining risks are visible.
- [ ] No fabricated dependency, test, deployment, or audit claim exists.
- [ ] Summary is concise enough to scan.

---

## Kesalahan Umum / Pitfalls

- Reporting 'done' without listing what was changed and what was tested.
- Stating assumptions as facts ('the endpoint is slow') without measurements.
- Omitting risks or known limitations to look more competent.
- Writing vague summaries instead of file-level, verifiable change lists.

## Trade-off dan Kapan Tidak Pakai

- Short reports are faster to read but may hide context — match depth to audience.
- Forcing a report format on trivial one-line fixes adds ceremony.
- Machine-readable output helps pipelines but hurts human debugging — use both.

## References

- https://www.anthropic.com/research/building-effective-agents
- https://docs.github.com/en/actions/security-guides/using-secrets-in-github-actions

*Dokumentasi ini bagian dari [AegisX Skills Collection](https://aegisxresearch.github.io/AegisX-Skills/). Dikelola oleh AegisX Research.*
