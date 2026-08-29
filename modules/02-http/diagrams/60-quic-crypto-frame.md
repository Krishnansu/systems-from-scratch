# Diagram 36-03 - TLS Handshake Inside QUIC CRYPTO Frames

```text
QUIC Initial Packet
+-----------------------------------+
| QUIC Header                       |
+-----------------------------------+
| CRYPTO Frame                      |
|                                   |
| TLS ClientHello                   |
+-----------------------------------+
```

Later handshake messages follow the same general pattern:

```text
TLS handshake bytes
        |
        v
   CRYPTO frame
        |
        v
   QUIC packet
        |
        v
   UDP datagram
```
