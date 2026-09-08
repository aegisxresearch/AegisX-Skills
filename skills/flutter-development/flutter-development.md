# Flutter Development

## Tujuan

Membangun aplikasi Flutter yang cepat, teruji, dan mudah dirawat: struktur widget yang jelas, state management yang konsisten, integrasi platform yang aman, dan pipeline rilis yang andal.

## Prasyarat

- Dasar Dart
- Konsep mobile development

## Konsep inti

1. **Widget tree** — UI = composable widgets. Pisahkan widget presentasional (murni) dan container (stateful/state-aware).
2. **State management** — pilih satu pendekatan (Riverpod direkomendasikan untuk skala sedang-besar; Bloc untuk pola event-state yang tegas). Hindari `setState` global yang menyebar.
3. **Arsitektur** — lapisan: `presentation → application (use cases) → domain → data`. Jangan taruh logic bisnis di widget.
4. **Local DB** — `drift`/`sqflite` untuk data terstruktur, `Isar`/Hive untuk cache ringan. Enkripsi bila perlu.
5. **Platform integration** — `MethodChannel`/`Pigeon` untuk native module; permission via `permission_handler`.
6. **Performance** — `const` constructor, `RepaintBoundary`, `ListView.builder`/`SliverList`, hindari rebuild berlebihan; profile dengan DevTools.
7. **Rilis** — code signing (Android keystore, iOS certificates), obfuscation (`--obfuscate`), versioning, CI (GitHub Actions/codemagic).

## Contoh (illustrative)

```dart
// Riverpod — provider sederhana
final counterProvider = StateNotifierProvider<CounterNotifier, int>((ref) {
  return CounterNotifier();
});

class CounterNotifier extends StateNotifier<int> {
  CounterNotifier() : super(0);
  void increment() => state = state + 1;
}

// Widget
class CounterView extends ConsumerWidget {
  const CounterView({super.key});

  @override
  Widget build(BuildContext context, WidgetRef ref) {
    final count = ref.watch(counterProvider);
    return Text('$count');
  }
}
```

## Checklist produksi

- [ ] `flutter analyze` bersih; nol `print` tersisa di production
- [ ] State management konsisten; tidak ada logic di build method
- [ ] Semua string UI melalui l10n (`flutter gen-l10n`)
- [ ] Local DB dengan migrasi; data sensitif dienkripsi
- [ ] Permission diminta kontekstual
- [ ] Test: unit (logic), widget test (interaksi), integration test (alur utama); minimal 1 happy path + 2 edge case
- [ ] CI: analyze + test + build (Android APK + iOS unsigned)
- [ ] Obfuscation dan minify aktif untuk release
- [ ] Crash reporting + analitik; privacy manifest untuk store (Play/App Store)

## Kesalahan umum

- Semua widget `StatefulWidget` dengan `setState` — susah diuji dan dibaca.
- Menaruh API call di widget — tidak ada pemisahan data/UI.
- `ListView` tanpa builder untuk data dinamis.
- Mengabaikan `const` — rebuild dan memory tidak optimal.
- Keystore/iOS signing tidak aman — secret bocor atau build tidak bisa rilis.

## Referensi

- https://docs.flutter.dev/ — dokumentasi resmi
- https://riverpod.dev/ — state management
- https://bloclibrary.dev/ — alternatif Bloc
- https://docs.flutter.dev/testing — testing Flutter