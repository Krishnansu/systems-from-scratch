# Diagram 91 - QUIC Stream Loss Independence

```text
Packet 100 → Stream 4 ─── X
Packet 101 → Stream 8 ─────→
Packet 102 → Stream 12 ────→

Stream 4 data needs recovery.
Stream 8 and Stream 12 can continue.
```
