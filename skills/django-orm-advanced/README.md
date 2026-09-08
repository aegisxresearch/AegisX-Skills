# Django ORM Advanced Patterns

> **Kategori:** Database dan Data Engineering | **Level:** Intermediate-Advanced

Panduan pola Django ORM tingkat lanjut: select_related/prefetch_related, F expressions, transactions, dan menghindari N+1.

## Yang Dipelajari
- QuerySet lazy evaluation dan kapan query benar-benar dijalankan
- select_related vs prefetch_related vs Subquery
- F() dan Q() expressions untuk update atomik dan query kompleks
- select_for_update dan transaction.atomic untuk konsistensi
- Custom managers, expressions, dan denormalisasi yang terkendali

## Production Outcome
Aplikasi Django dengan query count yang terukur per halaman, tanpa N+1 tersembunyi, dan operasi stok/saldo yang aman terhadap race condition.

## File
[`django-orm-advanced.md`](./django-orm-advanced.md) — Panduan lengkap

---

*Dokumentasi ini bagian dari [AegisX Skills Collection](https://aegisxresearch.github.io/AegisX-Skills/). Dikelola oleh AegisX Research.*
