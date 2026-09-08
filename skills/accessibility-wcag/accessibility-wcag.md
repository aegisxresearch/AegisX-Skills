# Accessibility & WCAG Engineering

## Goal
Make accessibility a product requirement, not a final audit. Target WCAG 2.2 AA unless a stricter contract applies.

## Operating Model
```text
Semantic structure → Keyboard interaction → Focus behavior → Assistive technology → Automated checks → Manual audit
```

## Semantic HTML First
```html
<main aria-labelledby="page-title">
  <h1 id="page-title">Account settings</h1>
  <form aria-describedby="form-help">
    <p id="form-help">Fields marked required must be completed.</p>
    <label for="email">Email address</label>
    <input id="email" name="email" type="email" autocomplete="email" required aria-describedby="email-error">
    <p id="email-error" role="alert" hidden>Enter a valid email address.</p>
    <button type="submit">Save changes</button>
  </form>
</main>
```

Prefer native elements before ARIA. Never add a widget role to a non-interactive element when a native `button`, `input`, `dialog`, or `select` is suitable.

## Keyboard Contract
- Every interactive control is reachable with `Tab`.
- `Enter` or `Space` activates controls according to native semantics.
- `Escape` closes dismissible overlays.
- Focus never becomes trapped behind a modal or lost after a route update.
- Focus indicators remain visible and have sufficient contrast.

## Dialog Pattern
```typescript
function closeDialog(dialog: HTMLDialogElement, returnTarget: HTMLElement): void {
  dialog.close();
  returnTarget.focus();
}

const dialog = document.querySelector<HTMLDialogElement>('#confirm-dialog');
const openButton = document.querySelector<HTMLButtonElement>('#open-dialog');

openButton?.addEventListener('click', () => {
  dialog?.showModal();
  dialog?.querySelector<HTMLElement>('[autofocus]')?.focus();
});
```
Use the native dialog where browser support and product requirements permit it. Otherwise implement focus trapping, inert background content, labelled title, and deterministic restoration.

## Live Regions
Use `role="status"` for non-urgent updates and `role="alert"` for urgent errors. Keep messages short and avoid updating a live region on every keystroke.

## Visual Requirements
- Body text contrast: at least 4.5:1.
- Large text contrast: at least 3:1.
- Do not communicate state through color alone.
- Support `prefers-reduced-motion`.
- Preserve zoom and reflow at narrow widths.

```css
:focus-visible {
  outline: 3px solid CanvasText;
  outline-offset: 3px;
}

@media (prefers-reduced-motion: reduce) {
  *, *::before, *::after {
    animation-duration: 0.01ms !important;
    transition-duration: 0.01ms !important;
    scroll-behavior: auto !important;
  }
}
```

## Testing Strategy
1. Run automated checks with axe in component and end-to-end tests.
2. Test all critical flows using keyboard only.
3. Test with at least one desktop and one mobile screen reader.
4. Verify zoom, reflow, contrast, errors, loading, and empty states.
5. Record violations with affected users, impact, and remediation owner.

## Acceptance Checklist
- [ ] Landmark structure is unique and logical.
- [ ] Heading hierarchy is meaningful.
- [ ] Every form control has a visible label.
- [ ] Errors are associated with fields and announced.
- [ ] Focus order matches visual and task order.
- [ ] Dialogs restore focus on close.
- [ ] Touch targets are large enough for the target platform.
- [ ] Motion can be reduced or disabled.
- [ ] Automated and manual checks pass for critical journeys.

## Common Failure Modes
- Using `div` click handlers instead of buttons.
- Adding ARIA while leaving invalid native semantics.
- Removing outlines without an equivalent focus style.
- Announcing the same status repeatedly.
- Testing only the happy path and not validation failures.

## References
- https://www.w3.org/TR/WCAG22/
- https://www.w3.org/WAI/ARIA/apg/
- https://developer.mozilla.org/en-US/docs/Web/Accessibility
