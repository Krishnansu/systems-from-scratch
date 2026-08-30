# Lesson 50 — HTTP/3 Performance & Trade-offs

## Objectives

- Understand why HTTP/3 can outperform HTTP/2 under certain network conditions.
- Understand how QUIC eliminates TCP-level cross-stream head-of-line blocking.
- Understand the performance implications of QUIC's handshake, 0-RTT, and connection migration.
- Understand why UDP itself is not inherently faster than TCP.
- Understand the costs and deployment trade-offs of HTTP/3.

## Core Idea

HTTP/3 is not automatically faster than HTTP/2 in every environment. Its major performance benefits come from the transport architecture provided by QUIC.

The most important idea is:

> HTTP/3 addresses transport limitations that remain when HTTP/2 runs over TCP.

## 1. Cross-Stream Head-of-Line Blocking

HTTP/2 multiplexes multiple streams over a single TCP byte stream.

```text
HTTP/2
   |
   v
Multiple streams
   |
   v
TCP
   |
   v
One ordered byte stream
```

If one TCP segment is lost, TCP must wait for the missing bytes before delivering later bytes to the application. This can affect unrelated HTTP/2 streams.

QUIC instead provides independent transport streams:

```text
QUIC Connection
   |
   +---- Stream A
   |
   +---- Stream B
   |
   +---- Stream C
```

If data for Stream A is lost, Stream B and Stream C can continue receiving their available data.

### Important Nuance

HTTP/3 does not eliminate every form of head-of-line blocking. Ordering requirements still exist within an individual stream, and congestion, flow control, server processing, and network failures can still affect the connection.

The precise claim is:

> HTTP/3 eliminates TCP-level cross-stream head-of-line blocking between independent QUIC streams.

## 2. Connection Establishment

Traditional HTTPS conceptually involves:

```text
TCP handshake
      |
      v
TLS handshake
      |
      v
HTTP request
```

QUIC integrates TLS 1.3 into the transport handshake:

```text
QUIC
  |
  +---- Transport establishment
  |
  +---- TLS 1.3
  |
  v
HTTP/3
```

This can reduce connection-establishment latency compared with a separate TCP and TLS handshake sequence.

## 3. 0-RTT

For eligible resumed connections, QUIC/TLS 1.3 can allow application data to be sent as early as the first flight of a new connection.

Conceptually:

```text
Previous connection
       |
       v
Client retains resumption state
       |
       v
New connection
       |
       +---- early application data
       |
       v
Server
```

### Important Caveat

0-RTT data can be replayed. Applications must therefore be careful with operations that have side effects.

Idempotent or otherwise replay-safe requests are better candidates than operations such as:

```text
POST /transfer-money
POST /create-order
```

## 4. Connection Migration

QUIC connection IDs allow a connection to survive certain network-path changes.

```text
Old path
192.168.1.20
     |
     X
     |
New path
10.20.30.40
```

QUIC validates the new path and can continue using the existing connection.

HTTP/3 streams do not have to be recreated simply because the underlying network path changed.

Migration is not free: the new path may have different latency, bandwidth, congestion conditions, or temporary packet loss.

## 5. UDP Is Not Automatically Faster

A common misconception is:

> HTTP/3 is faster because it uses UDP.

This is incomplete.

UDP itself provides only a datagram transport. The performance advantages come from QUIC building its own transport semantics above UDP.

```text
UDP
  |
  v
QUIC implements
  +---- streams
  +---- ACKs
  +---- loss recovery
  +---- flow control
  +---- congestion control
  +---- connection IDs
  +---- migration
```

The important advantage is that QUIC is not constrained by TCP's transport architecture.

## 6. QUIC's Costs

QUIC introduces substantial transport functionality:

- Stream management
- Packet numbering
- ACK processing
- Loss detection
- Retransmission
- Flow control
- Congestion control
- Connection IDs
- Path validation
- Connection migration
- TLS integration
- Encryption

This creates additional implementation and packet-processing complexity.

Depending on workload and implementation, QUIC can introduce additional CPU and memory overhead compared with a mature TCP stack.

## 7. UDP Deployment Considerations

Some networks and middleboxes historically treated UDP differently from TCP. Modern HTTP/3 deployments have improved significantly, but restrictive networks can still make UDP-based connectivity more complicated.

HTTP/3 therefore commonly exists alongside HTTP/2 rather than completely replacing it.

Conceptually:

```text
                 Server
                    |
             Protocol negotiation
                    |
          +---------+---------+
          |                   |
        HTTP/3              HTTP/2
          |                   |
        QUIC                 TCP
```

## 8. Where HTTP/3 Helps Most

HTTP/3 can be particularly valuable when there is:

### Packet loss

```text
QUIC
  |
  +---- Stream A → loss
  |
  +---- Stream B → continues
  |
  +---- Stream C → continues
```

### Higher latency

Reducing handshake overhead can have a larger impact when round-trip time is high.

### Network changes

Connection migration can avoid rebuilding the entire connection after certain network-path changes.

### Many concurrent resources

Independent QUIC streams reduce the impact of packet loss on unrelated streams.

## 9. Where HTTP/3 May Not Make a Huge Difference

On a stable, low-loss, low-latency network, HTTP/2 over TCP can already be highly efficient.

For example:

```text
Client
   |
   | fast + stable network
   |
Server
```

HTTP/3 should therefore not be thought of as a universal speed multiplier.

## 10. Performance Model

A useful conceptual model is:

```text
Total request/page latency
    =
Connection establishment
+
Request/response latency
+
Packet-loss recovery
+
Scheduling
+
Server processing
+
Network congestion
```

HTTP/3 primarily improves some of these transport-related components. It cannot eliminate physical distance, limited bandwidth, server processing time, congestion, or inefficient application behavior.

## 11. Evolution of the Protocol Stack

The progression is best understood as an engineering response to specific limitations:

```text
HTTP/1.1
   |
   | Need better concurrency
   v
HTTP/2
   |
   | Multiplexing helps, but TCP still has
   | one ordered byte stream
   v
HTTP/3
   |
   | QUIC provides independent streams,
   | modern handshake, and migration
   v
Modern HTTP transport
```

This is not simply:

```text
HTTP/1.1 = bad
HTTP/2   = better
HTTP/3   = best
```

Each generation solves important problems of the previous architecture while introducing its own trade-offs.

## 12. Trade-off Summary

```text
HTTP/3
  |
  +---- Benefits
  |       +-- Independent streams
  |       +-- Reduced cross-stream HOL blocking
  |       +-- Lower connection-establishment latency
  |       +-- 0-RTT for eligible resumed connections
  |       +-- Connection migration
  |
  +---- Costs
          +-- More transport complexity
          +-- CPU/memory overhead
          +-- UDP deployment considerations
```

## Key Takeaways

1. HTTP/3's major transport-level advantage is eliminating TCP's cross-stream head-of-line blocking.
2. QUIC integrates TLS 1.3 into its transport handshake, reducing connection-establishment overhead.
3. 0-RTT can reduce latency for resumed connections but introduces replay considerations.
4. Connection migration can allow a QUIC connection to survive certain network-path changes.
5. UDP itself is not inherently faster; it provides the substrate on which QUIC implements its own transport.
6. QUIC introduces additional implementation and packet-processing complexity.
7. HTTP/3 is not automatically faster than HTTP/2 in every environment.
8. HTTP/3's advantages are particularly relevant under packet loss, higher latency, and changing network paths.
9. HTTP/2 remains useful on stable networks and as a fallback when HTTP/3 connectivity is unavailable.
10. HTTP/3 is best understood as HTTP semantics running over a redesigned transport rather than simply a faster version of HTTP/2.

## Reflection Questions

- Why does a lost TCP packet affect unrelated HTTP/2 streams?
- Why does QUIC allow unrelated streams to continue?
- Why isn't UDP itself responsible for HTTP/3's performance benefits?
- Why can 0-RTT improve latency while simultaneously creating a replay concern?
- In what network conditions would HTTP/3's advantages be most noticeable?

## Related Lessons

- Lesson 30 — HTTP/2 Flow Control & Stream Management
- Lesson 43 — HTTP/3 Fundamentals
- Lesson 44 — HTTP/3 Streams & Frame Types
- Lesson 47 — HTTP/3 Error Handling & Connection Shutdown
- Lesson 48 — HTTP/3 Push & Prioritization
- Lesson 49 — HTTP/3 ↔ QUIC Integration
- Lesson 51 — HTTP Evolution Consolidation
