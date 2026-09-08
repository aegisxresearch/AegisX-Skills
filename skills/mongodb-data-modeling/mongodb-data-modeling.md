# MongoDB Data Modeling

## Tujuan

Merancang schema MongoDB yang cepat dan scalable: model dokumen yang cocok dengan pola akses aplikasi, bukan meniru schema relasional, dengan index dan aggregation yang tepat.

## Prasyarat

- Dasar database dan query
- Familiar dengan JSON

## Konsep inti

1. **Document model** — data disimpan sebagai dokumen BSON. Model mengikuti pola akses (query + update), bukan normalisasi relasional.
2. **Embed vs Reference**:
   - Embed: data selalu diakses bersama, ukuran terbatas, tidak berubah sendiri (contoh: item di order, alamat).
   - Reference: data besar, diakses banyak dokumen, berubah sering (contoh: user, product).
3. **Pola umum**:
   - *Extended Reference* — denormalisasi sebagian (copy field ringkas) untuk menghindari join mahal.
   - *Outlier* — simpan field jarang di dokumen terpisah agar dokumen utama kecil.
   - *Bucket* — data time-series dikelompokkan per interval.
4. **Design untuk query** — tentukan query utama, lalu pilih model; hindari query yang memaksa scan seluruh koleksi.
5. **Indexes** — B-tree; `compound index` mengikuti pola query (equality → sort → range); TTL index untuk data kedaluwarsa; unique index untuk jaminan unik.
6. **Aggregation** — `$match` sedini mungkin; hindari `$lookup` bila model bisa di-embed; batasi `$unwind`.

## Contoh pola (illustrative)

```javascript
// Embedded — order menyimpan snapshot item (harga pada saat pembelian)
{
  _id: ObjectId("..."),
  userId: ObjectId("..."),
  total: 259000,
  items: [
    { sku: "A-100", name: "Keyboard", qty: 1, price: 259000 }
  ],
  createdAt: ISODate("2026-09-08T00:00:00Z")
}
```

```javascript
// Index compound untuk query umum
db.orders.createIndex({ userId: 1, createdAt: -1 });
```

## Checklist produksi

- [ ] Model mengikuti pola akses (query nyata aplikasi)
- [ ] Embed/reference diputuskan dengan alasan tertulis (ukuran, frekuensi akses)
- [ ] Index untuk semua query produksi; `explain("executionStats")` dicek
- [ ] Dokumen tidak tumbuh tanpa batas (cap array, arsip data lama)
- [ ] Unique index untuk natural key; TTL untuk data sementara
- [ ] Data yang perlu konsistensi transaksional memakai `withTransaction` bila multi-dokumen
- [ ] Test: unit (pola akses), integration (mongo-memory-server), query plan review
- [ ] Backup + point-in-time recovery; monitoring (Atlas/ops manager)

## Kesalahan umum

- Meniru schema SQL 1:1 — banyak `$lookup` dan dokumen kecil.
- Embed array yang tumbuh tak terbatas (16MB limit dan fragmentasi).
- Tanpa index — collection scan pada data besar.
- Menaruh data sensitif tanpa enkripsi field.
- Mengandalkan `$lookup` untuk join yang sebenarnya bisa di-embed.

## Referensi

- https://www.mongodb.com/docs/manual/data-modeling/ — panduan resmi
- https://www.mongodb.com/docs/manual/core/indexes/ — indexing
- https://www.mongodb.com/docs/manual/aggregation/ — aggregation