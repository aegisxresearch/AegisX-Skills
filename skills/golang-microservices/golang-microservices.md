# Golang Microservices

## Tujuan

Merancang dan membangun microservices Go yang kecil, cepat, resilien, dan mudah diobservasi — menghindari monolith yang "terpecah" tanpa alasan.

## Prasyarat

- Dasar Go (goroutine, channel, interface)
- Konsep HTTP dan deployment

## Konsep inti

1. **Service boundary** — pecah berdasarkan domain dan beban, bukan berdasarkan tim. Mulai dari monolith modular; pisahkan saat ada alasan terukur.
2. **Transport** — REST via `net/http` atau `chi`; gRPC untuk komunikasi internal yang ketat; protobuf untuk kontrak.
3. **Concurrency** — `errgroup` untuk fan-out terbatas; jangan membuat goroutine tanpa batas (semaphore/worker pool).
4. **Resilience** — retry dengan backoff + jitter, timeout per request, circuit breaker (mis. `sony/gobreaker`), bulkhead.
5. **Observability** — OpenTelemetry tracing, structured slog logs, Prometheus metrics.
6. **Config** — `envconfig`/`env` + secrets dari vault; tidak ada config di binary.

## Contoh server HTTP minimal (illustrative)

```go
package main

import (
	"context"
	"log/slog"
	"net/http"
	"os"
	"os/signal"
	"syscall"
	"time"
)

func main() {
	srv := &http.Server{Addr: ":8080", Handler: routes(), ReadHeaderTimeout: 5 * time.Second}

	go func() {
		if err := srv.ListenAndServe(); err != nil && err != http.ErrServerClosed {
			slog.Error("server error", "err", err)
			os.Exit(1)
		}
	}()

	ctx, stop := signal.NotifyContext(context.Background(), syscall.SIGINT, syscall.SIGTERM)
	defer stop()
	<-ctx.Done()

	shutdownCtx, cancel := context.WithTimeout(context.Background(), 10*time.Second)
	defer cancel()
	_ = srv.Shutdown(shutdownCtx)
}
```

## Checklist produksi

- [ ] Timeout: server, client, dial — semuanya eksplisit
- [ ] Graceful shutdown menutup koneksi DB, consumer, dan server
- [ ] Structured logging (`slog`) dengan request id; tanpa log data PII
- [ ] Middleware: request id, recover, request logging, metrics
- [ ] Retry hanya untuk operasi idempotent; backoff + jitter
- [ ] Circuit breaker di sisi client untuk dependency kritis
- [ ] Health (`/healthz`) dan readiness terpisah
- [ ] Test: unit + integration (httptest), minimal 1 happy path + 2 edge case; `-race` di CI
- [ ] `go vet` + `staticcheck` di CI; dependensi di-audit

## Kesalahan umum

- Goroutine leak: goroutine tanpa context cancellation.
- `http.Client` tanpa timeout — hang selamanya.
- Mengembalikan stack trace/error internal ke klien.
- Retry tanpa idempotency menghasilkan duplikat efek.
- Membuat microservice baru untuk setiap fungsi kecil.

## Referensi

- https://pkg.go.dev/net/http — server HTTP standar
- https://grpc.io/docs/languages/go/ — gRPC-Go
- https://github.com/uber-go/guide — style guide
- https://opentelemetry.io/docs/languages/go/ — observability