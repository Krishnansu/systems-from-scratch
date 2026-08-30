# Diagram 115 — HTTP/3 Data to Network

```text
HTTP response body
        |
        v
QPACK (if headers)
        |
        v
HTTP/3 frame
        |
        v
QUIC stream
        |
        v
QUIC STREAM frame
        |
        v
QUIC packet
        |
        v
UDP datagram
        |
        v
IP packet
        |
        v
NETWORK
```

Receiving side reverses the process:

```text
NETWORK
   |
   v
IP → UDP → QUIC packet → QUIC stream
                              |
                              v
                         HTTP/3 frame
                              |
                              v
                         HTTP semantics
```
