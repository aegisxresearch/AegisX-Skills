# Property-Based Testing

## Tujuan

Menemukan bug yang tidak terpikirkan oleh contoh-based testing: mendefinisikan *invariant* (property) yang harus selalu benar, lalu membiarkan framework meng-generate ratusan input acak dan mengecilkan (shrink) input yang gagal.

## Prasyarat

- Pengalaman menulis unit test
- Familiar dengan satu bahasa (contoh: Python/TS/Rust)

## Konsep inti

1. **Property vs contoh** — contoh: input spesifik → output harapan. Property: untuk semua input yang memenuhi kondisi (precondition), output memenuhi invariant (postcondition).
2. **Generator** — framework meng-generate input (int, string, list, custom objects). Tulis generator khusus untuk domain (mis. email valid, struktur order).
3. **Shrinking** — saat test gagal, framework mencari input paling kecil yang tetap gagal. Hasilnya kasus reproduksi yang mudah dibaca.
4. **Sumber property umum**:
   - Round-trip: encode → decode = identik (serialisasi, kompresi).
   - Invariant: hasil selalu valid/terurut/tidak negatif.
   - Idempotency: `f(f(x)) == f(x)` (dedup, normalisasi).
   - Hukum aljabar: associativity/commutativity (menggabungkan operasi).
   - Oracle: hasil kode baru vs implementasi referensi.
5. **Boundaries** — generator wajib mencakup edge: 0, -1, max int, string kosong, Unicode, string sangat panjang, list kosong/duplikat.
6. **Integrasi** — jalankan dengan seed tetap di CI (deterministik) + seed acak saat development.

## Contoh (illustrative)

```python
from hypothesis import given, strategies as st


@given(st.lists(st.integers()))
def test_sort_returns_sorted(items):
    sortedItems = sorted(items)
    assert sortedItems == sorted(sortedItems)  # invariant: sorted
    assert len(sortedItems) == len(items)      # invariant: elemen tidak hilang
    assert set(sortedItems) == set(items)      # invariant: permutasi


@given(st.text())
def test_json_round_trip(text):
    import json
    assert json.loads(json.dumps(text)) == text
```

## Checklist produksi

- [ ] Property mendeskripsikan invariant nyata, bukan menyalin implementasi
- [ ] Precondition eksplisit (asumsi) — jangan property yang selalu gagal karena input invalid
- [ ] Generator custom untuk domain; boundary tercakup
- [ ] Shrinking menghasilkan kasus minimal yang terbaca
- [ ] Deterministik di CI (seed tetap); jalankan cukup banyak contoh (100+)
- [ ] Property-test melengkapi example-based test — bukan pengganti
- [ ] Timeout/budget di-set agar suite tidak meledak

## Kesalahan umum

- Property yang menyalin implementasi (`f(x) == my_implementation(x)`) — tidak menguji apa-apa.
- Generator memproduksi input invalid tanpa precondition.
- Mengabaikan shrinking — gagal sulit direproduksi.
- Hanya property test tanpa example test untuk kasus bisnis spesifik.
- Memakai generator default yang tidak mencakup edge domain.

## Trade-off dan Kapan Tidak Pakai

- Property-based testing finds edge cases but needs good generators — invest in them.
- It complements, not replaces, example-based tests — use both.
- Hypothesis/QuickCheck add a learning curve — start with simple properties.

## Referensi

- https://hypothesis.readthedocs.io/ — Hypothesis (Python)
- https://fast-check.dev/ — fast-check (JS/TS)
- https://proptest-rs.github.io/proptest/ — Proptest (Rust)
- https://fsharpforfunandprofit.com/posts/property-based-testing/ — pengantar yang jelas

---

*Dokumentasi ini bagian dari [AegisX Skills Collection](https://aegisxresearch.github.io/AegisX-Skills/). Dikelola oleh AegisX Research.*
