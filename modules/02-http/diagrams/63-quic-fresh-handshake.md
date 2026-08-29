# Diagram 36-06 - Fresh QUIC Connection

```text
Client                                  Server
  |                                       |
  | Initial                               |
  | CRYPTO: TLS ClientHello               |
  |-------------------------------------->|
  |                                       |
  | Initial / Handshake                   |
  | CRYPTO: TLS handshake data            |
  |<--------------------------------------|
  |                                       |
  | Handshake                             |
  | CRYPTO: TLS handshake data            |
  |-------------------------------------->|
  |                                       |
  | 1-RTT                                 |
  | STREAM: HTTP/3 request                |
  |-------------------------------------->|
```

TLS and QUIC progress together rather than performing separate TCP and TLS establishment phases.
