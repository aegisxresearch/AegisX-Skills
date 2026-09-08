# Frontend Testing Playbook

## Goal
Test user-visible behavior at the lowest reliable layer. Prefer accessible queries and real integration boundaries over implementation details.

## Test Pyramid
```text
Pure logic and utilities       many, fast
Component behavior             focused, realistic
Route and API integration      fewer, high value
Browser E2E                    critical journeys only
Visual regression              stable visual contracts
```python

## Component Example
```typescript
import { render, screen } from '@testing-library/react';
import userEvent from '@testing-library/user-event';
import { LoginForm } from './LoginForm';

test('submits valid credentials', async () => {
  const user = userEvent.setup();
  const onSubmit = vi.fn();
  render(<LoginForm onSubmit={onSubmit} />);

  await user.type(screen.getByLabelText(/email/i), 'user@example.com');
  await user.type(screen.getByLabelText(/password/i), 'correct-password');
  await user.click(screen.getByRole('button', { name: /sign in/i }));

  expect(onSubmit).toHaveBeenCalledWith({
    email: 'user@example.com',
    password: 'correct-password',
  });
});
```python
Use the test runner already adopted by the application. The example assumes Vitest syntax; do not add a second runner solely for this pattern.

## Required Negative Cases
Every important form or flow should cover at least:
- invalid input and field-level error;
- server rejection and retry behavior;
- loading, timeout, empty, and unauthorized states where applicable.

## Network Boundaries
Mock at the network boundary, not inside the component. Keep mock payloads aligned with the API contract and include malformed or partial responses in contract tests.

```typescript
test('shows a retry action when the profile request fails', async () => {
  server.use(http.get('/api/profile', () => HttpResponse.error()));
  render(<ProfilePage />);

  expect(await screen.findByRole('button', { name: /retry/i })).toBeVisible();
});
```

## E2E Principles
- Use stable roles, labels, and test IDs only for elements without user-facing semantics.
- Isolate data with a unique test account or transaction fixture.
- Avoid fixed sleeps; wait for observable state.
- Keep authentication setup reusable and secure.
- Capture trace, console errors, and network failures on retry.

## Accessibility Checks
Run axe against pages and components, but do not treat automated checks as a complete audit. Add keyboard interaction tests for dialogs, menus, comboboxes, and drag alternatives.

## Visual Regression
Use deterministic data, fixed fonts, stable viewport, and animation disabling. Review diffs rather than setting an excessively permissive threshold.

## Test Data Rules
- Never use production data or real credentials.
- Generate unique identifiers per test.
- Reset state through an API or database fixture, not UI cleanup.
- Keep fixtures minimal and explicit.

## CI Gates
```text
lint → typecheck → unit/component → accessibility → integration → critical E2E → visual review
```
Parallelize independent suites, but preserve artifact collection when a test fails.

## Checklist
- [ ] Tests assert user-visible behavior.
- [ ] Happy path and negative cases exist.
- [ ] Loading, empty, error, and retry states are covered.
- [ ] Network mocks match current contracts.
- [ ] Accessibility assertions cover critical controls.
- [ ] E2E tests avoid sleeps and shared mutable accounts.
- [ ] CI stores traces, screenshots, and console output.
- [ ] Flaky tests are quarantined with an owner and expiry date.

## Kesalahan Umum / Pitfalls

- Testing only the happy path — no error states or edge cases.
- Snapshot tests that change on every layout tweak — brittle.
- E2E tests that are slow and flaky — CI becomes a lottery.
- No accessibility testing — a11y regressions are silent.

## Trade-off dan Kapan Tidak Pakai

- Visual regression testing is powerful but noisy — use it on critical pages only.
- Component tests are fast but miss integration issues — combine with E2E.
- Test coverage is not the goal — behavior coverage is.

## References
- https://testing-library.com/docs/
- https://playwright.dev/docs/test-intro
- https://www.w3.org/WAI/test-evaluate/

---

*Dokumentasi ini bagian dari [AegisX Skills Collection](https://aegisxresearch.github.io/AegisX-Skills/). Dikelola oleh AegisX Research.*
