# GraphQL API Engineering

## Goal
Expose a typed, discoverable API while keeping query cost, authorization, and operational behavior predictable.

## Schema Design
Design the schema around domain capabilities, not database tables. Use nullable fields intentionally, stable identifiers, input objects for mutations, and explicit deprecation instead of breaking removal.

```graphql
type Query {
  viewer: User
  orders(first: Int = 20, after: String, status: OrderStatus): OrderConnection!
}

type Mutation {
  createOrder(input: CreateOrderInput!): CreateOrderPayload!
}

type OrderConnection {
  nodes: [Order!]!
  pageInfo: PageInfo!
  edges: [OrderEdge!]!
}
```typescript

## Resolver Boundaries
Keep resolvers thin. Put authorization and domain rules in application services. Use a request-scoped DataLoader or equivalent batching mechanism to prevent N+1 queries, and never share request-specific cache data across users.

## Authorization
Authorize every object and mutation at the resolver/service boundary. Field-level filtering may be required when a user can see an object but not all fields. Avoid relying on schema introspection visibility as an authorization mechanism.

## Query Cost Controls
Apply maximum depth, node count, alias limits, timeout, and complexity budgets. Disable or restrict introspection only according to the threat model; it is not a replacement for authorization.

```typescript
function validateQueryCost(depth: number, complexity: number): void {
  if (depth > 10 || complexity > 1000) {
    throw new Error('Query exceeds the allowed complexity');
  }
}
```

## Errors
Return stable, actionable error codes in `extensions.code`. Do not expose stack traces, SQL, tokens, or internal hostnames. Distinguish validation, authentication, authorization, conflict, rate-limit, and dependency failures.

## Pagination
Use Relay-style cursors or another opaque cursor format. Define ordering and consistency guarantees. Do not expose database offsets as public cursors when rows can be inserted or deleted between requests.

## Caching
Separate response caching, resolver caching, and normalized client caching. Never cache private data in a shared cache without a user-aware key and explicit policy. Invalidate mutations based on domain events, not arbitrary timeouts alone.

## Federation
Give each subgraph clear ownership and avoid cross-subgraph joins in hot paths. Version contracts, test composition in CI, and instrument downstream calls with trace context.

## Checklist
- [ ] Schema models domain concepts and has documented nullability.
- [ ] Every resolver has an authorization decision.
- [ ] N+1 behavior is tested with realistic lists.
- [ ] Query depth and complexity are bounded.
- [ ] Pagination is opaque and deterministic.
- [ ] Errors use stable public codes without sensitive details.
- [ ] Introspection and persisted-query policy is deliberate.
- [ ] Metrics cover operation name, latency, errors, and cost.
- [ ] Schema changes run compatibility checks.

## Kesalahan Umum / Pitfalls

- No query cost limits — a client can request the whole database.
- N+1 queries in resolvers — database hammering.
- Exposing internal fields via introspection.
- No pagination on list fields — unbounded responses.

## Trade-off dan Kapan Tidak Pakai

- GraphQL is powerful but complex — REST is simpler for public APIs.
- Schema evolution is easier with GraphQL but harder to cache.
- Persisted queries help caching — but add complexity.

## References
- https://graphql.org/learn/
- https://spec.graphql.org/
- https://www.apollographql.com/docs/graphos/schema-design/guides/handling-n-plus-one/

---

*Dokumentasi ini bagian dari [AegisX Skills Collection](https://aegisxresearch.github.io/AegisX-Skills/). Dikelola oleh AegisX Research.*
