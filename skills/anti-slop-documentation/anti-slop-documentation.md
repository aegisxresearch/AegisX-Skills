# Anti-Slop Documentation

## Goal
Make documentation useful for a real decision, implementation, or verification task. Remove impressive-sounding claims that do not change what the reader can do.

## Required Questions
Every substantial guide should answer:
1. What problem does this solve?
2. When should it be used?
3. When should it not be used?
4. What are the costs, risks, and trade-offs?
5. How can the reader verify the result?

## Claim Quality
Replace vague claims:
```text
This architecture is scalable and production-ready.
```
with bounded claims:
```text
This design separates read traffic from writes and can scale read replicas independently; it still requires consistency, failover, and lag monitoring.
```
A benchmark must include workload, hardware, version, sample size, metric, and limitations.

## Example Labels
Use one of these labels:
- **Runnable:** tested in the stated environment.
- **Illustrative:** demonstrates a pattern; integration details remain.
- **Pseudo-code:** intentionally omits syntax or implementation details.

Do not present pseudo-code as copy-paste production code.

## References
Prefer official, versioned, primary sources. Record access date or version when behavior can change. A link is not evidence unless it supports the nearby claim.

## Consistency
Use the repository's terminology, headings, code style, and file conventions. Keep README summaries synchronized with the main document. Remove obsolete examples instead of layering contradictory advice.

## Review Checklist
- [ ] Purpose and audience are clear.
- [ ] Scope and non-goals are stated.
- [ ] Examples have an honest execution label.
- [ ] Security, failure, and operational behavior are covered.
- [ ] Claims are bounded and evidence-backed.
- [ ] Trade-offs are explicit.
- [ ] References are relevant and authoritative.
- [ ] Internal links and filenames are valid.
- [ ] No filler section exists merely to increase length.
