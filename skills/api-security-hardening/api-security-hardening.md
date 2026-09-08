# API Security Hardening

## Tujuan

Mengidentifikasi dan menutup kerentanan API yang paling umum dan paling mahal — terutama kesalahan otorisasi (BOLA/IDOR), validasi input, dan penyalahgunaan rate limit — dengan kontrol yang benar-benar bekerja, bukan sekadar komentar.

## Prasyarat

- Familiar dengan REST/API dan auth
- Dasar OWASP Top 10

## Konsep inti (sesuai OWASP API Top 10 2023)

1. **BOLA/IDOR (API1)** — otorisasi object-level: setiap akses ke resource (by id) harus memeriksa kepemilikan/peran. Jangan percaya `id` dari klien.
2. **Broken Authentication (API2)** — sesi/JWT yang kuat, rotasi, validasi issuer/audience/exp, brute-force protection.
3. **Broken Object Property Level (API3)** — jangan mass-assignment; field internal tidak bisa di-set dari input.
4. **Unrestricted Resource Consumption (API4)** — rate limit per user+IP+scope; batas ukuran payload; timeout eksternal.
5. **Broken Function Level Authorization (API5)** — periksa otorisasi per fungsi (RBAC), bukan hanya "sudah login".
6. **Unrestricted Access to Sensitive Business Flows (API6)** — alur bisnis (voucher, transfer) butuh rate limit + kontrol khusus.
7. **Server-Side Request Forgery (API7)** — validasi/allowlist URL saat server mem-fetch input pengguna.
8. **Security Misconfiguration (API8)** — CORS ketat, header security, no debug, secret tidak bocor.
9. **Improper Inventory Management (API9)** — versi API, endpoint lama/tersembunyi diinventaris dan di-retire.
10. **Unsafe Consumption of APIs (API10)** — validasi dan timeout pada integrasi pihak ketiga.

## Contoh kontrol (illustrative)

```python
# Otorisasi object-level — selalu cek kepemilikan
async def get_contract(user, contract_id, db):
    contract = await db.get_contract(contract_id)
    if contract is None or contract.owner_id != user.id:
        raise HTTPException(status_code=404)  # jangan ungkap keberadaan resource
    return contract
```

```json
// Rate limit header yang konsisten
{ "X-RateLimit-Limit": 100, "X-RateLimit-Remaining": 98, "Retry-After": "30" }
```

## Checklist produksi

- [ ] Otorisasi object-level di semua endpoint resource; uji BOLA/IDOR negatif
- [ ] Otorisasi fungsi (role) diperiksa server-side, bukan hanya di UI
- [ ] JWT: signature, issuer, audience, exp, rotasi; secret aman
- [ ] Validasi input: schema + size limit; mass-assignment diblokir
- [ ] Rate limit: per identity + per IP, dengan scope endpoint sensitif lebih ketat
- [ ] SSRF: allowlist host/URL saat fetch dari input
- [ ] CORS: daftar origin eksplisit; header keamanan terpasang
- [ ] Error response tidak membocorkan stack trace/struktur internal
- [ ] Inventory API: versi usang di-retire; endpoint tidak dikenal ditolak
- [ ] Test: minimal 1 happy path + 2 edge case negatif per kontrol (401/403/429/404)
- [ ] Scanning rutin: DAST + dependency audit

## Kesalahan umum

- Hanya cek "sudah login" lalu percaya id resource — IDOR.
- Rate limit tanpa identitas — mudah di-bypass via rotasi IP/akun.
- Mass assignment: `request.body` langsung di-map ke model.
- Error "resource not found" yang membedakan 403 vs 404 — membantu attacker.
- Secret di header contoh/response — log bocor.

## Referensi

- https://owasp.org/API-Security/editions/2023/en/0x11-t10/ — API Top 10
- https://cheatsheetseries.owasp.org/ — cheat sheets
- https://owasp.org/www-project-application-security-verification-standard/ — ASVS

---

*Dokumentasi ini bagian dari [AegisX Skills Collection](https://aegisxresearch.github.io/AegisX-Skills/). Dikelola oleh AegisX Research.*
