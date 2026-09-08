# OpenAPI Spec-Driven Development

## Tujuan

Menjadikan spesifikasi OpenAPI sebagai sumber kebenaran API: kontrak disepakati sebelum implementasi, server/client di-generate atau divalidasi terhadap spec, dan perubahan API terdokumentasi otomatis.

## Prasyarat

- Familiar dengan REST dan JSON
- Paham siklus pengembangan API

## Konsep inti

1. **Contract-first vs code-first** — contract-first: spec ditulis dulu (desain terpikirkan, perubahan murah). Code-first: implementasi ditulis dulu, spec di-generate (cepat tapi kontrak sering terlupakan).
2. **Komponen reusable** — `components/schemas` untuk model; hindari duplikasi inline.
3. **Respons semua jalur** — definisikan status sukses dan semua error yang relevan (400, 401, 403, 404, 422, 429, 5xx).
4. **Pagination konsisten** — skema `page`/`page_size` atau `cursor` yang sama di seluruh API.
5. **Versioning spec** — simpan spec di repo, diff di CI, breaking change harus disetujui.
6. **Validasi otomatis** — Redocly/spectral lint di CI; contract test (Pact) atau request/response validation.

## Contoh skema (illustrative, OpenAPI 3.1)

```yaml
openapi: 3.1.0
info:
  title: Users API
  version: 1.0.0
paths:
  /users:
    post:
      operationId: createUser
      requestBody:
        required: true
        content:
          application/json:
            schema:
              $ref: "#/components/schemas/CreateUser"
      responses:
        "201":
          description: User created
          content:
            application/json:
              schema:
                $ref: "#/components/schemas/User"
        "422":
          description: Validation error
          content:
            application/json:
              schema:
                $ref: "#/components/schemas/Error"
components:
  schemas:
    CreateUser:
      type: object
      required: [email]
      properties:
        email: { type: string, format: email }
        name: { type: string, maxLength: 120 }
    User:
      allOf:
        - $ref: "#/components/schemas/CreateUser"
        - type: object
          properties:
            id: { type: string }
            created_at: { type: string, format: date-time }
    Error:
      type: object
      required: [code, message]
      properties:
        code: { type: string }
        message: { type: string }
```

## Alur kerja

1. Tulis/ubah spec di `openapi/` (atau root repo).
2. Jalankan lint: `redocly lint openapi.yaml` (standar konsisten).
3. Generate client/server bila memungkinkan (openapi-generator) — atau validasi runtime terhadap spec.
4. Jaga contoh (`examples`) agar dokumentasi hidup.
5. Diff spec di PR: `redocly bundle` + diff untuk mendeteksi breaking change.

## Checklist produksi

- [ ] Spec valid (lint lulus) dan ada di repo
- [ ] Semua operasi punya `operationId` unik
- [ ] Semua response error didokumentasikan
- [ ] Sensitive field tidak pernah masuk spec contoh (token, password asli)
- [ ] CI: lint + diff breaking change
- [ ] Mock server dari spec untuk pengembangan frontend paralel
- [ ] Dokumen API (Redoc/Swagger UI) otomatis dari spec yang sama

## Kesalahan umum

- Spec diabaikan setelah implementasi — kontrak dan kode berbeda.
- Menambahkan endpoint tanpa update spec, dokumentasi jadi usang.
- Menggunakan tipe samar seperti `object` tanpa properti.
- Menaruh secret di contoh spec yang ter-publish.
- Tanpa lint/diff di CI sehingga breaking change tidak terdeteksi.

## Referensi

- https://spec.openapis.org/oas/v3.1.0 — spesifikasi resmi
- https://redocly.com/docs/cli/ — lint dan bundle
- https://openapi-generator.tech/ — code generation