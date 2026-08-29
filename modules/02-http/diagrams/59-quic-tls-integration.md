# Diagram 36-02 - QUIC and TLS 1.3 Integration

```text
                 HTTP/3
                    |
                    v
                  QUIC
        +-----------+-----------+
        |                       |
   Transport                 TLS 1.3
        |                       |
   Packets                   Handshake
   Streams                   Key exchange
   ACKs                      Secrets
   Reliability               Authentication
        |                       |
        +-----------+-----------+
                    |
                    v
                   UDP
```

TLS supplies cryptographic state. QUIC supplies transport state.
