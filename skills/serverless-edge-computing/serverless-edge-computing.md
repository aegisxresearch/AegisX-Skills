# Serverless & Edge Computing

## Tujuan

Memanfaatkan serverless dan edge computing secara efektif: function yang kecil dan cepat, cold start yang dikelola, batasan platform dipahami, biaya terkendali, dan observability tetap lengkap.

## Prasyarat

- Paham HTTP dan deployment cloud
- Familiar dengan satu penyedia cloud

## Konsep inti

1. **Serverless ≠ tanpa server** — ada server yang dikelola penyedia; Anda tidak mengelola infra, tetapi harus hidup dalam batasan platform (timeout, memory, payload, concurrency).
2. **Cold start** — inisialisasi runtime saat instance baru. Mitigasi: ukuran bundle kecil, lazy import, provisioned concurrency (bila biaya layak), dan batasi warm-up pattern yang sia-sia.
3. **Desain function** — satu function = satu tanggung jawab; jangan monolith serverless. Idempotency penting karena retry otomatis.
4. **Edge vs region** — edge (Workers/Vercel Edge): latensi rendah, CPU terbatas, tanpa persistent state lokal; region (Lambda): kapasitas penuh, VPC/DB access.
5. **State & storage** — jangan simpan state di filesystem (ephemeral); gunakan DB/cache eksternal. Untuk edge, prefer KV/Durable Objects bila perlu state.
6. **Keamanan** — least privilege IAM, secret di env/vault, validasi input, rate limit di gateway, jangan log payload sensitif.
7. **Observability & biaya** — distributed tracing (X-Ray/OTel), metrics, struktur log; monitor invocation error rate, duration, dan cost per function.

## Contoh handler (illustrative)

```javascript
// Cloudflare Worker (illustrative)
export default {
  async fetch(request, env) {
    const url = new URL(request.url);
    if (url.pathname === "/api/status") {
      return Response.json({ ok: true, region: request.cf?.colo ?? "unknown" });
    }
    return new Response("Not found", { status: 404 });
  },
};
```

## Checklist produksi

- [ ] Fungsi dipecah per tanggung jawab; ukuran artifact terpantau
- [ ] Timeout lebih pendek dari limit platform; retry dengan backoff idempotent
- [ ] Cold start diukur (p95) dan mitigasi dipilih berdasarkan data
- [ ] IAM least privilege; secret tidak pernah masuk kode/log
- [ ] Rate limiting dan validasi input di lapisan masuk
- [ ] Tracing + metrics + alarm error rate per function
- [ ] Cost monitoring; alarm kenaikan biaya
- [ ] Test: unit handler, integration (local emulator), minimal 1 happy path + 2 edge case

## Kesalahan umum

- Function raksasa yang memuat seluruh aplikasi — cold start memburuk.
- Menyimpan state di memori/filesystem — hilang saat instance mati.
- Mengabaikan retry otomatis — duplikat efek (butuh idempotency).
- Tanpa observability — function gagal senyap.
- Over-provisioning concurrency — biaya melonjak tanpa manfaat.

## Referensi

- https://docs.aws.amazon.com/lambda/ — Lambda
- https://developers.cloudflare.com/workers/ — Workers
- https://vercel.com/docs/functions — Vercel Functions
- https://serverlessland.com/ — pola serverless

---

*Dokumentasi ini bagian dari [AegisX Skills Collection](https://aegisxresearch.github.io/AegisX-Skills/). Dikelola oleh AegisX Research.*
