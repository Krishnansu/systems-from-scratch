# Diagram 105 - QUIC NAT Rebinding

```text
Before:
Client → NAT → 203.0.113.20:62000 → Server

After:
Client → NAT → 203.0.113.20:62001 → Server

Logical QUIC connection can remain the same.
```
