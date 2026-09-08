# Contributing

Terima kasih sudah ingin berkontribusi ke **AegisX Skills Collection**. Repository ini adalah koleksi panduan teknis (skills) yang harus akurat, konsisten, dan mudah dirawat. Semua kontribusi diverifikasi otomatis oleh CI — pastikan Anda mengikuti alur di bawah ini.

## Cara menambahkan skill baru

1. Buat folder baru: `skills/<nama-skill>/`
2. Tambahkan `README.md` dengan ringkasan: kategori, level, deskripsi, dan references.
3. Tambahkan file panduan utama `<nama-skill>.md` berisi:
   - konsep inti dan contoh;
   - trade-off dan failure modes;
   - checklist yang dapat diverifikasi;
   - referensi resmi yang relevan.
4. Daftarkan skill di `skills/manifest.json` dengan metadata lengkap:
   ```json
   {
     "id": "<nama-skill>",
     "category": "<kategori>",
     "level": "beginner | intermediate | advanced",
     "summary": "Satu kalimat deskriptif.",
     "tags": ["tag1", "tag2"],
     "overview": "skills/<nama-skill>/README.md",
     "guide": "skills/<nama-skill>/<nama-skill>.md",
     "status": "maintained",
     "last_reviewed": "YYYY-MM-DD"
   }
   ```
5. Jalankan generator dan validator lokal:
   ```bash
   python3 scripts/generate-readme.py
   python3 scripts/validate-skills.py
   ```
   Validator harus lolos (exit code 0) sebelum PR dikirim.

## Panduan kualitas konten

- Contoh kode harus diberi label jujur: `runnable`, `illustrative`, atau `pseudo-code`.
- Setiap klaim teknis harus bisa diverifikasi — hindari kata kunci kosong seperti "scalable", "robust", atau "production-ready" tanpa kriteria.
- Jelaskan trade-off dan kapan suatu pendekatan **tidak** tepat digunakan.
- Jangan menambahkan library atau dependency fiktif; verifikasi API dan versi yang nyata.
- Referensi yang dipakai harus resmi dan masih relevan.

## Memperbarui skill yang ada

- Perbaiki konten, lalu **perbarui `last_reviewed`** di `skills/manifest.json` ke tanggal hari ini.
- Jika isi sudah tidak relevan, ubah `status` menjadi `needs-review` atau `deprecated` alih-alih membiarkannya tampak terawat.
- Jalankan kembali generator dan validator.

## Commit message

Gunakan [Conventional Commits](https://www.conventionalcommits.org/):

```text
feat: add <nama-skill> skill
docs: fix broken link in <skill>
chore: update manifest metadata
ci: add workflow step
```

## Proses Pull Request

1. Buat branch dari `main`.
2. Terapkan perubahan dan jalankan `scripts/generate-readme.py` + `scripts/validate-skills.py`.
3. Push dan buka PR — workflow **Skills Validation** akan berjalan otomatis.
4. PR hanya bisa lolos jika validator, lint, dan cek sinkronisasi katalog semuanya hijau.
5. Jika workflow `docs` aktif, situs GitHub Pages diperbarui otomatis setelah merge ke `main`.