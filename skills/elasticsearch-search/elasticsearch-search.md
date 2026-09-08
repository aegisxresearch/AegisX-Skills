# `Elasticsearch` & Search Engines

## Tujuan

Membangun fitur pencarian yang cepat dan relevan dengan `Elasticsearch`/OpenSearch: mapping yang benar, analysis yang sesuai bahasa, query yang efisien, tuning relevansi, dan cluster yang terpelihara.

## Prasyarat

- Dasar REST dan JSON
- Konsep inverted index

## Konsep inti

1. **Inverted index** — dokumen dipecah menjadi token; pencarian = lookup token. Mapping menentukan bagaimana field di-index.
2. **Analysis** — `analyzer` (standard, ik, ngram, dll) + `normalizer`. Pilih analyzer sesuai bahasa konten. `search_analyzer` bisa berbeda dari `index_analyzer`.
3. **Mapping** — tetapkan tipe field sejak awal (index mapping immutable); `text` vs `keyword`, `date`, `geo_point`, `nested` (bukan `object` untuk array objek yang perlu query terpisah).
4. **Query DSL** — `match` (full-text) vs `term` (exact); `bool` (must/should/filter/must_not); `filter` memanfaatkan cache, tidak memengaruhi score.
5. **Relevance** — BM25 default; boost field, `function_score`, synonyms; evaluasi dengan metrics (precision/recall, click-through) bukan intuisi.
6. **Indexing pipeline** — sinkronkan dari source (CDC/queue); alias untuk zero-downtime reindex; `refresh_interval` diperlonggar saat bulk.
7. **Operasional** — shard sizing (20-50GB per shard), replicas, ILM untuk lifecycle, snapshot backup, monitor heap/disk.

## Contoh (illustrative)

```json
{
  "mappings": {
    "properties": {
      "title": { "type": "text", "analyzer": "standard" },
      "tags": { "type": "keyword" },
      "published_at": { "type": "date" },
      "comments": { "type": "nested" }
    }
  }
}
```

```json
{
  "query": {
    "bool": {
      "must": [{ "match": { "title": "flutter offline" } }],
      "filter": [{ "term": { "status": "published" } }]
    }
  }
}
```

## Checklist produksi

- [ ] Mapping eksplisit (bukan dynamic mapping mentah) untuk field penting
- [ ] Analyzer sesuai bahasa; synonym dict terkelola bila relevan
- [ ] Query pakai `filter` untuk kondisi yang tidak butuh scoring
- [ ] Pagination via `search_after` untuk deep page (bukan `from` besar)
- [ ] Reindex lewat alias; downtime minimal
- [ ] Monitoring: shard health, heap, disk, slow query log
- [ ] Snapshot rutin + restore pernah diuji
- [ ] Test relevansi: golden set query → dokumen relevan; regression di CI

## Kesalahan umum

- `wildcard`/`regexp` di depan pola — scan mahal.
- `from` besar (deep pagination) — menggantung cluster.
- Mapping `nested` tidak dipakai untuk array objek → hasil query salah.
- Shard terlalu kecil/banyak — overhead; terlalu besar — lambat recover.
- Relevance tanpa evaluasi — tuning berdasarkan perasaan.

## Trade-off dan Kapan Tidak Pakai

- `Elasticsearch` is powerful but operationally heavy — consider managed search.
- Keyword vs full-text — know which field type fits each query.
- Reindexing is disruptive — plan for downtime or use aliases.

## Referensi

- https://www.elastic.co/docs/ — dokumentasi resmi
- https://opensearch.org/docs/latest/ — OpenSearch
- https://www.elastic.co/guide/en/elasticsearch/reference/current/query-dsl.html — Query DSL

---

*Dokumentasi ini bagian dari [AegisX Skills Collection](https://aegisxresearch.github.io/AegisX-Skills/). Dikelola oleh AegisX Research.*
