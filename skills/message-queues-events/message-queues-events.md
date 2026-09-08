# Message Queues & Event-Driven Systems

## Goal
Use asynchronous messaging to decouple work while making delivery, failure, and replay behavior explicit.

## Choose the Primitive
- **Command:** asks one consumer to perform work.
- **Event:** records that something happened and may have many consumers.
- **Queue:** distributes work among competing consumers.
- **Pub/sub:** fans out an event to independent subscribers.

Do not introduce a broker solely to hide slow code. Define the latency, durability, ordering, and replay requirements first.

## Event Contract
```json
{
  "id": "evt_01J...",
  "type": "order.created",
  "version": 1,
  "occurred_at": "2026-09-08T12:00:00Z",
  "producer": "order-service",
  "trace_id": "trace_123",
  "data": { "order_id": "ord_123", "customer_id": "cus_456" }
}
```
Use stable identifiers, UTC timestamps, schema versions, and an explicit ownership policy. Avoid publishing secrets or mutable snapshots without a reason.

## Delivery Semantics
Most systems provide at-least-once delivery. Consumers must be idempotent:

```sql
CREATE TABLE processed_messages (
  consumer_name TEXT NOT NULL,
  message_id TEXT NOT NULL,
  processed_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
  PRIMARY KEY (consumer_name, message_id)
);
```
Record processing atomically with the business state where possible. For external side effects, use idempotency keys and reconciliation.

## Transactional Outbox
Write the domain change and an outbox row in one database transaction. A publisher reads pending rows, publishes them, and marks them delivered. This avoids the dual-write gap between database commit and broker publish.

## Retries and Dead Letters
Retry transient failures with exponential backoff and jitter. Do not retry validation, authorization, or permanent schema errors. Add a maximum attempt count, preserve the original error category, and route exhausted messages to a dead-letter queue with an operator workflow.

## Ordering and Partitioning
Ordering usually exists only within a partition or key. Choose a key that preserves the domain ordering requirement without creating a hot partition. Document whether consumers may process events concurrently.

## Schema Evolution
Prefer additive changes. Consumers must tolerate unknown fields and, during migration, both old and new versions. Run compatibility checks in CI and retain old versions until all consumers migrate.

## Observability
Track publish failures, consumer lag, age of oldest message, throughput, retry rate, DLQ size, processing duration, and business outcome. Propagate trace context and include message IDs in logs.

## Checklist
- [ ] Command/event semantics are clear.
- [ ] Ownership and schema compatibility are documented.
- [ ] Consumers are idempotent.
- [ ] Retryable and permanent errors are separated.
- [ ] DLQ replay has a safe runbook.
- [ ] Outbox or equivalent dual-write protection exists.
- [ ] Partition/order guarantees are tested.
- [ ] Lag, retries, and DLQ metrics have alerts.

## References
- https://microservices.io/patterns/data/transactional-outbox.html
- https://www.asyncapi.com/docs
- https://martinfowler.com/articles/201701-event-driven.html
