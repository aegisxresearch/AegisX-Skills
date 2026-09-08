# GDPR & Data Privacy Engineering

## Tujuan

Membangun produk yang memenuhi kewajiban perlindungan data pribadi secara teknis: tahu data apa yang diproses, mengapa, oleh siapa, berapa lama — dan mampu memenuhi hak subjek data.

> Catatan: dokumen ini adalah panduan engineering, bukan nasihat hukum. Konfigurasi kepatuhan final harus direview oleh penasihat hukum sesuai yurisdiksi.

## Prasyarat

- Paham arsitektur aplikasi dan alur data
- Konsep dasar hukum privasi

## Konsep inti

1. **Data mapping** — inventaris: data apa yang diproses (kategori), untuk tujuan apa (legal basis), dari mana, ke mana, berapa lama disimpan. Ini fondasi semua kewajiban lain.
2. **Privacy by design & default** — minimisasi (hanya data yang diperlukan), pseudonymisasi bila memungkinkan, kontrol akses granular, dan pengaturan default yang paling tidak invasif.
3. **Consent** — opt-in eksplisit, granular per tujuan, mudah dicabut setara dengan memberi; jangan pre-checked. Simpan bukti consent (versi, timestamp, wording).
4. **Data Subject Requests (DSR)** — akses, perbaikan, hapus ("right to be forgotten"), portabilitas. Pipeline teknis: identifikasi data subjek lintas sistem, verifikasi identitas, SLA waktu (umumnya 30 hari), dan proses hapus termasuk backup.
5. **Retention & deletion** — kebijakan retention per kategori data; hapus otomatis saat batas; data anonim (tidak dapat diidentifikasi ulang) tidak lagi dianggap data pribadi.
6. **Transfer** — data lintas negara perlu mekanisme sah (SCC, adequacy); minimalkan transfer ke pihak ketiga.
7. **Incident & breach** — deteksi, containment, notifikasi (dalam waktu yang ditentukan jika berisiko), dan dokumentasi.

## Checklist teknis

- [ ] Data mapping dipertahankan dan diperbarui saat fitur baru
- [ ] Data minimisasi diterapkan: tidak ada field "mungkin berguna nanti"
- [ ] Consent flow: granular, opt-in, bukti tersimpan, pencabutan mudah
- [ ] DSR pipeline: akses/hapus/portabilitas lintas sistem + verifikasi identitas
- [ ] Retention schedule aktif; penghapusan otomatis dan teruji (termasuk backup)
- [ ] Logging tanpa data pribadi yang tidak perlu; log akses ke data sensitif
- [ ] Enkripsi saat transit dan at rest; kunci dikelola aman
- [ ] Vendor/sub-processor punya DPA dan akses minimal
- [ ] Uji privacy (penetration + DSR drill) berkala

## Kesalahan umum

- Menganggap "anonymized" padahal masih bisa diidentifikasi ulang (pseudonymized).
- Menyimpan data tanpa batas waktu "untuk jaga-jaga".
- Consent tidak terdokumentasi — tidak bisa membuktikan validitas.
- Hapus data utama tapi salinan tetap di backup/cache.
- Log dengan data pribadi mentah (email, IP penuh) tanpa alasan.

## Referensi

- https://gdpr-info.eu/ — teks regulasi
- https://www.edpb.europa.eu/ — pedoman EDPB
- https://iapp.org/ — praktik industri privasi