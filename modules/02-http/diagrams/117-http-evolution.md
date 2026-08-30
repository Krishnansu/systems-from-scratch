# Diagram 117 — HTTP Evolution

```text
                         HTTP EVOLUTION

HTTP/1.1
   |
   | Need better concurrency
   v
HTTP/2
   |
   | Multiplexing
   | HPACK
   |
   | BUT TCP provides one ordered byte stream
   | → TCP-level cross-stream HOL blocking
   v
QUIC
   |
   | Independent streams
   | Loss recovery
   | Flow control
   | Congestion control
   | Connection IDs
   | Migration
   | TLS 1.3 integration
   v
HTTP/3
   |
   | HTTP semantics over QUIC
   | QPACK
   | HTTP/3 frames
   | Control streams
   v
Modern HTTP transport
```

The diagram captures the central architectural story: each major evolution responds to a limitation of the previous architecture.
