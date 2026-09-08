# SAST & Dependency Scanning Automation

> **Kategori:** Security | **Level:** Intermediate

Panduan mengotomatisasi pemindaian kode (SAST) dan dependensi (SCA) di CI, dengan triase temuan dan kebijakan suppression yang terkelola.

## Yang Dipelajari
- SAST vs SCA: apa yang masing-masing temukan
- Semgrep untuk kode, OSV/Trivy untuk dependensi
- Baseline scanning agar PR baru hanya menampilkan temuan baru
- Kebijakan fail: severity mana yang memblokir merge
- SBOM sebagai hasil sampingan setiap build

## Production Outcome
Setiap PR tahu persis temuan security baru yang ia bawa, dan setiap build menghasilkan SBOM yang bisa diaudit.

## File
[`sast-dependency-scanning.md`](./sast-dependency-scanning.md) — Panduan lengkap

---

*Dokumentasi ini bagian dari [AegisX Skills Collection](https://aegisxresearch.github.io/AegisX-Skills/). Dikelola oleh AegisX Research.*
