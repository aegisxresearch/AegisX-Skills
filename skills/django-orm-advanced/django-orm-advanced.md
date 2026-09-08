# Django ORM Advanced Patterns

## Goal
Query Django yang efisien secara default: jumlah query per halaman stabil, operasi konkuren aman, dan ORM mempercepat pengembangan tanpa memperlambat produksi.

## Operating Model
```text
Tulis query -> ukur (connection.queries / django-debug-toolbar)
-> hilangkan N+1 -> kunci race condition -> uji ulang
```

## Konsep Inti

### 1. N+1 dan solusinya
```python
# BURUK: 1 + N query (author di-query per buku)
for book in Book.objects.all():
    print(book.author.name)

# BAIK - foreign key: JOIN dalam 1 query
books = Book.objects.select_related("author")

# BAIK - reverse/m2m: 2 query total
authors = Author.objects.prefetch_related("books")
for author in authors:
    author.books.all()   # dari prefetch cache, bukan query baru
```

### 2. F expressions: update atomik
```python
from django.db.models import F

# Race-safe: increment dihitung di database
Product.objects.filter(pk=pk).update(stock=F("stock") - quantity)
```
`F()` mencegah read-modify-write klasik yang hilang update saat dua request bersamaan.

### 3. Konsistensi dengan select_for_update
```python
from django.db import transaction

@transaction.atomic
def transfer(from_acc, to_acc, amount):
    src = Account.objects.select_for_update().get(pk=from_acc)
    dst = Account.objects.select_for_update().get(pk=to_acc)
    if src.balance < amount:
        raise InsufficientFunds
    src.balance -= amount
    dst.balance += amount
    src.save()
    dst.save()
```
Selalu kunci dalam urutan ID yang konsisten untuk menghindari deadlock; `select_for_update` butuh transaksi aktif.

### 4. Q objects untuk logika kompleks
```python
from django.db.models import Q

# (status='new' AND priority__gte=5) OR assigned_to=me
Ticket.objects.filter(
    Q(status="new", priority__gte=5) | Q(assigned_to=request.user)
)
```

### 5. Mengukur, bukan menduga
```python
from django.db import connection, reset_queries
import time

reset_queries()
start = time.perf_counter()
report = build_dashboard(user)
print(f"{len(connection.queries)} queries, {time.perf_counter()-start:.3f}s")
```
Di development, `django-debug-toolbar` menampilkan hal yang sama per request. Di test, `assertNumQueries` menjaga regresi:
```python
def test_dashboard_query_count(self):
    with self.assertNumQueries(4):
        self.client.get("/dashboard/")
```

## Acceptance Checklist
- [ ] Tidak ada loop yang mengakses atribut FK/reverse tanpa select_related/prefetch_related
- [ ] Update counter/saldo memakai F(), bukan read-modify-write
- [ ] Operasi multi-step terhadap saldo/stok dibungkus atomic + select_for_update
- [ ] assertNumQueries menjaga query count di test untuk halaman kritis
- [ ] Prefetch_related dipanggil dengan Prefetch() dan queryset terfilter bila hanya subset yang dipakai

## Kesalahan Umum / Pitfalls
- `prefetch_related` tanpa filter — memuat seluruh tabel relasi saat hanya 10 objek dipakai.
- `.exists()` diikuti `.get()` — dua query untuk satu pengecekan; pakai try/get saja.
- Memanggil `.all()` berulang di template — setiap pemanggilan bisa jadi query baru tanpa prefetch.
- `select_for_update` di luar transaksi — Django melempar error atau lock tidak efektif.
- Mempercayai jumlah query di development dengan data kecil — profil dengan volume data mirip produksi.

## Trade-off dan Kapan Tidak Pakai
- select_related membuat satu JOIN besar — untuk relasi multi-level atau kolom banyak, prefetch terpisah bisa lebih cepat.
- Denormalisasi (counter cache) mempercepat read dengan biaya sinkronisasi — hanya untuk read path yang benar-benar panas.
- Raw SQL kadang jauh lebih cepat untuk agregasi kompleks — tapi kehilangan safety dan portability ORM; dokumentasikan.
- Untuk dataset analitik besar, ORM bukan alat yang tepat — ekspor ke warehouse.

## Referensi
- https://docs.djangoproject.com/en/stable/topics/db/optimization/
- https://docs.djangoproject.com/en/stable/ref/models/querysets/#select-for-update
- https://docs.djangoproject.com/en/stable/ref/models/expressions/
- https://django-debug-toolbar.readthedocs.io/

---

*Dokumentasi ini bagian dari [AegisX Skills Collection](https://aegisxresearch.github.io/AegisX-Skills/). Dikelola oleh AegisX Research.*
