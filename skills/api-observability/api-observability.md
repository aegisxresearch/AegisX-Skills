# API Observability Engineering

## Goal
Turn API behavior into actionable signals without leaking sensitive data or creating noisy alerts.

## Three Signals
- **Rate:** requests, jobs, messages, and business operations per second.
- **Errors:** protocol errors, domain rejections, dependency failures, and timeouts.
- **Duration:** latency distributions, preferably p50/p95/p99 rather than averages.

Measure by route template and operation name, not raw URLs containing IDs.

## Structured Log
```json
{
  "timestamp": "2026-09-08T12:00:00.000Z",
  "level": "info",
  "message": "request completed",
  "service": "orders-api",
  "version": "2026.09.08.1",
  "trace_id": "abc123",
  "request_id": "req_456",
  "route": "POST /api/v1/orders",
  "status": 201,
  "duration_ms": 84
}
```
Never log passwords, tokens, full payment data, authorization headers, or unrestricted request bodies. Apply structured redaction before serialization.

## Trace Boundaries
Create a server span for each request and child spans for database, broker, cache, and external HTTP calls. Propagate W3C trace context only to trusted destinations and avoid accepting arbitrary trace baggage as a security decision.

## SLO Example
```yaml
service: orders-api
slos:
  availability:
    target: 99.9%
    window: 30d
  latency:
    target: 99%
    threshold_ms: 500
    window: 30d
```
Define whether 4xx responses count as errors based on user impact. Use burn-rate alerts that page only when the error budget is being consumed quickly.

## Metrics Hygiene
Bound label cardinality. Never use user ID, request ID, or arbitrary URL as a metric label. Use exemplars or trace links for drill-down.

## Health Endpoints
Separate liveness from readiness. Liveness should indicate whether the process can continue; readiness should reflect whether the instance can receive traffic. Do not make a deep dependency check a liveness probe.

## Incident Workflow
1. Detect an SLO-impacting signal.
2. Correlate release, route, dependency, and region.
3. Mitigate with rollback, feature flag, rate limit, or graceful degradation.
4. Preserve traces and representative logs.
5. Document root cause and corrective actions.

## Checklist
- [ ] Route templates and service versions are present.
- [ ] Logs are structured, correlated, and redacted.
- [ ] Traces cover external dependencies.
- [ ] Metrics have bounded cardinality.
- [ ] SLOs represent user-visible reliability.
- [ ] Readiness and liveness are distinct.
- [ ] Alerts have owners and runbooks.
- [ ] Retention and access controls meet privacy requirements.

## References
- https://opentelemetry.io/docs/concepts/observability-primer/
- https://sre.google/sre-book/service-level-objectives/
- https://prometheus.io/docs/practices/naming/
