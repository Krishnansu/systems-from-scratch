# Diagram 135 — WebSocket Message Recovery

```text
Server events:
100 → 101 → 102 → 103 → 104
              ^
              |
         connection lost

Client received:
100 → 101

Reconnect:
Client → Server: last_received = 101
Server → Client: 102 → 103 → 104

Alternative:
Reconnect → request current state
```
