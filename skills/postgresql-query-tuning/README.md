# PostgreSQL Query Tuning

> **Kategori:** Database dan Data Engineering | **Level:** Intermediate-Advanced

Panduan tuning query PostgreSQL: membaca EXPLAIN, memilih index yang tepat, dan mengukur dampaknya dengan data nyata.

## Yang Dipelajari
- Membaca EXPLAIN (ANALYZE, BUFFERS) tanpa menebak
- Index scan vs seq scan: kapan masing-masing benar
- Composite index, covering index, dan partial index
- Statistik planner dan kapan ANALYZE perlu dijalankan
- Pola query yang selalu lambat: N+1, OFFSET dalam, LIKE dengan wildcard depan

## Production Outcome
Query lambat diidentifikasi dari `pg_stat_statements`, dianalisis dengan EXPLAIN, dan diperbaiki dengan index yang terukur dampaknya — bukan dengan menambah index setiap kali ada keluhan.

## File
[`postgresql-query-tuning.md`](./postgresql-query-tuning.md) — Panduan lengkap

---

*Dokumentasi ini bagian dari [AegisX Skills Collection](https://aegisxresearch.github.io/AegisX-Skills/). Dikelola oleh AegisX Research.*
