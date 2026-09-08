# Microfrontends & Module Federation

## Tujuan

Memecah frontend monolith menjadi modul yang dimiliki tim berbeda, dikembangkan dan di-deploy independen, lalu disatukan di runtime — tanpa mengorbankan pengalaman pengguna.

## Prasyarat

- Pengalaman membangun SPA (`React`/Vue/Svelte)
- Paham bundler (webpack/vite) dan CI/CD

## Konsep inti

1. **Kapan memakai** — gunakan saat tim > 3-4, konflik deploy tinggi, dan domain benar-benar terpisah. Jangan untuk aplikasi kecil.
2. **Pola integrasi**:
   - Build-time (npm package) — sederhana, tapi semua harus di-build ulang.
   - Runtime (Module Federation / import map) — deploy independen, standar modern.
   - Server-side composition (SSI/passthrough) — untuk render kritis SEO.
3. **Module Federation** — remote modules dimuat runtime; `shared` untuk dependency bersama (react, react-dom) agar satu instance.
4. **Kontrak antar-modul** — definisikan props/events/API yang eksplisit; jangan bocorkan detail internal.
5. **Routing** — satu router di shell; tiap remote menyediakan slot rutenya sendiri.
6. **Isolasi styling & state** — scoped CSS; state global sesedikit mungkin (auth, user preferences) via kontrak.

## Contoh webpack Module Federation (illustrative)

```javascript
// webpack.config.js — remote (bagian dari shell config host)
const { ModuleFederationPlugin } = require("webpack").container;

module.exports = {
  plugins: [
    new ModuleFederationPlugin({
      name: "cart",
      filename: "remoteEntry.js",
      exposes: {
        "./Cart": "./src/Cart",
      },
      shared: { react: { singleton: true }, "react-dom": { singleton: true } },
    }),
  ],
};
```python

```javascript
// Host / shell — memuat remote secara dinamis
import { lazy } from "react";

const Cart = lazy(() => import("cart/Cart"));
```

## Checklist produksi

- [ ] Kontrak antar-modul didokumentasikan dan di-versioned
- [ ] `shared` singleton untuk `React` dan library state; versi kompatibel diverifikasi di CI
- [ ] Remote punya fallback UI + error boundary saat gagal dimuat
- [ ] Duplikasi bundle dicek (bundle analyzer); shared deps tidak membengkak
- [ ] Versi remote dipin; cache busting `remoteEntry` saat deploy
- [ ] Test: E2E alur lintas-modul; unit per modul; kontrak props di-test
- [ ] Styling tidak bocor antar modul (CSS Modules / scope)
- [ ] Auth dan token dibagikan lewat kontrak, bukan global acak

## Kesalahan umum

- Memecah frontend untuk masalah yang sebenarnya organisasi/tim.
- Remote memanggil API internal modul lain secara langsung (keterikatan).
- Dua instance `React` akibat shared yang gagal singleton — hooks error.
- Tanpa fallback saat remote down — seluruh aplikasi blank.
- "Satu deploy lagi" tetap dibutuhkan karena shared deps berubah bersamaan.

## Referensi

- https://module-federation.io/ — dokumentasi Module Federation
- https://martinfowler.com/articles/micro-frontends.html — analisis mendalam
- https://micro-frontends.org/ — pola dan contoh

---

*Dokumentasi ini bagian dari [AegisX Skills Collection](https://aegisxresearch.github.io/AegisX-Skills/). Dikelola oleh AegisX Research.*
