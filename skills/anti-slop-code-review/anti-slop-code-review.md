# Anti-Slop Code Review

## Goal
Reject code that is verbose, speculative, duplicated, misleading, or disconnected from a verified requirement. Quality means correct behavior with proportional complexity.

## Review Order
```text
Requirement → changed surface → behavior → failure modes → consistency → complexity → evidence
```
Read the surrounding code before judging an isolated snippet. Preserve existing conventions unless the change has a measurable reason to introduce a new pattern.

## Red Flags
- Abstraction used once without clarifying a domain concept.
- Generic names such as `data`, `result`, `helper`, or `process` where intent matters.
- Comments that narrate syntax instead of explaining a decision.
- Dead branches, unreachable fallback code, unused imports, and unused configuration.
- Broad catches that discard errors or return fake success.
- `any`, unsafe casts, magic values, and hidden global state.
- New dependency for functionality already available in the project.
- “siap diuji di lingkungan staging” claims without tests, limits, or operational behavior.

## Evidence Questions
For every non-trivial change, ask:
1. Which user or system behavior does this change enable or protect?
2. What proves the behavior works?
3. What happens on invalid input, timeout, duplicate request, and dependency failure?
4. Why is this level of abstraction necessary?
5. Does the change follow the repository's existing stack and naming?

## Complexity Budget
Prefer the smallest complete implementation. Add a helper when it removes duplication or names a meaningful invariant, not merely to shorten a file. Avoid speculative interfaces, unused extension points, and configuration without a consumer.

## Review Output
Every finding should contain:
- location;
- concrete problem;
- user/system impact;
- actionable correction;
- confidence and severity.

Do not report stylistic preference as a defect. Do not claim a vulnerability without describing the attack path or violated invariant.

## Checklist
- [ ] Scope matches a verified requirement.
- [ ] Changed behavior has meaningful assertions.
- [ ] Error, timeout, retry, and duplicate cases are handled.
- [ ] No dead code, fake fallback, or unused abstraction was added.
- [ ] Types and validation reflect actual runtime values.
- [ ] Dependencies are justified and available.
- [ ] Logs and comments add useful information.
- [ ] Complexity is proportional to the problem.
- [ ] Findings are evidence-based and prioritized.

---

*Dokumentasi ini bagian dari [AegisX Skills Collection](https://aegisxresearch.github.io/AegisX-Skills/). Dikelola oleh AegisX Research.*
