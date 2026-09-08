# Anti-Slop Test Quality

## Goal
Write tests that fail when user-visible or contract-level behavior regresses, not tests that merely execute lines or confirm implementation details.

## Strong Assertions
Weak:
```typescript
expect(response).toBeDefined();
```yaml

Stronger:
```typescript
expect(response.status).toBe(422);
expect(response.body.error.code).toBe('VALIDATION_ERROR');
expect(response.body.error.details).toEqual([
  { field: 'email', message: 'Invalid email address' },
]);
```
Assert the smallest stable contract that matters. Avoid asserting incidental object ordering or private method calls.

## Minimum Case Set
For a meaningful behavior, cover:
- happy path;
- invalid or boundary input;
- dependency failure, authorization failure, conflict, timeout, or duplicate operation as relevant.

Do not invent irrelevant edge cases to increase test count.

## Mock Boundaries
Mock external systems at their boundary. Do not mock the function under test, its validators, or every internal collaborator. A mock should model success, failure, latency, malformed data, and retry behavior where those affect the contract.

## Mutation Resistance
A useful test should fail if an important condition, status code, transformation, or authorization check is removed. Periodically use mutation testing or deliberate fault injection on critical paths.

## Flake Prevention
- Avoid fixed sleeps; wait for observable state.
- Isolate data and time.
- Control randomness and clocks.
- Do not depend on test order or shared accounts.
- Clean up resources and listeners.
- Capture traces, logs, and screenshots for browser failures.

## Coverage Interpretation
Line coverage is a diagnostic signal, not proof of quality. Review branch, contract, risk, and failure-mode coverage. A highly covered test suite can still miss authorization, data leakage, or incorrect assertions.

## Checklist
- [ ] Assertions verify behavior or a public contract.
- [ ] At least one happy path and relevant negative cases exist.
- [ ] Tests would fail after a realistic regression.
- [ ] Mocks stop at external boundaries.
- [ ] Fixtures are isolated, minimal, and non-sensitive.
- [ ] No fixed sleeps or order dependence exist.
- [ ] Error, timeout, retry, and duplicate behavior is covered where relevant.
- [ ] Flaky tests have an owner and removal deadline.
- [ ] Coverage reports are interpreted with risk context.

---

## Kesalahan Umum / Pitfalls

- Asserting implementation details instead of behavior — tests break on refactors.
- Mocking everything, including the code under test's own collaborators.
- Writing tests that pass without ever failing — no assertion strength check.
- Ignoring flakey tests instead of fixing the root cause.

## Trade-off dan Kapan Tidak Pakai

- Heavy integration tests catch more but are slower and flakier — balance with unit tests.
- Property-based tests find edge cases but need good generators — not always worth it.
- 100% coverage is a target, not a quality metric — mutation testing is stronger.

*Dokumentasi ini bagian dari [AegisX Skills Collection](https://aegisxresearch.github.io/AegisX-Skills/). Dikelola oleh AegisX Research.*
