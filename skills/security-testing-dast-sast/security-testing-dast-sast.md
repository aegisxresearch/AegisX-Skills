# Security Testing: DAST & SAST

## Goal
Menemukan kerentanan dengan dua lapis: SAST menganalisis kode sebelum build, DAST menguji aplikasi berjalan setelah deploy ke staging. Keduanya melengkapi review manual dan threat modeling.

## Operating Model
```text
Commit -> SAST (code) -> Build -> Deploy staging -> DAST (runtime) -> Triage -> Fix -> Verify
```

## SAST: Static Analysis Security Testing

### Alat pilihan per bahasa
```text
Python:   bandit, semgrep
JS/TS:    semgrep, eslint-plugin-security
Go:       gosec, semgrep
Java:     spotbugs + find-sec-bugs, semgrep
Multi:    semgrep (bisa lintas bahasa dengan rule kustom)
```

### Integrasi CI dengan baseline
```yaml
# .github/workflows/security.yml (fragment)
- name: SAST scan
  run: |
    semgrep scan --config p/owasp-top-ten \
      --baseline-commit origin/main \
      --error --json -o sast-results.json
```

Prinsip penting:
- Scan hanya diff (baseline) agar tidak banjir temuan lama di PR baru.
- Semua suppression harus punya alasan dan reviewer, bukan `# nosemgrep` kosong.
- Gagal build untuk temuan severity tinggi (`critical`, `high`), warning untuk sisanya.

### DAST: Dynamic Analysis Security Testing

OWASP ZAP adalah pilihan open source standar. Jalankan di staging dengan konteks autentikasi:

```bash
zap-baseline.py -t https://staging.example.com \
  -r zap-report.html \
  -c zap-rules.conf \
  || true  # baseline mode: warning only, fail on new findings
```

Untuk authenticated scan, buat context ZAP dengan session cookie atau token, lalu gunakan `zap-full-scan.py`. Active scan hanya di environment staging yang datanya bisa dibuang.

### Triage: false positive vs actionable
```text
Temuan -> Cek request/response asli -> Reproduksi manual -> Klasifikasi:
  - False positive: dokumentasikan alasannya di rules config
  - Terkonfirmasi: buat issue dengan PoC + severity
  - Perlu konteks: tanyakan ke pemilik fitur
```

## Acceptance Checklist
- [ ] SAST berjalan di setiap PR dengan baseline commit
- [ ] Tidak ada suppression tanpa alasan tertulis
- [ ] DAST baseline scan berjalan di setiap deploy staging
- [ ] DAST authenticated scan berjalan mingguan
- [ ] Setiap temuan kritis punya issue dengan PoC dan owner
- [ ] Escape rate (temuan di prod yang lolos scan) diukur per kuartal

## Kesalahan Umum / Pitfalls
- Menjalankan active scan terhadap produksi — bisa merusak data atau memicu alarm.
- Mematikan scanner karena false positive tanpa men-tune rules — semua sinyal hilang.
- Memperlakukan DAST sebagai pengganti SAST — DAST tidak melihat kode, SAST tidak melihat runtime config.
- Menumpuk temuan tanpa SLA — backlog security yang tidak pernah turun.
- Scan tanpa autentikasi — hanya halaman login yang teruji.

## Trade-off dan Kapan Tidak Pakai
- SAST di monorepo besar menambah waktu CI — jalankan hanya pada path yang berubah.
- DAST penuh (full scan) bisa memakan waktu berjam-jam — jadwalkan, jangan blok setiap deploy.
- Untuk library (bukan aplikasi), DAST tidak relevan — fokus ke SAST dan SCA.
- WAF bisa menyembunyikan temuan DAST — scan dari dalam network saat memungkinkan.

## Referensi
- https://owasp.org/www-project-web-security-testing-guide/
- https://www.zaproxy.org/docs/docker/baseline-scan/
- https://semgrep.dev/docs/
- https://cheatsheetseries.owasp.org/cheatsheets/DAST_Automation_Cheat_Sheet.html

---

*Dokumentasi ini bagian dari [AegisX Skills Collection](https://aegisxresearch.github.io/AegisX-Skills/). Dikelola oleh AegisX Research.*
