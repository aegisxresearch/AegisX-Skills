# OpenTelemetry Distributed Tracing

## Goal
Setiap request yang melintasi lebih dari satu service harus bisa diikuti lewat satu trace ID — dari ingress sampai query database — tanpa logging manual di setiap hop.

## Operating Model
```text
Client -> Ingress -> Service A -> Service B -> Database
   |          |           |           |          |
   +----------+-----------+-----------+----------+
                satu trace ID, span per hop
```

## Konsep Inti

### Trace, Span, Context
```text
Trace   = pohon span untuk satu request
Span    = satu unit kerja dengan waktu mulai/akhir + atribut
Context = metadata (trace ID, span ID) yang dipropagasi antar service
```

Propagasi standar adalah W3C Trace Context: header `traceparent` dan `tracestate`. Semua SDK utama mendukungnya; jangan pakai propagator vendor-proprietary kecuali semua hop mengertinya.

### Instrumentasi: otomatis vs manual
```text
Otomatis: HTTP server/client, gRPC, banyak DB driver — cukup untuk 80% kasus
Manual:   logika bisnis penting, batch job, consumer queue
```

Contoh span manual di Python:
```python
from opentelemetry import trace

tracer = trace.get_tracer(__name__)

def process_order(order_id: str) -> None:
    with tracer.start_as_current_span("process_order") as span:
        span.set_attribute("order.id", order_id)
        validate(order_id)      # otomatis tercatat di dalam span ini
        charge_payment(order_id)
```

### Sampling: menjaga biaya
```text
Head-based: keputusan di awal request — hemat, tapi bisa kehilangan trace error
Tail-based: keputusan di akhir — simpan semua error/slow, buang sisanya
```

Produksi umumnya: head sampling 1-10% + `ParentBased` agar keputusan konsisten antar hop, lalu tail sampling di collector untuk menyimpan 100% trace error dan latency tinggi.

### Export dan collector
```yaml
# otel-collector-config.yaml (fragment)
receivers:
  otlp:
    protocols:
      grpc: { endpoint: 0.0.0.0:4317 }
processors:
  tail_sampling:
    decision_wait: 10s
    policies:
      - name: errors
        type: status_code
        status_code: { status_codes: [ERROR] }
      - name: probabilistic
        type: probabilistic
        probabilistic: { sampling_percentage: 5 }
exporters:
  otlp/tempo:
    endpoint: tempo:4317
```

Aplikasi mengirim ke collector (bukan langsung ke backend) agar kebijakan sampling dan routing bisa berubah tanpa redeploy aplikasi.

### Korelasi dengan log dan metrics
Suntikkan trace ID ke log:
```python
logger.info("order processed", extra={"trace_id": trace.get_current_span().get_span_context().trace_id})
```
Dengan itu, dari satu log error bisa langsung lompat ke trace lengkapnya. Di sisi metrics, resource attributes (`service.name`, `deployment.environment`) harus konsisten di semua service.

## Acceptance Checklist
- [ ] Semua service mengirim trace ke collector OTLP
- [ ] `traceparent` dipropagasi lintas service (cek satu request end-to-end)
- [ ] Sampling menyimpan 100% trace error
- [ ] Trace ID muncul di log error
- [ ] `service.name` dan environment konsisten di semua service
- [ ] Latency p99 per hop terlihat di backend tracing

## Kesalahan Umum / Pitfalls
- Sampling head-based tanpa `ParentBased` — setiap hop memutuskan sendiri, trace putus-putus.
- Span per fungsi kecil — banjir span membuat trace tidak terbaca dan mahal.
- Atribut bernilai tinggi kardinalitas (user ID di nama span) — backend tracing melambat.
- Tidak menutup span saat error — error path tidak terukur.
- Mengirim trace langsung ke vendor tanpa collector — kebijakan sampling terkunci di kode.

## Trade-off dan Kapan Tidak Pakai
- Tracing penuh menambah latency dan biaya — sampling adalah wajib, bukan opsional.
- Untuk monolith kecil, tracing sering berlebihan — structured logging dengan request ID cukup.
- Tail sampling butuh buffer memori di collector — ukur dan kapasitasnya sebelum menaikkan traffic.
- Vendor SaaS cepat dipakai tapi mahal di skala besar — self-host (Jaeger/Tempo) untuk volume tinggi.

## Referensi
- https://opentelemetry.io/docs/concepts/signals/traces/
- https://www.w3.org/TR/trace-context/
- https://opentelemetry.io/docs/collector/
- https://grafana.com/docs/tempo/latest/

---

*Dokumentasi ini bagian dari [AegisX Skills Collection](https://aegisxresearch.github.io/AegisX-Skills/). Dikelola oleh AegisX Research.*
