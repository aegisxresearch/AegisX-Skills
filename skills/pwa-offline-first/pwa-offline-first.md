# PWA & Offline-First

## Tujuan

Membangun aplikasi web yang dapat diinstal, bekerja offline, cepat dimuat ulang, dan resilien terhadap koneksi buruk — dengan service worker dan strategi cache yang benar.

## Prasyarat

- HTML/CSS/JS dasar
- Pemahaman HTTP caching

## Konsep inti

1. **Service Worker (SW)** — script yang berjalan di thread terpisah; meng-intercept fetch dan mengelola cache. Hanya aktif di HTTPS (atau localhost).
2. **Lifecycle SW** — install → activate → fetch. Perbarui versi dengan cache name baru dan hapus cache lama di `activate`.
3. **Strategi cache**:
   - `cache-first` — aset statis (bundle, gambar).
   - `network-first` — navigasi/halaman (fallback ke cache saat offline).
   - `stale-while-revalidate` — konten yang boleh basi sesaat.
   - `network-only` — data sensitif/real-time.
4. **Precache** — daftar aset penting di-`addAll` saat install agar aplikasi langsung buka offline.
5. **Web App Manifest** — name, icons, theme color, display; syarat installability.
6. **Background sync** — antrekan aksi (mis. kirim pesan) saat offline dan jalankan saat online kembali.

## Contoh service worker (illustrative)

```javascript
// sw.js
const CACHE_NAME = "app-v1";
const PRECACHE = ["/", "/index.html", "/app.js", "/app.css"];

self.addEventListener("install", (event) => {
  event.waitUntil(caches.open(CACHE_NAME).then((c) => c.addAll(PRECACHE)));
  self.skipWaiting();
});

self.addEventListener("activate", (event) => {
  event.waitUntil(
    caches.keys().then((keys) =>
      Promise.all(keys.filter((k) => k !== CACHE_NAME).map((k) => caches.delete(k)))
    )
  );
  self.clients.claim();
});

self.addEventListener("fetch", (event) => {
  const { request } = event;
  if (request.method !== "GET") return;

  if (request.mode === "navigate") {
    // network-first untuk navigasi
    event.respondWith(
      fetch(request).catch(() => caches.match("/index.html"))
    );
    return;
  }

  // stale-while-revalidate untuk aset
  event.respondWith(
    caches.match(request).then((cached) => {
      const network = fetch(request).then((response) => {
        if (response.ok) {
          const copy = response.clone();
          caches.open(CACHE_NAME).then((c) => c.put(request, copy));
        }
        return response;
      });
      return cached || network;
    })
  );
});
```

## Checklist produksi

- [ ] HTTPS aktif; SW terdaftar dengan error handling
- [ ] Cache versioning; cache lama dibersihkan di activate
- [ ] Navigasi punya fallback offline (halaman/template)
- [ ] Tidak meng-cache request dengan Authorization header secara tidak aman
- [ ] Manifest: name, short_name, icons 192/512, theme_color, start_url
- [ ] Uji offline di DevTools (Offline mode) + Lighthouse PWA audit
- [ ] Test: unit strategi cache (workbox-build/mock), integration load halaman offline
- [ ] Update SW tidak menimpa data pengguna; versi di-versioning

## Kesalahan umum

- Cache semua request termasuk API dinamis tanpa batas ukuran.
- Update SW tanpa `skipWaiting`/`clients.claim` — pengguna stuck di versi lama.
- Cache melewati izin/auth sehingga halaman offline menampilkan data pengguna lain.
- Tanpa `Cache-Control` yang tepat, SW dan HTTP cache konflik.
- Mengabaikan pengguna yang mematikan JavaScript — SW butuh JS.

## Trade-off dan Kapan Tidak Pakai

- Offline-first is great for flaky networks but adds sync complexity — consider if users are online.
- Service workers are powerful but hard to debug — use Workbox.
- Push notifications need permission — don't rely on them.

## Referensi

- https://web.dev/learn/pwa/ — panduan resmi web.dev
- https://developer.chrome.com/docs/workbox/ — Workbox (produksi siap)
- https://developer.mozilla.org/en-US/docs/Web/Progressive_web_apps — MDN

---

*Dokumentasi ini bagian dari [AegisX Skills Collection](https://aegisxresearch.github.io/AegisX-Skills/). Dikelola oleh AegisX Research.*
