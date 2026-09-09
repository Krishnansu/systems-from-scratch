# Lesson 62 — HTTP Module Consolidation

## Core Mental Model

The HTTP module is not a sequence where every technology replaces the previous one. It is a growing toolbox where each mechanism addresses a particular systems problem.

```text
HTTP/1.1
   ↓ concurrency limitations
HTTP/2
   ↓ TCP-level head-of-line blocking
QUIC
   ↓ HTTP semantics over QUIC
HTTP/3
   ↓ application continuity
Sessions / JWT
   ↓ latency and backend load
Caching
   ↓ network bandwidth
Compression
   ↓ persistent real-time communication
WebSocket
   ↓ peer-to-peer real-time media/data
WebRTC
```

## HTTP/1.1 → HTTP/2

HTTP/1.1 primarily uses request/response communication. HTTP/2 introduced multiplexed streams so multiple requests could share a connection.

```text
HTTP/2
│
├── Stream 1
├── Stream 3
├── Stream 5
└── Stream 7
```

However, TCP still provides one ordered byte stream, so packet loss can cause cross-stream head-of-line blocking at the transport layer.

## HTTP/2 → QUIC → HTTP/3

QUIC provides independent transport streams and modern transport features.

```text
HTTP/3
   ↓
QUIC
   ↓
UDP
   ↓
IP
```

QUIC provides mechanisms such as:
- Independent streams
- Flow control
- Loss recovery
- Congestion control
- Integrated TLS
- Connection IDs
- Connection migration

HTTP/3 adapts HTTP semantics to QUIC.

## Sessions and JWT

HTTP is stateless, but applications often need to identify users across requests.

Sessions store authentication state on the server side, while JWTs represent authentication information in a signed token that can often be verified locally.

```text
Session:
Client → Session ID → Server → Session Store

JWT:
Client → JWT → Server → Signature Verification
```

Both approaches involve trade-offs around scalability, revocation, state management, and security.

## Caching

Caching reduces latency and backend load by serving frequently accessed data from a faster layer.

```text
Client
  ↓
Application
  ├── Cache → HIT
  └── Database → MISS
```

Important concepts:
- Cache hit/miss
- TTL
- Eviction
- Cache-aside
- Invalidation
- Cache stampede
- Hot keys
- Distributed caching

Caching trades some consistency complexity for performance.

## Compression

Compression reduces network bytes at the cost of CPU work.

```text
Original data
     ↓
 Compression
     ↓
Smaller payload
     ↓
   Network
```

Important distinction:

```text
HTTP body compression ≠ HPACK ≠ QPACK
```

HPACK and QPACK primarily compress HTTP headers, while gzip/Brotli compress message bodies.

## WebSockets

WebSockets provide a persistent bidirectional client/server channel.

```text
Client <=================> Server
       persistent channel
```

Useful for:
- Chat
- Notifications
- Presence
- Collaborative editing
- Live dashboards
- Real-time game state

At scale, WebSockets introduce distributed-systems concerns such as connection ownership, load balancing, connection registries, message brokers, fan-out, presence, reconnects, and state recovery.

## WebRTC

WebRTC is designed for real-time peer-to-peer media and data.

```text
Peer A <====================> Peer B
          WebRTC
       video/audio/data
```

Important concepts:
- Signaling
- SDP
- ICE
- STUN
- TURN
- NAT traversal
- DataChannel

WebRTC is particularly suited to video calls, audio calls, and screen sharing because it is designed around real-time media transport.

## WebSocket vs WebRTC

They are complementary rather than direct replacements.

```text
HTTP      → APIs / resources
WebSocket → server-backed real-time communication
WebRTC    → peer-to-peer real-time media/data
```

A video application might use:

```text
HTTP
  → authentication, APIs, configuration

WebSocket
  → signaling, chat, presence, coordination

WebRTC
  → video, audio, screen sharing
```

## Full Systems View

```text
                    APPLICATION
                         |
          +--------------+--------------+
          |              |              |
         HTTP         WebSocket       WebRTC
          |              |              |
      APIs/CRUD      Real-time       Media/P2P
          |          server comms        |
          +--------------+--------------+
                         |
                    NETWORK STACK
                         |
                  HTTP/3 → QUIC
                         |
                        UDP
                         |
                         IP
```

Surrounding the communication mechanisms:

```text
Authentication
├── Sessions
└── JWT

Performance
├── Caching
└── Compression

Distributed Systems
├── Load Balancers
├── Connection Registries
├── Message Brokers
└── Databases
```

## Systems Thinking Pattern

Do not start with:

> "Which technology should I use?"

Start with:

> "What communication or systems problem am I solving?"

Examples:

- Need request/response APIs → HTTP
- Need multiplexed HTTP over a modern transport → HTTP/3 + QUIC
- Need user continuity → Sessions or JWT
- Need lower latency/backend load → Cache
- Need fewer network bytes → Compression
- Need persistent server communication → WebSocket
- Need real-time peer media → WebRTC
- Need distributed WebSockets → Load balancer + connection registry + message broker + recovery strategy

## Final Mental Model

```text
                    WHAT DOES THE SYSTEM NEED?
                              |
          +-------------------+-------------------+
          |                   |                   |
      Request/Response   Server Push/Realtime   P2P Media
          |                   |                   |
         HTTP             WebSocket             WebRTC
          |                   |                   |
          +-------------------+-------------------+
                              |
                        NETWORK STACK
                              |
                    HTTP/3 → QUIC → UDP → IP
```

The key lesson is that these technologies form a toolbox, not a replacement chain.

## Summary

The HTTP module evolved by solving increasingly specific communication and systems problems: HTTP/1.1 established web request/response, HTTP/2 improved concurrency, QUIC introduced a modern transport with independent streams, HTTP/3 brought HTTP semantics onto QUIC, sessions and JWT addressed application identity, caching and compression improved performance, WebSockets enabled persistent bidirectional communication, and WebRTC enabled real-time peer-to-peer media and data.

## Key Takeaways

1. Each protocol or mechanism exists to solve a particular constraint.
2. HTTP/2 multiplexes streams but still runs over TCP.
3. QUIC provides independent transport streams and modern transport capabilities.
4. HTTP/3 is HTTP semantics over QUIC.
5. Sessions and JWT solve application authentication/continuity with different state-management trade-offs.
6. Caching trades consistency complexity for performance.
7. Compression trades CPU work for reduced network traffic.
8. WebSockets provide persistent bidirectional client/server communication.
9. WebRTC is designed for real-time peer-to-peer media/data.
10. WebSocket and WebRTC are often complementary rather than competing technologies.
11. Systems design should begin with the problem and communication model, not the technology name.

## Reflection Questions

1. What specific problem did HTTP/2 solve that HTTP/1.1 struggled with?
2. Why was QUIC needed even after HTTP/2 introduced multiplexing?
3. What is the responsibility boundary between HTTP/3 and QUIC?
4. How do sessions and JWT differ in where authentication state lives?
5. What trade-off does caching introduce?
6. Why is HTTP body compression different from HPACK/QPACK?
7. Why is WebSocket a better fit than WebRTC for many server-backed chat systems?
8. Why is WebRTC a better fit for real-time video/audio?
9. Design a chat application with video calls. Which role would HTTP, WebSocket, WebRTC, cache, database, and message broker play?
10. When designing a new system, what questions should you ask before choosing a communication technology?

## Preview

The HTTP module is now complete. The next module will move beyond HTTP into the next systems layer according to the roadmap.
