# PostgreSQL Query Tuning

## Goal
Mengubah proses "database lambat, tambah index" menjadi proses terukur: temukan query terburuk dari data nyata, baca rencana eksekusinya, perbaiki dengan bukti.

## Operating Model
```text
pg_stat_statements -> pilih query terlama -> EXPLAIN (ANALYZE, BUFFERS)
-> identifikasi bottleneck -> perbaiki (index/rewrite) -> ukur ulang
```

## Konsep Inti

### 1. Temukan dulu, jangan menebak
```sql
-- 5 query terlama total (bukan per-call)
SELECT query, calls, total_exec_time, mean_exec_time
FROM pg_stat_statements
ORDER BY total_exec_time DESC
LIMIT 5;
```
Query yang dipanggil 10x/detik dengan 50ms lebih penting daripada query laporan yang berjalan 5 detik sekali sehari.

### 2. Baca EXPLAIN dengan benar
```sql
EXPLAIN (ANALYZE, BUFFERS, FORMAT TEXT)
SELECT * FROM orders
WHERE customer_id = 42 AND status = 'pending'
ORDER BY created_at DESC
LIMIT 20;
```

Yang perlu dicari:
```text
Seq Scan di tabel besar          -> butuh index (atau memang wajar untuk scan penuh)
Rows estimasi vs actual jauh     -> statistik basi -> ANALYZE
Nested Loop dengan inner scan    -> cek apakah inner loop pakai index
Sort node di atas LIMIT          -> top-N heapsort OK; external merge = alarm
Buffers: shared read tinggi      -> cache miss, cek working set
```

### 3. Index yang tepat untuk query ini
```sql
-- Composite index mengikuti urutan: equality dulu, range/sort kemudian
CREATE INDEX idx_orders_customer_status_created
  ON orders (customer_id, status, created_at DESC);

-- Partial index untuk subset yang benar-benar di-query
CREATE INDEX idx_orders_pending
  ON orders (customer_id, created_at DESC)
  WHERE status = 'pending';

-- Covering index (index-only scan) bila kolom tambahan sedikit
CREATE INDEX idx_orders_customer_cover
  ON orders (customer_id) INCLUDE (status, total_amount);
```

Verifikasi dampak: jalankan EXPLAIN lagi — harus Index Scan/Index Only Scan, dan bandingkan `Buffers: shared hit` sebelum vs sesudah.

### 4. Pola yang selalu lambat
```text
N+1:      loop di aplikasi memicu ratusan query kecil -> gabung dengan JOIN atau IN
OFFSET:   OFFSET 100000 berarti baca dan buang 100000 baris -> keyset pagination
LIKE '%x': wildcard depan mematikan B-tree -> trigram index (pg_trgm) untuk search
COUNT(*):  di tabel besar untuk UI -> estimasi atau counter cache
```

Keyset pagination:
```sql
-- Halaman berikutnya: semua baris setelah kursor terakhir
SELECT id, created_at FROM orders
WHERE (created_at, id) < (:last_created_at, :last_id)
ORDER BY created_at DESC, id DESC
LIMIT 20;
```

## Acceptance Checklist
- [ ] `pg_stat_statements` aktif dan dipantau
- [ ] Setiap perbaikan query didahului EXPLAIN dan diikuti EXPLAIN
- [ ] Tidak ada index yang dibuat tanpa bukti dari query nyata
- [ ] Index yang tidak dipakai (pg_stat_user_indexes, idx_scan = 0) ditinjau dan dihapus
- [ ] Pagination di tabel besar memakai keyset, bukan OFFSET
- [ ] ANALYZE terjadwal setelah bulk load besar

## Kesalahan Umum / Pitfalls
- Menambah index untuk setiap keluhan lambat — index memperlambat write dan menumpuk.
- Membaca EXPLAIN tanpa ANALYZE — estimasi bisa jauh dari kenyataan.
- Index dengan kolom urutan salah — `(status, created_at)` tidak membantu filter `customer_id`.
- Menguji di dataset 1000 baris — planner memilih strategi berbeda di 10 juta baris.
- Mengabaikan statistik — setelah bulk import besar, planner mengambil keputusan dari data basi.

## Trade-off dan Kapan Tidak Pakai
- Setiap index mempercepat read tertentu dan memperlambat semua write di tabel itu — index hanya untuk query yang benar-benar berjalan.
- Covering index besar hampir separuh ukuran tabel — pertimbangkan trade-off terhadap cache.
- Partial index sangat efisien tapi rapuh terhadap perubahan pola query — review saat query berubah.
- Untuk analitik berat (scan ratusan juta baris), tuning query bukan jawabannya — pindahkan ke replica atau warehouse.

## Referensi
- https://www.postgresql.org/docs/current/sql-explain.html
- https://www.postgresql.org/docs/current/pgstatstatements.html
- https://use-the-index-luke.com/
- https://www.postgresql.org/docs/current/indexes-partial.html

---

*Dokumentasi ini bagian dari [AegisX Skills Collection](https://aegisxresearch.github.io/AegisX-Skills/). Dikelola oleh AegisX Research.*
