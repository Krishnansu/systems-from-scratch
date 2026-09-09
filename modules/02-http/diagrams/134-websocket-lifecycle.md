# Diagram 134 — WebSocket Lifecycle & Recovery

```text
CONNECTING
    |
    | success
    v
CONNECTED
    |
    | heartbeat failure / network failure
    v
RECONNECTING
    |
    | exponential backoff + jitter
    v
CONNECTING
    |
    +---- success ----> RESUME / RESYNC ----> CONNECTED
    |
    +---- failure ----> retry
```
