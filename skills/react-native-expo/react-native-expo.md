# `React` Native & Expo

## Tujuan

Membangun aplikasi mobile iOS + Android dari satu codebase dengan `React` Native dan Expo: arsitektur teruji, navigasi, offline-first, push, serta pipeline build/rilis yang dapat diulang.

## Prasyarat

- `React`/JavaScript dasar
- Familiar dengan konsep mobile (permission, lifecycle app)

## Konsep inti

1. **Expo managed vs prebuild** — mulai dengan managed workflow; `expo prebuild` saat butuh native module khusus. Jangan jalankan `expo run:android` pada codebase yang belum di-setup.
2. **Navigasi** — `React` Navigation: stack, tabs, drawer. Navigasi adalah state; jangan simpan di global store.
3. **State** — server state: TanStack Query (cache + retry + pagination); client state: Zustand/Context minimal.
4. **Offline-first** — persist cache query; antrekan mutasi offline (background sync) untuk aksi penting.
5. **Push notification** — Expo Notifications/`expo-notifications`; simpan token push per user; tangani foreground/background.
6. **Build & rilis** — EAS Build (development/preview/production profile); EAS Update untuk update OTA; signing via EAS; naikkan versi build saat rilis store.
7. **Performance** — FlashList untuk list panjang, image optimization, hindari re-render global; profile dengan `React` DevTools.

## Contoh (illustrative)

```tsx
// navigasi + server state
import { createNativeStackNavigator } from "@react-navigation/native-stack";
import { useQuery } from "@tanstack/react-query";

const Stack = createNativeStackNavigator();

function ProductList() {
  const { data, isLoading } = useQuery({
    queryKey: ["products"],
    queryFn: () => fetch("/api/products").then((r) => r.json()),
  });
  // render dengan FlatList/FlashList
}
```

## Checklist produksi

- [ ] Permissions (kamera, lokasi, notifikasi) diminta saat dibutuhkan, bukan saat launch
- [ ] Secure storage untuk token (`expo-secure-store`); jangan AsyncStorage untuk secret
- [ ] Error boundary + fallback UI; loading state konsisten
- [ ] Push token: registrasi, refresh saat berubah, hapus saat logout
- [ ] Deep linking dikonfigurasi; link masuk ke screen yang benar
- [ ] Test: unit (jest), component (react-native-testing-library), E2E (maestro/detox) untuk alur utama
- [ ] Build production via EAS; versi build meningkat tiap rilis; changelog store
- [ ] Analitik dan crash reporting (Sentry) aktif sejak awal

## Kesalahan umum

- Menaruh semua state global — re-render seluruh app tiap perubahan.
- List tanpa virtualisasi — freeze di perangkat low-end.
- AsyncStorage untuk token — data tidak terenkripsi.
- Ignore status bar/notch/safe area — konten terpotong.
- Build lokal manual tanpa pipeline — "works on my machine" syndrome.

## Trade-off dan Kapan Tidak Pakai

- Expo is fast to develop but abstracts native — some features need native code.
- Offline-first adds sync complexity — consider if users are online.
- App store release cycles are slow — plan updates carefully.

## Referensi

- https://docs.expo.dev/ — dokumentasi Expo
- https://reactnavigation.org/ — navigasi
- https://tanstack.com/query/latest/docs/framework/react/react-native — TanStack Query
- https://docs.expo.dev/build/introduction/ — EAS Build

---

*Dokumentasi ini bagian dari [AegisX Skills Collection](https://aegisxresearch.github.io/AegisX-Skills/). Dikelola oleh AegisX Research.*
