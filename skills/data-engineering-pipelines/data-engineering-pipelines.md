# Data Engineering Pipelines

## Goal
Move trusted data predictably while preserving correctness, lineage, freshness, and the ability to recover from partial failure.

## Batch and Streaming
Use batch for bounded latency and simpler recomputation. Use streaming when freshness or event-driven behavior justifies operational complexity. Many systems benefit from a batch backfill path even when serving is streaming.

## Data Contract
```yaml
name: order-events
owner: commerce-platform
version: 2
fields:
  order_id: { type: string, required: true }
  occurred_at: { type: timestamp, required: true }
  total_cents: { type: integer, required: true, minimum: 0 }
compatibility: backward
```
Contracts should define semantics, units, time zone, nullability, quality expectations, and ownership.

## Idempotent Processing
Use a stable source event ID or business key. Write outputs with merge/upsert semantics, partition by a deterministic key, and record checkpoints only after output is durable. Retries must not double-count metrics or append duplicate facts.

## Incremental Loads
Track a watermark, account for late-arriving data, and define a correction window. Backfills must be isolated, observable, and safe to run alongside normal ingestion.

## Quality Checks
Validate freshness, volume, uniqueness, referential integrity, accepted values, distribution changes, and null rates. Fail closed for critical tables and quarantine malformed records with reason codes.

## Lineage and Privacy
Record source-to-output lineage and classify sensitive fields. Minimize copies of personal data, apply retention, encryption, access controls, and deletion propagation.

## Observability
Track run status, duration, input/output row counts, freshness, lag, rejected records, checkpoint, and cost. Alert based on downstream impact and SLOs.

## Recovery Runbook
1. Stop or isolate affected consumers.
2. Identify last valid checkpoint and data interval.
3. Preserve bad inputs and error samples.
4. Fix transform or source contract.
5. Replay idempotently.
6. Reconcile counts and business totals.
7. Document impact and prevention.

## Checklist
- [ ] Every dataset has an owner and contract.
- [ ] Processing is idempotent and checkpointed.
- [ ] Late data and backfill behavior are documented.
- [ ] Quality checks cover schema and business invariants.
- [ ] Quarantine and replay workflows exist.
- [ ] Lineage, retention, and privacy classification exist.
- [ ] Freshness and lag have alerts.
- [ ] Cost and capacity are monitored.

## References
- https://www.dataengineeringweekly.com/
- https://opentelemetry.io/docs/concepts/observability-primer/
- https://docs.getdbt.com/docs/build/data-tests
