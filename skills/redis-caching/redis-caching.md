# `Redis` Caching & Data Structures

## Goal
Use `Redis` for explicitly bounded, observable state with a clear consistency and failure policy.

## Cache-Aside
```typescript
async function getProduct(id: string): Promise<Product> {
  const key = `product:v1:${id}`;
  const cached = await redis.get(key);
  if (cached) return JSON.parse(cached) as Product;

  const product = await repository.findById(id);
  if (product) await redis.set(key, JSON.stringify(product), { EX: 300 });
  return product;
}
```
Define serialization version, TTL, negative-cache policy, invalidation trigger, and behavior when `Redis` is unavailable. Never let cache failure expose private data across tenants.

## Stampede Protection
Use jittered TTLs, request coalescing, stale-while-revalidate, or a narrowly scoped lock. A lock is not a replacement for database constraints and must have an expiry and owner token.

## Rate Limiting
Prefer atomic Lua scripts or server-side commands for increment-and-expire operations. Define identity, window, limits, clock behavior, and the response contract. Do not use unbounded keys from raw user input.

## Distributed Locks
`Redis` locks can coordinate best-effort work but do not automatically provide fencing or correctness under all network partitions. Use a database constraint or durable workflow for critical financial or security decisions.

## Memory and Persistence
Set max memory and an eviction policy intentionally. Distinguish cache nodes from durable data stores. Configure persistence, replication, backups, and recovery only when the data requires it.

## Security
Use TLS where needed, authentication/ACLs, private networking, key-prefix ownership, and payload minimization. Never expose `Redis` directly to the public internet.

## Monitoring
Track hit ratio, misses, evictions, memory fragmentation, command latency, connection saturation, replication lag, keyspace growth, and error rate.

## Checklist
- [ ] Every key has an owner, version, TTL, and bounded cardinality.
- [ ] Cache consistency and invalidation behavior are documented.
- [ ] Stampede and `Redis` outage behavior are tested.
- [ ] Critical operations do not rely solely on a lock.
- [ ] Memory and eviction policy are explicit.
- [ ] `Redis` is network-restricted and ACL-protected.
- [ ] Metrics cover hit rate, evictions, latency, and saturation.

## Kesalahan Umum / Pitfalls

- Cache-aside without TTL — stale data forever.
- Using Redis as a primary database — it is not durable by default.
- No connection pooling — connection exhaustion.
- Cache stampede — all requests miss at once and hit the DB.

## Trade-off dan Kapan Tidak Pakai

- Redis is fast but not a replacement for a real database — use it for cache/queue.
- Distributed locking with Redis is tricky — consider Redlock carefully.
- Cache invalidation is hard — prefer TTLs over explicit invalidation.

## References
- https://redis.io/docs/latest/develop/use/patterns/
- https://redis.io/docs/latest/develop/data-types/
- https://redis.io/docs/latest/operate/rs/security/

---

*Dokumentasi ini bagian dari [AegisX Skills Collection](https://aegisxresearch.github.io/AegisX-Skills/). Dikelola oleh AegisX Research.*
