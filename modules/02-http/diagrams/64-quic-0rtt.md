# Diagram 36-07 - QUIC 0-RTT Resumption

```text
Previous connection
Client <----------------------> Server
          resumption information

Later connection

Client                                  Server
  |                                       |
  | Initial + TLS ClientHello             |
  | + 0-RTT application data              |
  |-------------------------------------->|
```

0-RTT can reduce startup latency for returning clients, but 0-RTT application data can be replayed, so state-changing operations require careful handling.
