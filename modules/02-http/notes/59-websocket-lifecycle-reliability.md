# Lesson 59 — WebSocket Lifecycle & Reliability

## Objectives

- Understand the lifecycle of a production WebSocket connection.
- Understand heartbeats and failure detection.
- Understand reconnection and reconnect storms.
- Understand exponential backoff and jitter.
- Understand missed messages, sequence numbers, replay, and state synchronization.

## Core Ideas

A WebSocket connection can fail because of network changes, server crashes, load balancers, timeouts, or application failures. Production clients need failure detection, reconnection, and a strategy for recovering state.

```text
CONNECTED
    │
    │ failure
    ▼
RECONNECTING
    │
    │ backoff + jitter
    ▼
CONNECTING
    │
    ├── success → RESUME / RESYNC → CONNECTED
    └── failure → retry
```

- Ping/Pong can provide application-level liveness checks.
- Heartbeat failure indicates that a connection may be unhealthy; it does not itself reconnect the client.
- Immediate reconnects can create reconnect storms when many clients fail simultaneously.
- Exponential backoff spreads reconnect attempts over time.
- Jitter prevents many clients from retrying at exactly the same time.
- Connection reliability is different from message reliability.
- TCP/WebSocket reliability applies while the connection exists; applications must handle messages missed during disconnection.
- Sequence numbers can identify the last received event.
- After reconnecting, applications may replay missed events or synchronize current state.

## Reconnect Strategy

```text
Attempt 1 → ~1s
Attempt 2 → ~2s
Attempt 3 → ~4s
Attempt 4 → ~8s
...
```

Add random jitter so large groups of clients do not reconnect simultaneously.

## Event Replay vs State Synchronization

```text
Event replay:
"Send everything after sequence 101."

State synchronization:
"Give me the current state."
```

Event replay is useful when historical events matter. State synchronization is often sufficient for dashboards, presence, or current-value views.

## Practical Example

A chat client receives:

```text
100 ✓
101 ✓
102 ✗
103 ✗
```

After reconnecting, it can tell the server it has received through `101` and request events starting from `102`.

## Key Takeaways

- WebSocket reliability has both connection-level and application-level dimensions.
- Heartbeats help detect unhealthy connections.
- Exponential backoff + jitter prevents reconnect storms.
- Sequence numbers can support message resumption.
- Applications must choose between replaying events and synchronizing current state.

## Reflection Questions

1. Why can TCP being connected differ from the application being healthy?
2. Why is jitter important when thousands of clients reconnect?
3. When is state synchronization better than replaying missed events?
4. What information would a server need to resume a client's event stream?

## Related Lessons

- Lesson 57 — WebSockets
- Lesson 58 — WebSocket Protocol Deep Dive
- Lesson 60 — WebSockets at Scale
