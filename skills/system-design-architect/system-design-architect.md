# System Design Architect

## Overview
Panduan system design: architecture patterns, scalability, microservices, dan distributed systems.

---

## ️ Architecture Patterns

### Monolith
```text
┌─────────────────────────────────────────┐
│              MONOLITH                   │
│  ┌─────────┐  ┌─────────┐  ┌─────────┐ │
│  │  User   │  │  Order  │  │ Product │ │
│  │ Service │  │ Service │  │ Service │ │
│  └────┬────┘  └────┬────┘  └────┬────┘ │
│       └────────────┼────────────┘      │
│                    │                   │
│              ┌─────┴─────┐            │
│              │ Database  │            │
│              └───────────┘            │
└─────────────────────────────────────────┘
```

### Microservices
```text
┌──────────┐  ┌──────────┐  ┌──────────┐
│   User   │  │  Order   │  │ Product  │
│ Service  │  │ Service  │  │ Service  │
└────┬─────┘  └────┬─────┘  └────┬─────┘
     │             │             │
┌────┴─────┐  ┌────┴─────┐  ┌────┴─────┐
│ User DB  │  │ Order DB │  │Product DB│
└──────────┘  └──────────┘  └──────────┘
     │             │             │
     └─────────────┼─────────────┘
                   │
            ┌──────┴──────┐
            │   API       │
            │   Gateway   │
            └─────────────┘
```yaml

---

## Scalability Patterns

### Horizontal Scaling
```yaml
# Load Balancer
services:
  app:
    deploy:
      replicas: 3
    resources:
      limits:
        cpus: '1.0'
        memory: 1G
```

### Caching Strategy
```text
┌─────────┐     ┌─────────┐     ┌─────────┐
│  Client  │────▶│  `Redis`  │────▶│Database │
└─────────┘     │ (Cache) │     └─────────┘
                └─────────┘
                   │
              Cache Hit? 
              Yes → Return cached
              No → Query DB, cache result
```

### Database Scaling
```text
┌─────────────────────────────────────────┐
│              PRIMARY                    │
│           (Write Operations)            │
└─────────────────┬───────────────────────┘
                  │
        ┌─────────┼─────────┐
        ▼         ▼         ▼
   ┌─────────┐ ┌─────────┐ ┌─────────┐
   │ Replica │ │ Replica │ │ Replica │
   │   (R)   │ │   (R)   │ │   (R)   │
   └─────────┘ └─────────┘ └─────────┘
   (Read Operations)
```

---

## Message Queue Patterns

### Event-Driven Architecture
```text
┌─────────┐    ┌─────────┐    ┌─────────┐
│ Service │───▶│  Kafka  │───▶│ Service │
│   A     │    │ (Queue) │    │   B     │
└─────────┘    └─────────┘    └─────────┘
                   │
                   ▼
              ┌─────────┐
              │ Service │
              │   C     │
              └─────────┘
```

### Use Cases
| Pattern | Use Case | Example |
|---------|----------|---------|
| Pub/Sub | Notifications | User signs up → Send welcome email |
| Event Sourcing | Audit logs | Order placed → Store event |
| CQRS | Read/write separation | Heavy reads, light writes |

---

## ️ Resilience Patterns

### Circuit Breaker
```text
State Machine:
CLOSED ──(failure threshold)──▶ OPEN
  ▲                              │
  │                         (timeout)
  │                              │
  └──(success)──── HALF-OPEN ◀──┘
```python

### Retry with Backoff
```typescript
async function retryWithBackoff<T>(
  fn: () => Promise<T>,
  maxRetries: number = 3,
  baseDelay: number = 1000
): Promise<T> {
  for (let i = 0; i < maxRetries; i++) {
    try {
      return await fn()
    } catch (error) {
      if (i === maxRetries - 1) throw error
      await sleep(baseDelay * Math.pow(2, i))
    }
  }
  throw new Error('Max retries exceeded')
}
```

---

## System Design Checklist

### Requirements
- [ ] Functional requirements defined
- [ ] Non-functional requirements (latency, throughput)
- [ ] Scale estimates (QPS, storage)
- [ ] Data model designed

### Architecture
- [ ] Component diagram created
- [ ] API contracts defined
- [ ] Database schema designed
- [ ] Caching strategy defined

### Scalability
- [ ] Horizontal scaling plan
- [ ] Database replication strategy
- [ ] Load balancing configured
- [ ] CDN for static assets

### Resilience
- [ ] Circuit breakers implemented
- [ ] Retry logic with backoff
- [ ] Graceful degradation
- [ ] Monitoring and alerting

---

## Kesalahan Umum / Pitfalls

- Designing for scale before you have users — premature optimization.
- No circuit breaker — cascading failures.
- Synchronous calls between services — latency and coupling.
- Ignoring backpressure — slow consumers overflow queues.

## Trade-off dan Kapan Tidak Pakai

- Microservices add operational complexity — start monolith, split when needed.
- Queues add resilience but latency — use sync for low-latency paths.
- Caching improves speed but adds staleness — know your tolerance.

## References
- https://github.com/donnemartin/system-design-primer
- https://microservices.io/patterns/
- https://aws.amazon.com/architecture/

---

*Dokumentasi ini bagian dari [AegisX Skills Collection](https://aegisxresearch.github.io/AegisX-Skills/). Dikelola oleh AegisX Research.*
