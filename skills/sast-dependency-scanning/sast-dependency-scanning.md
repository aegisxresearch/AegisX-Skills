# SAST & Dependency Scanning Automation

## Goal
Setiap pull request mendapat umpan balik security otomatis dalam hitungan menit: temuan baru di kode (SAST) dan kerentanan di dependensi (SCA), tanpa membanjiri reviewer dengan temuan lama.

## Operating Model
```text
PR -> SAST (diff-only) -> SCA (lockfile) -> Gate: critical/high fail
                                       -> SBOM artifact tersimpan
```

## SAST: pemindaian kode

Semgrep dengan baseline commit membuat PR hanya menampilkan temuan baru:

```bash
semgrep scan --config p/owasp-top-ten \
  --baseline-commit origin/main \
  --error --json -o sast.json
```

Aturan praktis:
- Mulai dari ruleset bawaan (`p/owasp-top-ten`, `p/default`), tulis rule kustom hanya setelah pola spesifik proyek ditemukan.
- Suppression inline harus menyertakan alasan: `# nosemgrep: rule-id karena X diverifikasi aman`.
- Reviewer harus menyetujui setiap suppression baru — ini perubahan kebijakan, bukan gaya kode.

## SCA: pemindaian dependensi

Dua layer yang saling melengkapi:

```bash
# 1. OSV: kerentanan yang diketahui, cepat dan gratis
osv-scanner --lockfile=package-lock.json

# 2. Trivy: kerentanan + misconfig + secret
trivy fs --severity HIGH,CRITICAL --exit-code 1 .
```

### Kebijakan fail yang sehat
```text
CRITICAL dengan fix tersedia  -> fail, wajib diperbaiki sebelum merge
CRITICAL tanpa fix            -> issue + mitigasi terdokumentasi
HIGH                          -> fail di dependensi langsung, warning di transitif
MEDIUM/LOW                    -> laporkan, jangan blokir
```

### SBOM per build
```bash
trivy fs --format cyclonedx --output sbom.json .
```
Simpan SBOM sebagai artifact CI. Saat CVE baru terpublikasi, cari cepat: "apakah artifact versi X yang kami deploy mengandung library Y?"

## Acceptance Checklist
- [ ] SAST berjalan diff-only di setiap PR
- [ ] Tidak ada suppression tanpa alasan dan persetujuan reviewer
- [ ] SCA membaca lockfile, bukan manifest saja
- [ ] Kebijakan fail per severity terdokumentasi dan diikuti CI
- [ ] SBOM dihasilkan dan disimpan sebagai artifact setiap build
- [ ] Waktu rata-rata dari temuan sampai fix terukur

## Kesalahan Umum / Pitfalls
- Scan manifest (`package.json`) tanpa lockfile — versi terpasang bisa berbeda dari yang discan.
- Mematikan scanner sepenuhnya karena terlalu banyak false positive — tune rules, jangan matikan.
- Suppression tanpa kedaluwarsa — utang security tersembunyi bertahun-tahun.
- Fail untuk semua severity — tim mematikan scanner karena menghalangi semua merge.
- SBOM dibuat tapi tidak pernah di-query — nilainya nol bila tidak dipakai saat insiden.

## Trade-off dan Kapan Tidak Pakai
- Semakin ketat gate, semakin lambat iterasi — mulai dari CRITICAL saja, naikkan bertahap.
- Rule kustom mahal dirawat — batasi untuk pola yang benar-benar spesifik proyek.
- Monorepo besar: scan full-repo melebihi batas waktu CI — gunakan baseline dan path filter.
- Untuk aplikasi internal dengan permukaan serangan kecil, DAST+review bisa lebih prioritas daripada SAST mendalam.

## Referensi
- https://semgrep.dev/docs/
- https://google.github.io/osv-scanner/
- https://trivy.dev/latest/docs/
- https://cyclonedx.org/

---

*Dokumentasi ini bagian dari [AegisX Skills Collection](https://aegisxresearch.github.io/AegisX-Skills/). Dikelola oleh AegisX Research.*
