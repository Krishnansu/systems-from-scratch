# Diagram 36-04 - QUIC Encryption Levels

```text
Connection start
      |
      v
+-------------+
|   Initial   |
| Initial keys|
+-------------+
      |
      v
+-------------+
|  Handshake  |
|Handshake keys|
+-------------+
      |
      v
+-------------+
|    1-RTT    |
| Application |
|    keys     |
+-------------+
      |
      v
   HTTP/3 data
```

The exact TLS and QUIC key schedule is more detailed; this diagram shows the high-level progression.
