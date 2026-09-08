# WebSocket & Realtime Systems

## Goal
Deliver live updates without treating a persistent connection as a guarantee of delivery or authorization.

## Connection Lifecycle
```text
HTTP upgrade → authenticate → authorize subscriptions → heartbeat → messages → drain → close
```

Authenticate during the handshake and re-check authorization when subscribing to a resource. Do not place long-lived secrets in query strings. Prefer secure cookies or a short-lived connection token with origin validation.

## Message Envelope
```typescript
type ClientMessage =
  | { type: 'subscribe'; channel: string; requestId: string }
  | { type: 'unsubscribe'; channel: string; requestId: string }
  | { type: 'ack'; messageId: string };

type ServerMessage = {
  type: 'event' | 'error' | 'snapshot';
  messageId: string;
  sequence: number;
  channel: string;
  payload: unknown;
};
```
Validate message type, size, channel, and payload at runtime. Treat all client messages as untrusted.

## Reliability
WebSockets commonly provide ordered delivery per connection, not durable delivery. Add sequence numbers, acknowledgements, replay windows, or snapshots when the domain requires recovery after reconnect. Define whether duplicate delivery is possible and make consumers idempotent.

## Reconnect
Use exponential backoff with jitter, a maximum delay, and a retry budget. On reconnect, re-authenticate and resynchronize from the last acknowledged sequence or request a fresh snapshot. Do not create unbounded reconnect storms.

## Heartbeats and Backpressure
Use ping/pong or application heartbeats to remove dead connections. Bound per-connection queues, enforce message rate limits, and close slow consumers predictably. Prefer dropping obsolete presence updates over allowing memory growth.

## Horizontal Scaling
A load balancer may route successive connections to different instances. Use a broker or durable event log for fanout, but keep authorization and connection state local or replicated deliberately. Document ordering guarantees across instances.

## Shutdown
Stop accepting new connections, notify clients when appropriate, drain bounded queues, close with a meaningful code, and expose connection counts during deployment.

## Observability
Track active connections, handshake failures, auth failures, subscriptions, message rates, queue depth, reconnect rate, close codes, delivery latency, and broker lag. Avoid logging message payloads containing personal data.

## Checklist
- [ ] Origin, authentication, authorization, and message validation are enforced.
- [ ] Connection and subscription limits exist.
- [ ] Heartbeats remove dead clients.
- [ ] Backpressure cannot grow memory without bound.
- [ ] Reconnect and replay behavior is documented.
- [ ] Duplicate delivery is safe or prevented.
- [ ] Multi-instance fanout and ordering are tested.
- [ ] Graceful shutdown drains connections.
- [ ] Metrics and close-code dashboards exist.

## References
- https://www.rfc-editor.org/rfc/rfc6455
- https://developer.mozilla.org/en-US/docs/Web/API/WebSocket
- https://owasp.org/www-community/vulnerabilities/WebSocket_Security

---

*Dokumentasi ini bagian dari [AegisX Skills Collection](https://aegisxresearch.github.io/AegisX-Skills/). Dikelola oleh AegisX Research.*
