# AGENTS.md — AegisX Skills Collection

Instruksi operasional untuk coding agent yang bekerja pada repository ini.
Repository ini adalah **knowledge base dokumentasi**, bukan aplikasi executable.

---

## 1. Tujuan Repository

Kumpulan panduan engineering terstruktur untuk programmer, software engineer,
DevOps, security, dan ML engineer. Setiap skill adalah referensi praktis dengan
contoh, checklist, trade-off, dan referensi resmi.

## 2. Struktur Repository

```text
.
├── README.md                 # Katalog utama (digenerate dari manifest)
├── AGENTS.md                 # Instruksi operasional untuk agent
├── skills/
│   ├── manifest.json         # Source of truth metadata skill
│   └── <nama-skill>/
│       ├── README.md         # Ringkasan kategori, level, topik
│       └── <nama-skill>.md   # Panduan lengkap
└── scripts/
    ├── validate-skills.py    # Validator struktur, manifest, link, placeholder
    └── generate-readme.py    # Generator katalog README dari manifest
```

## 3. Source of Truth

- **`skills/manifest.json`** adalah satu-satunya sumber kebenaran daftar skill:
  id, kategori, level, summary, tags, path overview, dan path guide.
- **`README.md`** bagian katalog **tidak diedit manual** — dihasilkan oleh
  `scripts/generate-readme.py` dari manifest.
- Setiap skill aktual = direktori `skills/<nama-skill>/` berisi `README.md` dan
  `<nama-skill>.md`, **plus** entri di manifest.
- Klaim jumlah skill harus selalu mengacu pada manifest/direktori aktual.
  Jangan menyebut jumlah skill, sub-agent, atau fitur yang tidak ada filenya.

## 4. Aturan Menulis/Mengubah Skill

1. Buat folder `skills/<nama-skill>/` dengan `README.md` dan `<nama-skill>.md`.
2. `README.md`: kategori, level, deskripsi singkat, dan referensi.
3. Panduan utama: tujuan, konsep, contoh, trade-off, failure modes, checklist,
   referensi resmi.
4. Tambahkan entri di `skills/manifest.json` (id, category, level, summary,
   tags, overview, guide, status).
5. Jalankan `python3 scripts/generate-readme.py` lalu
   `python3 scripts/validate-skills.py`.
6. Jangan membuat file di `.freebuff/` atau mengklaim katalog yang tidak ada
   di repository.

## 5. Anti-Slop Guardrails

1. Jangan menambahkan dependency, import, API, atau konfigurasi tanpa verifikasi
   dari manifest, lockfile, source, atau dokumentasi resmi.
2. Jangan menyebut kode `production-ready`, test lulus, deployment berhasil,
   atau audit selesai tanpa bukti verifikasi yang sesuai.
3. Setiap contoh kode harus memiliki minimal satu happy path dan failure/edge
   case yang relevan; assertion harus memverifikasi behavior, bukan sekadar
   eksekusi.
4. Jangan menambahkan abstraksi, komentar, konfigurasi, mock, atau dokumentasi
   yang tidak memiliki tujuan terverifikasi.
5. Bedakan contoh `runnable`, `illustrative`, dan `pseudo-code`; jelaskan
   trade-off, failure modes, serta batasan.
6. Laporkan file yang diubah, command yang dijalankan, hasil verifikasi, asumsi,
   dan risiko secara faktual.
7. Utamakan perubahan terkecil yang lengkap, konsisten dengan repository, dan
   dapat dipelihara.
8. Jangan menyalin konten dari luar repository tanpa verifikasi fakta dan lisensi.

Skill terkait (ada di repository ini):
- `skills/anti-slop-code-review/`
- `skills/anti-slop-test-quality/`
- `skills/anti-hallucinated-dependencies/`
- `skills/anti-slop-documentation/`
- `skills/anti-slop-agent-output/`

## 6. Gate Validasi

Sebelum menyatakan selesai, jalankan:

```bash
python3 scripts/validate-skills.py     # wajib: 0 error
python3 scripts/generate-readme.py     # wajib: katalog sinkron
```

Validator memeriksa:

- pasangan `README.md` / `<nama-skill>.md` lengkap;
- manifest sinkron dengan direktori aktual;
- metadata valid (id unik, kategori, level, status, path ada);
- tanpa placeholder (`TODO: implement later`, `PLACEHOLDER`, `FIXME`);
- tanpa karakter kontrol (NUL);
- link lokal Markdown valid;
- README utama menautkan semua skill dan jumlah klaim benar.

Repository ini tidak memiliki test runner atau aplikasi yang dapat dieksekusi;
validasi struktur di atas adalah gate yang relevan.

## 7. Alur Kerja Agent

1. Baca `skills/manifest.json` untuk daftar skill aktual dan metadata.
2. Untuk tugas konten: cek konvensi skill yang sudah ada sebelum menulis.
3. Untuk tugas struktur: ubah manifest terlebih dahulu, baru regenerate README.
4. Jalankan validator dan generator; perbaiki semua temuan sampai 0 error.
5. Laporkan hasil secara faktual (lihat format laporan di bawah).

## 8. Format Laporan Agent

Setiap laporan akhir harus memuat:

- **Perubahan**: file yang ditambahkan/diubah (path lengkap).
- **Verifikasi**: command yang dijalankan dan hasilnya.
- **Asumsi**: keputusan yang diambil tanpa bukti langsung.
- **Risiko/Keterbatasan**: apa yang belum diverifikasi dan mengapa.

Jangan menyatakan "selesai"/"sukses" tanpa daftar bukti di atas.

## 9. Eskalasi

Jika instruksi bertentangan dengan isi repository (misalnya klaim fitur yang
tidak ada filenya), utamakan fakta repository dan catat konflik tersebut dalam
laporan alih-alih mengikuti klaim yang tidak dapat diverifikasi.