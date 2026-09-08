# `TypeScript` Advanced Patterns

> 🎯 **Kategori:** Programming / `TypeScript` | **Level:** Intermediate - Advanced

## Deskripsi
Panduan `TypeScript` lanjutan: generics, utility types, type guards, dan design patterns.

## Yang Dipelajari
- Generics (functions, interfaces, classes, constraints)
- Utility types (Partial, Pick, Omit, Record, ReturnType)
- Custom utility types (DeepPartial, RequireField)
- Type guards (typeof, instanceof, in, custom)
- Discriminated unions
- Design patterns (Builder, Factory, Observer)

## File
📄 [`typescript-advanced-patterns.md`](./typescript-advanced-patterns.md) — Isi skill lengkap

## Example
```typescript
type Result<T> =
  | { success: true; data: T }
  | { success: false; error: string }
```

## References
- https://www.typescriptlang.org/docs/handbook/
- https://github.com/type-challenges/type-challenges

---

*Dokumentasi ini bagian dari [AegisX Skills Collection](https://aegisxresearch.github.io/AegisX-Skills/). Dikelola oleh AegisX Research.*
