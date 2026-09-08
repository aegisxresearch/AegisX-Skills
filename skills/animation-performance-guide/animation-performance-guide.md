# Animation Performance Guide

## Overview
Panduan animasi web yang performant: GPU-accelerated properties, will-change, reduced-motion, dan optimization.

---

## GPU-Accelerated Properties

### Safe to Animate (GPU-accelerated)
```css
/* ✅ GOOD - GPU accelerated */
transform: translateX(100px);
transform: scale(1.5);
transform: rotate(45deg);
opacity: 0.5;
filter: blur(5px);
```

### Avoid Animating (CPU-intensive)
```css
/* ❌ BAD - Causes layout/paint */
width: 100px;
height: 100px;
top: 50px;
left: 50px;
margin: 20px;
padding: 20px;
border-width: 5px;
```

### Why?
```text
Transform & Opacity → Composite only (fastest)
Width, Height, Top → Layout + Paint (slowest)
```

---

## CSS Animation Best Practices

### Smooth Transition
```css
/* ✅ Use transform for movement */
.card {
  transition: transform 0.3s ease-out;
}

.card:hover {
  transform: translateY(-4px);
}

/* ❌ Don't use top/margin for movement */
.card {
  transition: margin-top 0.3s ease-out; /* Janky! */
}

.card:hover {
  margin-top: -4px; /* Triggers layout! */
}
```python

### Keyframe Animation
```css
@keyframes fadeInUp {
  from {
    opacity: 0;
    transform: translateY(20px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

.animate-in {
  animation: fadeInUp 0.4s ease-out forwards;
  will-change: opacity, transform;
}
```

---

## will-change Property

### Usage
```css
/* Prepare for animation (before it happens) */
.card {
  will-change: transform, opacity;
}

/* Remove after animation completes */
.card.animated {
  will-change: auto;
}
```

### Rules
- [ ] Only use on elements that will animate
- [ ] Remove after animation completes
- [ ] Don't use on too many elements (memory overhead)
- [ ] Don't use on static elements

### Memory Impact
```css
/* ❌ Don't do this */
* {
  will-change: transform; /* Huge memory leak! */
}

/* ✅ Do this */
.animated-element {
  will-change: transform;
}
```css

---

## Reduced Motion

### Respect User Preference
```css
/* Check user preference */
@media (prefers-reduced-motion: reduce) {
  *,
  *::before,
  *::after {
    animation-duration: 0.01ms !important;
    animation-iteration-count: 1 !important;
    transition-duration: 0.01ms !important;
    scroll-behavior: auto !important;
  }
}
```typescript

### JavaScript Check
```javascript
const prefersReducedMotion = window.matchMedia(
  '(prefers-reduced-motion: reduce)'
).matches;

if (!prefersReducedMotion) {
  // Add animations
  element.classList.add('animate-in');
}
```

---

## Performance Monitoring

### Chrome DevTools
```text
1. Open DevTools → Performance tab
2. Record animation
3. Look for:
   - 🟢 Green bars = Composite (good)
   - 🟡 Yellow bars = Paint (slow)
   - 🔴 Red bars = Layout (very slow)
```

### Core Web Vitals
```javascript
// CLS (Cumulative Layout Shift)
// Target: < 0.1

// INP (Interaction to Next Paint)
// Target: < 200ms
```python

---

## Animation Libraries

### Framer Motion (`React`)
```jsx
import { motion } from 'framer-motion';

// ✅ Framer Motion uses transform by default
<motion.div
  initial={{ opacity: 0, y: 20 }}
  animate={{ opacity: 1, y: 0 }}
  transition={{ duration: 0.4 }}
>
  Content
</motion.div>
```

### GSAP (Vanilla JS)
```javascript
// ✅ GSAP uses transform by default
gsap.to('.card', {
  y: -4,
  duration: 0.3,
  ease: 'power2.out'
});
```python

### CSS Only (Lightest)
```css
/* ✅ Pure CSS is fastest */
@keyframes slideIn {
  from { transform: translateX(-100%); }
  to { transform: translateX(0); }
}

.animate {
  animation: slideIn 0.3s ease-out;
}
```

---

## Animation Checklist

### Performance
- [ ] Animate only transform & opacity
- [ ] Use will-change sparingly
- [ ] Remove will-change after animation
- [ ] Test on low-end devices
- [ ] Check Chrome DevTools Performance tab

### Accessibility
- [ ] Respect prefers-reduced-motion
- [ ] Don't auto-play animations
- [ ] Provide pause/stop controls
- [ ] No flashing content (seizure risk)

### Best Practices
- [ ] Keep animations under 500ms
- [ ] Use appropriate easing
- [ ] Don't block user interaction
- [ ] Test on mobile devices
- [ ] Monitor CLS and INP scores

---

## References
- https://web.dev/articles/sticky-headers
- https://developer.mozilla.org/en-US/docs/Web/Performance
- https://www.smashingmagazine.com/2021/03/complete-guide-accessible-front-end-components/

---

*Dokumentasi ini bagian dari [AegisX Skills Collection](https://aegisxresearch.github.io/AegisX-Skills/). Dikelola oleh AegisX Research.*
