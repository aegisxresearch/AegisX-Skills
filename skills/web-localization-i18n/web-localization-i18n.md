# Web Localization & i18n

## Tujuan

Membuat aplikasi web yang mendukung banyak bahasa dan region dengan benar: kode tidak bercampur teks, format lokal (tanggal, angka, mata uang) akurat, RTL berfungsi, dan proses terjemahan berkelanjutan.

## Prasyarat

- Familiar dengan komponen UI dan routing
- Paham HTML/CSS

## Konsep inti

1. **i18n vs l10n** — i18n = arsitektur kode yang siap multi-bahasa; l10n = konten/budaya per lokasi.
2. **Pemisahan string** — semua teks UI lewat kunci terjemahan, bukan hardcode. Satu kunci = satu makna.
3. **Pluralization & interpolasi** — ICU MessageFormat (atau setara) menangani plural rules per bahasa; jangan concat string.
4. **Format lokal** — gunakan `Intl.DateTimeFormat`, `Intl.NumberFormat`, `Intl.RelativeTimeFormat`; jangan format manual.
5. **RTL** — pakai logical properties (`margin-inline-start`) bukan `left/right`; `dir="rtl"` pada elemen root; uji dengan bahasa Arab/Ibrani.
6. **Locale routing & SEO** — pola `/`, `/id`, `/en-US` (path-based) dengan `hreflang` dan canonical; pilih strategi yang konsisten (path > subdomain > query).
7. **Alur terjemahan** — extract kunci otomatis, file per locale, validasi kunci hilang/berlebih di CI.

## Contoh (illustrative)

```tsx
// i18n helper (pseudo-code — gunakan library seperti react-i18next/lingui)
import { t } from "./i18n";

export function NotificationCount({ count }: { count: number }) {
  return (
    <p>
      {t("notification_count", { count })} {/* ICU: {count, plural, =0 {Tidak ada notifikasi} one {# notifikasi} other {# notifikasi}} */}
    </p>
  );
}
```typescript

```tsx
// Format angka lokal
const formatter = new Intl.NumberFormat(locale, { style: "currency", currency });
```

## Checklist produksi

- [ ] Tidak ada string UI hardcoded di komponen
- [ ] Plural rules per bahasa benar (ICU atau library)
- [ ] Tanggal/angka/mata uang memakai `Intl`, bukan format manual
- [ ] RTL: layout memakai logical properties; snapshot test RTL
- [ ] `lang` dan `dir` pada `<html>` sesuai locale
- [ ] `hreflang` + canonical benar untuk SEO multi-locale
- [ ] CI: cek kunci hilang/berlebih, format file valid
- [ ] Fallback locale didefinisikan; kunci yang belum diterjemahkan jatuh ke default
- [ ] Terjemahan tidak memuat HTML tidak aman; sanitize bila perlu

## Kesalahan umum

- Concatenation string ("Hello " + name) — urutan kata berbeda per bahasa.
- `left`/`right` CSS untuk layout — pecah di RTL.
- Menerjemahkan nama merek/kode teknis.
- Satu file terjemahan raksasa tanpa namespace — konflik PR terus-menerus.
- Mengabaikan plural: "1 items" atau "2 item" muncul di beberapa bahasa.

## Trade-off dan Kapan Tidak Pakai

- i18n adds complexity — start with a few locales and grow.
- Machine translation is fast but error-prone — human review for customer-facing text.
- Locale routing (URL prefixes) is SEO-friendly but adds URL complexity.

## Referensi

- https://www.w3.org/International/ — panduan W3C i18n
- https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Intl — Intl API
- https://unicode-org.github.io/icu/userguide/format_parse/messages/ — ICU MessageFormat

---

*Dokumentasi ini bagian dari [AegisX Skills Collection](https://aegisxresearch.github.io/AegisX-Skills/). Dikelola oleh AegisX Research.*
