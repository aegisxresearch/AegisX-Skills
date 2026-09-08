# Observability: Prometheus & Grafana

## Tujuan

Membangun observability yang menjawab "apakah sistem sehat dan seberapa baik SLA" — metrik yang tepat, alerting yang tidak berisik, dashboard yang berguna, dan SLO yang terukur.

## Prasyarat

- Dasar HTTP service dan Linux
- Konsep monitoring dasar

## Konsep inti

1. **RED/USE** — RED untuk request-driven service: Rate, Errors, Duration. USE untuk resource: Utilization, Saturation, Errors. Mulai dari sini, tambah yang spesifik.
2. **Metrik aplikasi** — expose `/metrics` Prometheus; gunakan client library resmi (prometheus-client, prom-client, micrometer). Label terbatas dan bernilai rendah-kardinalitas.
3. **Service discovery & scraping** — scrape target dari Kubernetes annotations/labels; jangan scrape dari jaringan publik tanpa auth.
4. **PromQL** — `rate()` untuk counter, histogram untuk latency (p50/p95/p99), `increase` untuk delta. Hindari query tanpa bounding range.
5. **Alerting** — alert harus actionable: severity jelas, runbook terhubung, tidak ada alert yang selalu merah ("alert fatigue"). Gunakan `for` untuk menghindari flapping.
6. **SLO** — target berdasarkan error budget: misal 99.9% availability/bulan. Hitung burn rate; alert saat error budget habis lebih cepat dari laju.
7. **Dashboard** — Grafana: per service view (RED), dependency view, dan SLO view. Jangan buat dashboard tanpa pertanyaan yang jelas.

## Contoh PromQL (illustrative)

```promql
# HTTP error ratio per 5 menit
sum(rate(http_requests_total{status=~"5.."}[5m]))
  / sum(rate(http_requests_total[5m]))

# p95 latency
histogram_quantile(0.95, sum(rate(http_request_duration_seconds_bucket[5m])) by (le))
```

## Checklist produksi

- [ ] `/metrics` ada di semua service; metrik RED tercakup
- [ ] Label berkardinalitas rendah; tanpa label user id/request id di metrik
- [ ] Histogram bucket sesuai latensi aktual
- [ ] Alert rules: setiap alert punya severity + runbook; `for` di-set
- [ ] Test alerting (dead man's switch / amot) agar saluran tidak mati senyap
- [ ] SLO didefinisikan; burn rate alert aktif
- [ ] Dashboard per service + SLO; diskrit dan mudah dibaca
- [ ] Retention dan downsampling sesuai kebutuhan; biaya penyimpanan terkendali

## Kesalahan umum

- Alert yang selalu merah → diabaikan semua orang.
- Metrik label kardinalitas tinggi → Prometheus membengkak.
- Hanya uptime, tanpa error rate dan latency — mati "pelan-pelan" tak terlihat.
- Dashboard penuh panel tanpa konteks — tidak menjawab pertanyaan apa pun.
- SLO tanpa error budget — target "100%" tidak realistis.

## Referensi

- https://prometheus.io/docs/ — dokumentasi Prometheus
- https://grafana.com/docs/ — Grafana
- https://promlabs.com/promql-cheat-sheet/ — kuis PromQL
- https://sre.google/sre-book/service-level-objectives/ — SRE book SLO