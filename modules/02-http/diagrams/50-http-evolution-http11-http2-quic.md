# HTTP/1.1 → HTTP/2 → QUIC → HTTP/3

```text
HTTP/1.1
    |
    | Limited parallelism
    v
Multiple TCP Connections / Pipelining
    |
    | Overhead / ordered responses
    v
HTTP/2
    |
    | Multiplexed HTTP streams
    v
One TCP Connection
    |
    | TCP-level HOL blocking
    v
QUIC
    |
    | Transport-level streams
    v
HTTP/3
```

**Key Insight**

HTTP/2 solves HTTP-level multiplexing. QUIC moves multiplexed streams into the transport layer, providing the foundation for HTTP/3.