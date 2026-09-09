# Diagram 133 — WebSocket Message Fragmentation

```text
Logical Message
      |
      +--> TEXT frame, FIN=0
      |
      +--> CONTINUATION frame, FIN=0
      |
      +--> CONTINUATION frame, FIN=1
      |
      +--> Reassembled Message
```

Control frames such as Ping may appear between fragments.
