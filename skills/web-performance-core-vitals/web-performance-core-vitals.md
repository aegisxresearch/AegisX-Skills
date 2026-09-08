# Web Performance & Core Web Vitals

## Goal
Optimize real-user experience using field data, not only local Lighthouse scores.

## Primary Signals
- **LCP:** loading performance; investigate slow server response, render-blocking resources, and hero images.
- **INP:** interaction responsiveness; reduce long main-thread tasks and unnecessary re-renders.
- **CLS:** visual stability; reserve dimensions for media, ads, and injected content.

Track p75 by device class and geography. Define budgets before optimizing.

## Performance Budget Example
```yaml
performance:
  javascript_initial_kb: 180
  largest_contentful_paint_ms: 2500
  interaction_to_next_paint_ms: 200
  cumulative_layout_shift: 0.1
  third_party_scripts: 5
```

## Loading Strategy
- Stream HTML where supported.
- Preload only critical, discoverable resources.
- Use responsive images with explicit dimensions.
- Lazy-load below-the-fold media.
- Avoid shipping client JavaScript for static content.
- Cache immutable assets with content hashes.

```html
<img
  src="/hero-1280.webp"
  srcset="/hero-640.webp 640w, /hero-1280.webp 1280w"
  sizes="100vw"
  width="1280"
  height="720"
  fetchpriority="high"
  alt="Product dashboard"
>
```

## Main Thread and INP
Break long work into smaller tasks, virtualize large lists, debounce expensive input handling, and keep event handlers short. Prefer CSS transitions and transforms for visual movement.

```typescript
function scheduleSearch(query: string, render: (value: string) => void): void {
  setTimeout(() => render(query), 0);
}
```
Use scheduling to yield to input; it is not a substitute for reducing the work itself.

## Caching
Separate browser, CDN, and server caches. Document cache keys, invalidation, stale behavior, and privacy boundaries. Never cache personalized responses in a shared cache without an explicit safe policy.

## Real User Monitoring
Capture:
- navigation and route timings;
- Web Vitals with attribution;
- device/network class;
- release version;
- consent-compliant sampling.

Do not collect URLs or payloads containing personal data.

## Investigation Workflow
1. Identify a regression in field data.
2. Segment by release, route, device, and connection.
3. Reproduce with CPU/network throttling.
4. Inspect trace for network, layout, scripting, and rendering cost.
5. Make one targeted change and compare p75.
6. Roll back if error rate or conversion degrades.

## Checklist
- [ ] Field data is available by route and release.
- [ ] Budgets are enforced in CI or deployment checks.
- [ ] Critical images have dimensions and intentional priority.
- [ ] Fonts use limited weights and appropriate loading strategy.
- [ ] Third-party scripts have owners and documented value.
- [ ] Long tasks and hydration cost are measured.
- [ ] Layout shifts are attributable and prevented.
- [ ] Performance alerts have actionable thresholds.

## References
- https://web.dev/articles/vitals
- https://developer.chrome.com/docs/lighthouse/overview
- https://developer.mozilla.org/en-US/docs/Web/Performance
