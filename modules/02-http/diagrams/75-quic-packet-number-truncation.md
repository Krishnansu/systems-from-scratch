# Diagram 75 - QUIC Packet Number Truncation

```text
Full Packet Number
      |
      v
+----------------+
|     123456     |
+----------------+
      |
      v
Transmit selected low-order bytes
      |
      v
+----------------+
|       56       |
+----------------+
```

The truncated packet number reduces the number of bytes carried in the packet header.
