# Evolution from HTTP/1.1 to HTTP/3

```text
HTTP/1.1
    │
    │ Multiple requests
    ▼
Multiple TCP Connections
    │
    │ Connection / TLS overhead
    ▼
HTTP/1.1 Pipelining
    │
    │ Ordered responses
    ▼
Head-of-Line Blocking
    │
    ▼
HTTP/2
    │
    │ Multiplexed streams
    ▼
One TCP Connection
    │
    │ TCP still provides
    │ ordered byte delivery
    ▼
TCP Head-of-Line Blocking
    │
    ▼
QUIC
    │
    │ Independent streams
    ▼
HTTP/3
```

**Key Insight**

HTTP/2 solves important HTTP-level multiplexing problems, but TCP's ordered byte-stream semantics remain. QUIC moves stream multiplexing into the transport design, providing the foundation for HTTP/3.