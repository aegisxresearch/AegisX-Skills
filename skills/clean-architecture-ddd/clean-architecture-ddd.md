# Clean Architecture & DDD

## Tujuan

Menerapkan Clean Architecture dan DDD untuk domain yang kompleks: model domain yang mencerminkan bisnis, dependensi mengalir ke dalam, dan teknologi (framework/DB) menjadi detail yang bisa diganti.

## Prasyarat

- Pengalaman membangun aplikasi nyata
- Familiar dengan OOP/fungsional dan testing

## Konsep inti

1. **Kapan memakai** — DDD/Clean Architecture berguna saat domain kompleks dan aturan bisnis berubah. Untuk CRUD sederhana, arsitektur berlapis ringan lebih murah. Jangan dogmatis.
2. **Ubiquitous language** — istilah bisnis dipakai konsisten di kode, dokumen, dan percakapan. Model domain memakai bahasa ini.
3. **Bounded context** — batas model per konteks bisnis (mis. "Sales" vs "Shipping"). Antara konteks: contract/API, bukan berbagi model internal.
4. **Entity & Value Object** — entity punya identitas dan lifecycle; value object tidak (dibandingkan berdasarkan nilai). Buat value objects untuk money, date range, dll.
5. **Dependency rule** — dependensi source code hanya menunjuk ke dalam: `domain ← application ← infrastructure/interface`. Framework dan DB di lapisan terluar.
6. **Ports & Adapters** — domain/application mendefinisikan interface (port); infra mengimplementasikan adapter (repo, email, payment).
7. **Aggregate** — kelompok entity yang konsisten secara transaksional; akses dari luar lewat aggregate root.

## Contoh (illustrative)

```python
# domain — tanpa dependensi framework
class Money:
    def __init__(self, amount: int, currency: str):
        if amount < 0:
            raise ValueError("amount must be non-negative")
        self.amount = amount
        self.currency = currency

    def add(self, other: "Money") -> "Money":
        if self.currency != other.currency:
            raise ValueError("currency mismatch")
        return Money(self.amount + other.amount, self.currency)

# application port
class OrderRepository(Protocol):
    def save(self, order: "Order") -> None: ...
    def find_by_id(self, order_id: str) -> "Order | None": ...

# infrastructure adapter
class SqlOrderRepository(OrderRepository):
    def save(self, order):
        self.session.add(OrderRow.from_domain(order))
```

## Checklist produksi

- [ ] Ubiquitous language konsisten; istilah domain tidak diterjemahkan sembarangan
- [ ] Lapisan terpisah: domain, application, infrastructure; framework tidak bocor ke domain
- [ ] Entity vs value object diputuskan eksplisit
- [ ] Aggregate root membatasi mutasi internal
- [ ] Port didefinisikan di dalam; adapter di luar
- [ ] Test domain murni (tanpa framework); test application dengan port di-mock
- [ ] Transaction/consistency boundary sesuai aggregate, bukan satu transaksi raksasa
- [ ] Kompleksitas arsitektur sebanding kompleksitas domain (tidak over-engineered)

## Kesalahan umum

- Menerapkan DDD untuk CRUD sederhana — biaya arsitektur > manfaat.
- Framework merembes ke domain (mis. entity menurunkan ORM class).
- Satu "model" global untuk semua konteks — bounded context diabaikan.
- Repository "generic" untuk semua entity tanpa alasan.
- Anemic domain: semua logic di service, domain hanya data container.

## Trade-off dan Kapan Tidak Pakai

- DDD shines in complex domains — skip it for simple CRUD.
- Ports & adapters add indirection — worth it for testability of core logic.
- Event-driven DDD is powerful but hard to debug — start with commands/queries.

## Referensi

- https://blog.cleancoder.com/uncle-bob/2012/08/13/the-clean-architecture.html — Clean Architecture
- https://martinfowler.com/tags/domain%20driven%20design.html — DDD (Fowler)
- https://www.dddcommunity.org/ — komunitas DDD

---

*Dokumentasi ini bagian dari [AegisX Skills Collection](https://aegisxresearch.github.io/AegisX-Skills/). Dikelola oleh AegisX Research.*
