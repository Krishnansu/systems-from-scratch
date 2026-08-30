# Lesson 51 — HTTP Evolution: The Big Consolidation

## Objectives

- Understand why HTTP evolved from HTTP/1.1 to HTTP/2 and then HTTP/3.
- Connect HTTP/2 multiplexing with the TCP head-of-line blocking problem.
- Understand why QUIC was introduced as a new transport architecture.
- Understand how HTTP/3 adapts HTTP semantics to QUIC.
- Build a complete mental model of the HTTP/1.1 → HTTP/2 → QUIC → HTTP/3 evolution.

## 1. HTTP Is an Application Protocol

At the highest level, HTTP defines request/response semantics:

```text
Client
  |
  | Request
  v
Server
  |
  | Response
  v
Client
```

HTTP defines concepts such as:

- Methods
- URLs
- Headers
- Status codes
- Request/response semantics
- Caching
- Content

HTTP relies on a transport underneath it to move those messages across the network.

## 2. HTTP/1.1

The traditional stack is:

```text
HTTP/1.1
    |
    v
   TCP
    |
    v
   IP
```

TCP provides:

- Reliable delivery
- Ordered byte delivery
- Retransmission
- Congestion control

HTTP/1.1 works well, but concurrency across many resources is awkward. Browsers therefore historically relied on multiple TCP connections to obtain useful parallelism.

Conceptually:

```text
Client
  |
  +---- TCP #1 ---- Server
  |
  +---- TCP #2 ---- Server
  |
  +---- TCP #3 ---- Server
  |
  +---- TCP #4 ---- Server
```

## 3. HTTP/2 — Multiplexing

HTTP/2 introduced multiplexing of multiple logical streams over one TCP connection.

```text
HTTP/2 connection
       |
       +---- Stream A
       +---- Stream B
       +---- Stream C
       +---- Stream D
```

Instead of requiring a separate connection for every concurrent operation, multiple requests and responses can share one connection.

This was a major improvement in HTTP concurrency.

## 4. The Hidden HTTP/2 Problem

HTTP/2 streams exist above TCP. TCP itself only sees one ordered byte stream.

```text
HTTP/2
   |
   +---- Stream A
   +---- Stream B
   +---- Stream C
          |
          v
         TCP
          |
          v
   One ordered byte stream
```

TCP does not understand that bytes belong to independent HTTP/2 streams.

If one TCP packet is lost, TCP must wait for the missing bytes before delivering later bytes to the application.

Conceptually:

```text
Stream A ───── X ─── loss ─── waiting
Stream B ───────────────────── waiting
Stream C ───────────────────── waiting
```

This is TCP-level cross-stream head-of-line blocking.

### Important Distinction

HTTP/2 provides logical stream multiplexing, but the underlying TCP transport still has one ordered byte stream.

Therefore:

> HTTP/2 multiplexing does not eliminate TCP-level cross-stream head-of-line blocking.

## 5. Why QUIC Was Introduced

The deeper problem was not an HTTP feature that could simply be added to HTTP/2. The limitation came from the transport architecture.

TCP already defines its transport behavior, including:

- Ordering
- Reliability
- Retransmission
- Congestion control
- Connection state

TCP cannot simply be instructed to expose independent reliable streams with QUIC-like semantics.

A new transport architecture was therefore introduced: QUIC.

```text
HTTP/3
   |
  QUIC
   |
  UDP
   |
  IP
```

## 6. QUIC Provides Independent Streams

QUIC understands streams as part of the transport itself.

```text
QUIC connection
       |
       +---- Stream A
       |
       +---- Stream B
       |
       +---- Stream C
```

If Stream A loses data, Stream B and Stream C can continue receiving available data.

```text
Stream A ───── X ─── loss ─── waiting
Stream B ───────────────────────→
Stream C ───────────────────────→
```

The important claim is:

> QUIC eliminates TCP-level cross-stream head-of-line blocking between independent streams.

It does not eliminate every possible form of blocking. Ordering within an individual stream still matters, and congestion, flow control, server processing, and network failures can still affect communication.

## 7. Why UDP?

UDP itself is not responsible for HTTP/3's performance benefits.

The important advantage is that QUIC can implement its own transport behavior above a minimal datagram substrate.

```text
UDP
 |
 v
QUIC
 +-- reliability
 +-- loss detection
 +-- retransmission
 +-- stream multiplexing
 +-- flow control
 +-- congestion control
 +-- connection IDs
 +-- migration
 +-- TLS integration
```

The architecture gives QUIC control that it could not obtain by simply running above TCP.

## 8. QUIC Still Provides Reliable Transport

HTTP/3 is not an unreliable protocol simply because it uses UDP.

The stack is:

```text
HTTP/3
   |
 QUIC
   |
 UDP
   |
 IP
```

QUIC provides reliability and transport control itself, including loss detection, retransmission, flow control, and congestion control.

## 9. HTTP/3

HTTP/3 adapts HTTP semantics to QUIC.

```text
HTTP semantics
       |
       v
    HTTP/3
       |
       v
      QUIC
       |
       v
      UDP
```

HTTP concepts such as methods, status codes, headers, cookies, and caching remain HTTP concepts.

The major architectural change is the transport underneath them.

## 10. HTTP/2 Streams vs HTTP/3 Streams

HTTP/2:

```text
HTTP/2
  |
  +---- Stream A
  +---- Stream B
  +---- Stream C
          |
          v
         TCP
```

HTTP/3:

```text
HTTP/3
  |
  +---- Stream A
  +---- Stream B
  +---- Stream C
          |
          v
         QUIC
```

The critical difference is that HTTP/3's streams are directly backed by QUIC transport streams, allowing QUIC to provide independent delivery behavior.

## 11. TLS and Connection Establishment

Traditional HTTPS conceptually involves separate TCP and TLS establishment:

```text
TCP handshake
      |
      v
TLS handshake
      |
      v
HTTP
```

QUIC integrates TLS 1.3 into connection establishment:

```text
QUIC handshake
      |
      +---- transport establishment
      |
      +---- TLS 1.3
      |
      v
HTTP/3
```

For resumed connections, QUIC/TLS can also support 0-RTT application data, subject to replay considerations.

## 12. Connection Migration

TCP connections are closely associated with their network endpoints. A network change can therefore require a new connection.

QUIC uses Connection IDs to allow a connection to survive certain network-path changes.

```text
Same QUIC connection
       |
       +---- Wi-Fi
       |
       +---- Mobile
```

The new path is validated before it is trusted for continued communication.

## 13. QPACK

HTTP/2 uses HPACK, while HTTP/3 uses QPACK.

This difference is connected to the transport architecture:

```text
HTTP/2
   |
 HPACK
   |
 TCP ordered transport

HTTP/3
   |
 QPACK
   |
 QUIC independent streams
```

QPACK was designed to provide header compression without imposing the same blocking behavior that would conflict with independent QUIC streams.

## 14. Flow Control

HTTP/3's transport inherits QUIC's flow-control model.

QUIC can control both the connection as a whole and individual streams.

```text
QUIC connection
       |
       +---- Connection flow-control limit
       |
       +---- Stream A limit
       +---- Stream B limit
       +---- Stream C limit
```

The purpose remains the same:

> Prevent a sender from overwhelming the receiver.

## 15. Errors Exist at Different Layers

A failure in the HTTP layer is not necessarily a QUIC failure.

```text
Application
   |
   | HTTP response/error
   v
HTTP/3
   |
   | HTTP/3 protocol error
   v
QUIC
   |
   | QUIC transport error
   v
Network
```

For example:

```text
503 No healthy upstream
```

is an HTTP response generated by an HTTP server or intermediary.

A QUIC connection failure may instead mean that no HTTP response was received at all.

## 16. The Complete Evolution

The architectural story can be summarized as:

```text
HTTP/1.1
   |
   | Concurrency limitations
   v
HTTP/2
   |
   | Multiplexing
   | Header compression
   |
   | BUT TCP still provides
   | one ordered byte stream
   | → TCP-level HOL blocking
   v
QUIC
   |
   | Independent streams
   | Loss recovery
   | Flow control
   | Congestion control
   | Connection IDs
   | Migration
   | Integrated TLS
   v
HTTP/3
   |
   | HTTP semantics adapted to QUIC
   | QPACK
   | Control streams
   | HTTP/3 frame model
   v
Modern HTTP transport
```

## 17. The Correct Way to Think About the Evolution

Do not think:

```text
HTTP/1.1 = bad
HTTP/2   = better
HTTP/3   = best
```

Instead:

```text
HTTP/1.1
   |
   | Need better concurrency
   v
HTTP/2
   |
   | Multiplexing helps,
   | but TCP creates a transport-level limitation
   v
QUIC
   |
   | New transport architecture
   v
HTTP/3
   |
   | HTTP adapted to the new transport
```

Each generation addresses important limitations of the previous architecture while introducing its own trade-offs.

## 18. Comparison Table

| | HTTP/1.1 | HTTP/2 | HTTP/3 |
|---|---|---|---|
| Transport | TCP | TCP | QUIC |
| Network substrate | IP | IP | UDP/IP |
| Multiplexing | Limited | Yes | Yes |
| TCP cross-stream HOL | N/A | Yes | No |
| Header compression | None | HPACK | QPACK |
| TLS | Separate layer | Separate layer | Integrated with QUIC |
| Connection migration | No | No | Yes |
| 0-RTT | No | No | Yes, via QUIC/TLS resumption |
| Flow control | TCP | HTTP/2 + TCP | QUIC stream + connection |
| HTTP semantics | HTTP | HTTP | HTTP |

## Key Takeaways

1. HTTP/1.1's major limitation was inefficient concurrency across many resources.
2. HTTP/2 introduced multiplexing over a single TCP connection.
3. TCP does not understand HTTP/2 streams; it only provides one ordered byte stream.
4. TCP-level head-of-line blocking can therefore affect multiple HTTP/2 streams.
5. QUIC was introduced as a new transport architecture rather than modifying TCP.
6. QUIC provides independent streams, allowing unrelated streams to make progress despite loss on another stream.
7. UDP is only the substrate; QUIC provides reliability, flow control, congestion control, and loss recovery.
8. HTTP/3 adapts HTTP semantics to QUIC rather than fundamentally changing HTTP semantics.
9. QPACK, connection migration, 0-RTT, and QUIC flow control are consequences or capabilities of the new transport architecture.
10. The overall evolution is best remembered as:

```text
HTTP/1.1
   ↓
Concurrency problem
   ↓
HTTP/2
   ↓
Transport problem caused by TCP
   ↓
QUIC
   ↓
HTTP adaptation
   ↓
HTTP/3
```

## Reflection Questions

- Why couldn't HTTP/2 simply solve TCP head-of-line blocking at the HTTP layer?
- Why did QUIC need to run over UDP instead of TCP?
- What exactly is different about an HTTP/3 stream compared with an HTTP/2 stream?
- Which parts of HTTP remained unchanged between HTTP/2 and HTTP/3?
- Why is `503 No healthy upstream` fundamentally different from a QUIC connection failure?
- What architectural problem does QPACK solve?

## Next Lesson

Lesson 52 — Build an HTTP/3 Request From Scratch.

We will trace a single request from HTTP semantics all the way down through HTTP/3 frames, QPACK, a QUIC stream, QUIC packets, UDP, IP, and the network, then trace the response back up the stack.
