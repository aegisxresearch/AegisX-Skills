# Design System Builder

## Overview
Panduan membangun Design System dari nol: design tokens, components, documentation, dan governance.

---

## ️ Design System Architecture

```
┌─────────────────────────────────────────────────────────┐
│                   DESIGN TOKENS                         │
│  (Colors, Typography, Spacing, Shadows)                 │
└─────────────────────┬───────────────────────────────────┘
                      │
                      ▼
┌─────────────────────────────────────────────────────────┐
│                   PRIMITIVES                            │
│  (Button, Input, Icon, Badge)                           │
└─────────────────────┬───────────────────────────────────┘
                      │
                      ▼
┌─────────────────────────────────────────────────────────┐
│                   COMPOSITIONS                          │
│  (Card, Modal, Sidebar, Form)                           │
└─────────────────────┬───────────────────────────────────┘
                      │
                      ▼
┌─────────────────────────────────────────────────────────┐
│                   PATTERNS                              │
│  (Auth Flow, Data Table, Navigation)                    │
└─────────────────────────────────────────────────────────┘
```

---

## Design Tokens

### Token Structure (JSON)
```json
{
  "color": {
    "primary": {
      "50": "#eff6ff",
      "100": "#dbeafe",
      "500": "#3b82f6",
      "900": "#1e3a8a"
    },
    "neutral": {
      "0": "#ffffff",
      "900": "#111827"
    }
  },
  "spacing": {
    "xs": "4px",
    "sm": "8px",
    "md": "16px",
    "lg": "24px",
    "xl": "32px"
  },
  "typography": {
    "fontFamily": {
      "sans": "Inter, system-ui, sans-serif",
      "mono": "JetBrains Mono, monospace"
    },
    "fontSize": {
      "sm": "14px",
      "base": "16px",
      "lg": "18px",
      "xl": "20px"
    }
  }
}
```

### CSS Custom Properties
```css
:root {
  /* Colors */
  --color-primary-500: #3b82f6;
  --color-neutral-900: #111827;
  
  /* Spacing */
  --spacing-xs: 4px;
  --spacing-sm: 8px;
  --spacing-md: 16px;
  
  /* Typography */
  --font-sans: 'Inter', system-ui, sans-serif;
  --font-mono: 'JetBrains Mono', monospace;
}
```

---

## Component Checklist

### Component Documentation
```markdown
# Button

## Purpose
Trigger actions or events.

## Variants
- primary, secondary, ghost, danger
- sm, md, lg

## Props
| Prop | Type | Default | Description |
|------|------|---------|-------------|
| variant | string | 'primary' | Visual style |
| size | string | 'md' | Button size |
| disabled | boolean | false | Disable interaction |
| loading | boolean | false | Show spinner |

## Usage
​```jsx
<Button variant="primary" size="md">
  Save Changes
</Button>
​```

## Accessibility
- Uses `<button>` element
- Focus ring visible on keyboard navigation
- Loading state announced to screen readers
```

---

## Spacing System

### Base Unit (4px grid)
```
4px   = 1 unit  (xs)
8px   = 2 units (sm)
16px  = 4 units (md)
24px  = 6 units (lg)
32px  = 8 units (xl)
48px  = 12 units (2xl)
64px  = 16 units (3xl)
```

### Usage Rules
```css
/* Consistent spacing */
.card {
  padding: var(--spacing-md);      /* 16px */
  margin-bottom: var(--spacing-lg); /* 24px */
}

/* Vertical rhythm */
h1 { margin-bottom: var(--spacing-lg); }
p  { margin-bottom: var(--spacing-md); }
```

---

## Color System

### Semantic Colors
```json
{
  "semantic": {
    "success": "green.500",
    "warning": "amber.500",
    "error": "red.500",
    "info": "blue.500"
  }
}
```

### Color Usage
```
✅ Use semantic tokens (success, error)
✅ Ensure 4.5:1 contrast ratio minimum
✅ Test with color blindness simulators
❌ Don't rely on color alone to convey info
```

---

## Typography Scale

### Modular Scale (1.25 ratio)
```yaml
xs:    12px / 16px  (0.75rem)
sm:    14px / 20px  (0.875rem)
base:  16px / 24px  (1rem)
lg:    18px / 28px  (1.125rem)
xl:    20px / 28px  (1.25rem)
2xl:   24px / 32px  (1.5rem)
3xl:   30px / 36px  (1.875rem)
4xl:   36px / 40px  (2.25rem)
```

### Line Height Rules
```yaml
Headings: 1.2 (tight)
Body:     1.5 (normal)
Small:    1.4 (compact)
```

---

## Accessibility (WCAG 2.1)

### Component Requirements
- [ ] Keyboard navigable (Tab, Enter, Escape)
- [ ] Focus indicators visible
- [ ] ARIA labels where needed
- [ ] Color contrast ≥ 4.5:1
- [ ] Screen reader tested
- [ ] Reduced motion supported

### Focus Styles
```css
/* Visible focus ring */
:focus-visible {
  outline: 2px solid var(--color-primary-500);
  outline-offset: 2px;
}

/* Skip to main content */
.skip-link {
  position: absolute;
  top: -40px;
  left: 0;
}
.skip-link:focus {
  top: 0;
}
```

---

## Design System Checklist

### Foundation
- [ ] Color palette defined (primary, neutral, semantic)
- [ ] Typography scale established
- [ ] Spacing system (4px grid)
- [ ] Border radius tokens
- [ ] Shadow tokens (elevation)
- [ ] Animation/transition tokens

### Components
- [ ] Button (variants, sizes, states)
- [ ] Input (text, textarea, select)
- [ ] Card
- [ ] Modal/Dialog
- [ ] Toast/Notification
- [ ] Avatar
- [ ] Badge
- [ ] Tooltip

### Documentation
- [ ] Storybook setup
- [ ] Component API docs
- [ ] Usage guidelines
- [ ] Do's and Don'ts
- [ ] Contribution guide

---

## References
- https://carbondesignsystem.com/
- https://material.io/design
- https://www.smashingmagazine.com/2022/01/front-end-architecture-design-systems/

---

*Dokumentasi ini bagian dari [AegisX Skills Collection](https://aegisxresearch.github.io/AegisX-Skills/). Dikelola oleh AegisX Research.*
