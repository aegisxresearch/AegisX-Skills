# Prometheus Alerting & SLO Design

## Goal
Setiap alert yang berbunyi merepresentasikan pembakaran error budget yang nyata — dan memang ada orang yang wajib meresponnya. Tidak ada alert kosmetik di tengah malam.

## Operating Model
```text
Definisikan SLI -> tetapkan SLO -> hitung error budget
-> alert berdasarkan burn rate -> route ke on-call -> review tiap kejadian
```

## Konsep Inti

### 1. SLI yang jujur
Ukur dari sudut pandang pengguna, bukan mesin:
```text
Availability SLI: ratio request HTTP 5xx terhadap semua request
Latency SLI:      ratio request di bawah threshold (mis. < 300ms)
Freshness SLI:    ratio data yang lebih baru dari X (untuk pipeline)
```

### 2. SLO dan error budget
```text
SLO 99.9% availability per 28 hari
Error budget = 0.1% dari request dalam 28 hari
             = boleh gagal ~20 menit penuh traffic
```

### 3. Multi-window burn rate
Burn rate = seberapa cepat error budget terbakar relatif terhadap jadwal. Pola standar (Google SRE Workbook, bab 5):

```yaml
# Page: budget terbakar >14.4x dalam 1 jam DAN >14.4x dalam 5 menit
# -> jika terus, 2% budget habis dalam 1 jam; butuh respons segera
- alert: SLOBurnRateFast
  expr: |
    (
      sum(rate(http_requests_total{code=~"5.."}[1h]))
      /
      sum(rate(http_requests_total[1h]))
    ) > (14.4 * 0.001)
    and
    (
      sum(rate(http_requests_total{code=~"5.."}[5m]))
      /
      sum(rate(http_requests_total[5m]))
    ) > (14.4 * 0.001)
  for: 2m
  labels: { severity: page }

# Ticket: 6x dalam 6 jam DAN 6x dalam 30 menit -> hari kerja
- alert: SLOBurnRateSlow
  expr: |
    (
      sum(rate(http_requests_total{code=~"5.."}[6h]))
      /
      sum(rate(http_requests_total[6h]))
    ) > (6 * 0.001)
    and
    (
      sum(rate(http_requests_total{code=~"5.."}[30m]))
      /
      sum(rate(http_requests_total[30m]))
    ) > (6 * 0.001)
  labels: { severity: ticket }
```

Dua window mencegah dua kegagalan klasik: alert dari spike 1 menit yang sudah selesai (window pendek saja) dan alert yang baru berbunyi setelah budget habis (window panjang saja).

### 4. Latency dari histogram
```promql
# P99: kuantil dari histogram bucket
histogram_quantile(0.99,
  sum(rate(http_request_duration_seconds_bucket[5m])) by (le)
)
```

### 5. Routing yang masuk akal (Alertmanager)
```yaml
route:
  receiver: oncall
  group_by: [alertname, service]
  group_wait: 30s
  group_interval: 5m
  repeat_interval: 4h
routes:
  - matchers: [severity="ticket"]
    receiver: ticket-queue      # tidak membangunkan siapa pun
receivers:
  - name: oncall
    pagerduty_configs: [{ routing_key: "<secret>" }]
```

## Acceptance Checklist
- [ ] Setiap service kritis punya SLO availability dan/atau latency tertulis
- [ ] Alert page memakai multi-window multi-burn-rate, bukan threshold tunggal
- [ ] Tidak ada alert page tanpa runbook (link di annotasi alert)
- [ ] Alert ticket diarahkan ke antrean, bukan pager
- [ ] Tingkat kesehatan alerting terukur: berapa % alert yang di-acknowledge dan actionable
- [ ] Error budget dibahas di review, bukan hanya uptime

## Kesalahan Umum / Pitfalls
- Alert pada CPU/memori tinggi — gejala, bukan dampak pengguna; biasanya selesai sendiri.
- Threshold tunggal (mis. error > 1% selama 5m) — kacau di traffic rendah, telat di traffic tinggi.
- `for: 0s` — alert berbunyi untuk spike sesaat yang tidak pernah terlihat pengguna.
- Alert tanpa runbook — on-call menebak di jam 3 pagi.
- Menambah alert setiap insiden tanpa pernah menghapus — pager jadi spam, alert nyata tenggelam.

## Trade-off dan Kapan Tidak Pakai
- Multi-window menambah kompleksitas rule — untuk service kecil dengan traffic stabil, satu window panjang bisa cukup.
- SLO per endpoint memecah fokus — mulai dari SLO service-level, per endpoint hanya jika kritis.
- Error budget 99.99% hampir selalu terlalu ketat untuk aplikasi biasa — mulai 99.9% dan ukur.
- Untuk batch job, burn-rate HTTP tidak cocok — alertkan freshness dan success rate job.

## Referensi
- https://sre.google/workbook/implementing-service-level-objectives/
- https://prometheus.io/docs/prometheus/latest/querying/basics/
- https://prometheus.io/docs/alerting/latest/configuration/
- https://cloud.google.com/architecture/-alerting-on-slos

---

*Dokumentasi ini bagian dari [AegisX Skills Collection](https://aegisxresearch.github.io/AegisX-Skills/). Dikelola oleh AegisX Research.*
