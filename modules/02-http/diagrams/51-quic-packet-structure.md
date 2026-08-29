# Diagram 35-01 - QUIC Packet Structure

```text
+------------------------------------------+
| QUIC Packet Header                       |
|                                          |
| Connection ID                            |
| Packet Number                            |
| Other header information                 |
+------------------------------------------+
| Frame 1                                  |
+------------------------------------------+
| Frame 2                                  |
+------------------------------------------+
| Frame 3                                  |
+------------------------------------------+
| ...                                      |
+------------------------------------------+
```

Key idea:

```text
QUIC packet = header + one or more frames
```
