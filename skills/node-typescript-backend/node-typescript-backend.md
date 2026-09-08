# Node.js `TypeScript` Backend

## Tujuan

Membangun backend Node.js yang strictly typed, modular, teruji, dan mudah dirawat — tanpa `any`, tanpa error handler kosong, tanpa callback hell.

## Prasyarat

- JavaScript/Node.js dasar
- `TypeScript` dasar

## Konsep inti

1. **Zod (atau skema sejenis)** — validasi runtime untuk input eksternal; `TypeScript` types hanya compile-time.
2. **Struktur modular** — pisahkan `routes`, `services`, `repositories`, `middleware`, `schemas`.
3. **Error handling terpusat** — satu error boundary; error domain vs error internal dipisah.
4. **Logging terstruktur** — JSON logs dengan request id; `pino` adalah pilihan umum.
5. **Typed API** — infer tipe request/response dari schema agar frontend dan backend sinkron.
6. **Process management** — jalankan dengan orchestrator (`Docker`) dan graceful shutdown; jangan `process.exit` sembarangan.

## Konfigurasi `TypeScript` (contoh)

```json
{
  "compilerOptions": {
    "target": "ES2022",
    "module": "NodeNext",
    "moduleResolution": "NodeNext",
    "strict": true,
    "noUncheckedIndexedAccess": true,
    "exactOptionalPropertyTypes": true,
    "outDir": "dist",
    "sourceMap": true
  }
}
```python

## Contoh Fastify + Zod

```typescript
// src/routes/users.ts
import type { FastifyPluginAsync } from "fastify";
import { z } from "zod";

const CreateUserSchema = z.object({
  email: z.string().email(),
  name: z.string().min(1).max(120),
});

export const userRoutes: FastifyPluginAsync = async (app) => {
  app.post("/users", async (request, reply) => {
    const parsed = CreateUserSchema.safeParse(request.body);
    if (!parsed.success) {
      return reply.status(400).send({ errors: parsed.error.flatten() });
    }
    const user = await app.userService.create(parsed.data);
    return reply.status(201).send(user);
  });
};
```

## Checklist produksi

- [ ] `strict: true`; nol `any` eksplisit (kecuali di boundary yang terdokumentasi)
- [ ] Validasi runtime semua input (body, query, params, headers)
- [ ] Error handler terpusat; log konteks tanpa data sensitif
- [ ] Graceful shutdown (SIGTERM/SIGINT) menutup koneksi DB dan server
- [ ] Health check endpoint terpisah dari auth
- [ ] Test: unit (service), integration (Fastify inject), minimal 1 happy path + 2 edge case
- [ ] Dependency pinned + lockfile; audit rutin (`npm audit`)
- [ ] Timeout dan `AbortController` untuk HTTP client keluar

## Kesalahan umum

- `catch (err) { console.log(err) }` tanpa langkah mitigasi.
- Menerima body mentah tanpa validasi, lalu diasumsikan shape-nya benar.
- Blocking event loop dengan operasi CPU berat atau sync DB driver.
- Menyimpan secret di kode/env yang ter-commit.
- Type cast `as any` untuk menutupi kekurangan tipe.

## Trade-off dan Kapan Tidak Pakai

- TypeScript adds safety but costs boilerplate — worth it for teams.
- Fastify vs Express — Fastify is faster but less familiar.
- Async is non-optional in Node — learn it properly.

## Referensi

- https://fastify.dev/docs/latest/ — Fastify
- https://zod.dev/ — Zod schema validation
- https://www.typescriptlang.org/tsconfig/ — opsi tsconfig

---

*Dokumentasi ini bagian dari [AegisX Skills Collection](https://aegisxresearch.github.io/AegisX-Skills/). Dikelola oleh AegisX Research.*
