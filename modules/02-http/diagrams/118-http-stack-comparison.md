# Diagram 118 — HTTP/2 vs HTTP/3 Stack

```text
HTTP/2                              HTTP/3

HTTP semantics                      HTTP semantics
      |                                    |
      v                                    v
   HTTP/2                               HTTP/3
      |                                    |
      +-- Stream A                         +-- Stream A
      +-- Stream B                         +-- Stream B
      +-- Stream C                         +-- Stream C
      |                                    |
      v                                    v
     TCP                                  QUIC
      |                                    |
      |                                    +-- independent streams
      |                                    +-- loss recovery
      |                                    +-- flow control
      |                                    +-- congestion control
      |                                    +-- Connection IDs
      |                                    +-- migration
      |                                    +-- TLS 1.3
      |                                    |
      v                                    v
     IP                                   UDP
                                           |
                                           v
                                          IP
```

HTTP/2 multiplexes at the HTTP layer over TCP's single ordered byte stream. HTTP/3 uses QUIC, which provides independent transport streams and additional transport capabilities.
