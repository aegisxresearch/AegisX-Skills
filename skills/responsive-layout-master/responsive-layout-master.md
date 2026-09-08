# Responsive Layout Master

## Overview
Panduan responsive design: mobile-first approach, fluid typography, container queries, dan layout patterns.

---

## Mobile-First Approach

### Breakpoint System
```css
/* Mobile-first: start with mobile, add complexity for larger screens */

/* Base: Mobile (0-640px) */
.container {
  padding: 16px;
  grid-template-columns: 1fr;
}

/* Tablet (641px+) */
@media (min-width: 641px) {
  .container {
    padding: 24px;
    grid-template-columns: repeat(2, 1fr);
  }
}

/* Desktop (1025px+) */
@media (min-width: 1025px) {
  .container {
    padding: 32px;
    grid-template-columns: repeat(3, 1fr);
    max-width: 1200px;
    margin: 0 auto;
  }
}
```typescript

### Standard Breakpoints
| Name | Width | Target |
|------|-------|--------|
| xs | 0-640px | Mobile |
| sm | 641-1024px | Tablet |
| md | 1025-1440px | Desktop |
| lg | 1441px+ | Large desktop |

---

## Fluid Typography

### Clamp Function (Modern)
```css
/* Fluid font size: min - preferred - max */
h1 {
  font-size: clamp(1.5rem, 4vw, 3rem);
  /* 24px → scales with viewport → 48px */
}

p {
  font-size: clamp(0.875rem, 2vw, 1rem);
  /* 14px → scales → 16px */
}
```

### Fluid Spacing
```css
:root {
  --space-xs: clamp(0.25rem, 0.5vw, 0.5rem);
  --space-sm: clamp(0.5rem, 1vw, 1rem);
  --space-md: clamp(1rem, 2vw, 2rem);
  --space-lg: clamp(1.5rem, 3vw, 3rem);
  --space-xl: clamp(2rem, 4vw, 4rem);
}
```css

---

## Layout Patterns

### 1. Holy Grail Layout
```css
.layout {
  display: grid;
  grid-template-areas:
    "header"
    "nav"
    "main"
    "footer";
  min-height: 100vh;
}

@media (min-width: 768px) {
  .layout {
    grid-template-columns: 250px 1fr;
    grid-template-areas:
      "header header"
      "nav    main"
      "footer footer";
  }
}
```css

### 2. Sidebar + Content
```css
.dashboard {
  display: grid;
  grid-template-columns: 1fr;
  min-height: 100vh;
}

@media (min-width: 1025px) {
  .dashboard {
    grid-template-columns: 260px 1fr;
  }
}

.sidebar {
  position: fixed;
  top: 0;
  left: 0;
  bottom: 0;
  width: 260px;
  transform: translateX(-100%);
  transition: transform 0.3s ease;
}

.sidebar.open {
  transform: translateX(0);
}
```

### 3. Card Grid (Auto-fit)
```css
/* Responsive cards without media queries! */
.card-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
  gap: 24px;
}
```css

### 4. Responsive Table
```css
/* Stack table on mobile */
@media (max-width: 768px) {
  table, thead, tbody, th, td, tr {
    display: block;
  }
  
  thead {
    position: absolute;
    width: 1px;
    height: 1px;
    overflow: hidden;
  }
  
  tr {
    margin-bottom: 16px;
    border: 1px solid #e5e7eb;
    border-radius: 8px;
  }
  
  td {
    text-align: right;
    padding-left: 50%;
    position: relative;
  }
  
  td::before {
    content: attr(data-label);
    position: absolute;
    left: 16px;
    font-weight: 600;
  }
}
```

---

## ️ Responsive Images

### Picture Element
```html
<picture>
  <source media="(min-width: 1024px)" srcset="large.webp">
  <source media="(min-width: 641px)" srcset="medium.webp">
  <img src="small.jpg" alt="Description" loading="lazy">
</picture>
```

### Responsive Image Sizes
```html
<img 
  srcset="photo-320.jpg 320w,
          photo-640.jpg 640w,
          photo-1280.jpg 1280w"
  sizes="(max-width: 640px) 100vw,
         (max-width: 1024px) 50vw,
         33vw"
  src="photo-640.jpg"
  alt="Description"
  loading="lazy"
>
```

---

## Container Queries (Modern)

```css
/* Parent container */
.card-container {
  container-type: inline-size;
}

/* Responsive to container, not viewport! */
@container (min-width: 400px) {
  .card {
    display: flex;
    flex-direction: row;
  }
}

@container (min-width: 700px) {
  .card {
    flex-direction: row;
    gap: 24px;
  }
}
```

---

## Responsive Checklist

### Mobile (0-640px)
- [ ] Touch targets ≥ 44px
- [ ] No horizontal scroll
- [ ] Text readable without zoom
- [ ] Forms easy to fill on mobile
- [ ] Images responsive

### Tablet (641-1024px)
- [ ] 2-column layouts work
- [ ] Sidebar collapses to hamburger
- [ ] Tables scroll horizontally or stack

### Desktop (1025px+)
- [ ] Max-width container (1200px)
- [ ] Sidebar always visible
- [ ] Hover states work
- [ ] Keyboard navigation

---

## Kesalahan Umum / Pitfalls

- Fixed pixel widths — break on small screens.
- No fluid typography — text overflows on mobile.
- Container queries where viewport queries would do — over-engineering.
- Testing only on one device — browsers differ.

## Trade-off dan Kapan Tidak Pakai

- Mobile-first is a mindset, not a rule — desktop-first works for some apps.
- Container queries are powerful but new — check browser support.
- Fluid grids can cause layout shifts — use min/max constraints.

## References
- https://web.dev/responsive-web-design-basics/
- https://css-tricks.com/snippets/css/complete-guide-grid/
- https://web.dev/learn/css/container-queries/

---

*Dokumentasi ini bagian dari [AegisX Skills Collection](https://aegisxresearch.github.io/AegisX-Skills/). Dikelola oleh AegisX Research.*
