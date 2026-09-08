# Animation Performance Guide

> 🎯 **Kategori:** Web Design / Performance | **Level:** Intermediate

## Deskripsi
Panduan animasi web yang performant: GPU-accelerated properties, will-change, reduced-motion.

## Yang Dipelajari
- GPU-accelerated properties (transform, opacity)
- Properties yang harus dihindari (width, height, top, left)
- will-change usage & memory impact
- prefers-reduced-motion support
- Performance monitoring (Chrome DevTools)
- Animation libraries (Framer Motion, GSAP, CSS)

## File
📄 [`animation-performance-guide.md`](./animation-performance-guide.md) — Isi skill lengkap

## Golden Rule
```
Transform & Opacity → Composite only (fastest ✅)
Width, Height, Top → Layout + Paint (slowest ❌)
```

## References
- https://web.dev/articles/sticky-headers
- https://developer.mozilla.org/en-US/docs/Web/Performance
