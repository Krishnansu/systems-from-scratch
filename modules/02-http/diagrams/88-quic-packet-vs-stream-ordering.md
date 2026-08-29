# Diagram 88 - Packet Number vs Stream Offset

```text
                 QUIC
                   |
          +--------+--------+
          |                 |
          v                 v
    Packet-level         Stream-level
      tracking             ordering
          |                 |
          v                 v
   Packet Number        Stream Offset
```
