# Lesson 52 — Build an HTTP/3 Request From Scratch

## Objectives

- Trace one HTTP/3 request through the complete protocol stack.
- Understand how HTTP/3 frames are carried by QUIC streams.
- Understand how QPACK fits into the request path.
- Distinguish HTTP/3 frames from QUIC frames and packets.
- Understand encapsulation and decapsulation across HTTP/3 → QUIC → UDP → IP.

## Prerequisites

- HTTP/3 fundamentals
- QUIC streams and packets
- QPACK
- HTTP/3 request/response lifecycle
- HTTP/1.1 vs HTTP/2 vs HTTP/3 evolution

## Theory

A request such as:

```text
GET https://example.com/index.html
```

starts as HTTP semantics and is progressively represented by lower protocol layers.

The conceptual path is:

```text
HTTP request
    ↓
HTTP/3 HEADERS frame
    ↓
QPACK-compressed header block
    ↓
QUIC stream
    ↓
QUIC STREAM frame
    ↓
QUIC packet
    ↓
UDP datagram
    ↓
IP packet
    ↓
Network
```

The receiver performs the reverse process.

## HTTP/3 Layer

The request is represented using HTTP/3 frames. A simple GET request primarily needs a `HEADERS` frame because it normally has no request body.

Conceptually:

```text
HEADERS
  ├── :method = GET
  ├── :scheme = https
  ├── :authority = example.com
  └── :path = /index.html
```

HTTP/3 is responsible for HTTP semantics and HTTP/3 framing. It does not need to understand IP routing or UDP delivery.

## QPACK Layer

The HTTP headers are compressed using QPACK.

QPACK can represent common fields using the static table and can use the dynamic table for reusable connection-specific entries.

```text
HTTP headers
     ↓
   QPACK
     ↓
compressed header block
```

QPACK exists because HTTP/3 operates over independent QUIC streams rather than TCP's single ordered byte stream.

## QUIC Stream Layer

The compressed HTTP/3 frame bytes are written to a QUIC request stream.

```text
QUIC Stream 7

+-----------------------------+
| HTTP/3 HEADERS frame        |
| QPACK-compressed headers    |
+-----------------------------+
```

QUIC does not need to understand what `/index.html` means. It treats the HTTP/3 data as stream bytes.

## QUIC STREAM Frame

QUIC carries stream data using `STREAM` frames.

```text
QUIC STREAM frame
  ├── Stream ID = 7
  ├── Offset = 0
  ├── Length = N
  └── Data = HTTP/3 frame bytes
```

This is different from an HTTP/3 `DATA` frame or `HEADERS` frame.

```text
HTTP/3 layer:
  HEADERS
  DATA
  SETTINGS
  GOAWAY

QUIC layer:
  STREAM
  ACK
  CRYPTO
  MAX_DATA
  MAX_STREAM_DATA
  etc.
```

An HTTP/3 frame can therefore be carried inside a QUIC `STREAM` frame.

## QUIC Packet

QUIC packages its frames into encrypted QUIC packets.

Conceptually:

```text
+---------------------------+
| QUIC Header               |
| Connection ID             |
| Packet Number             |
+---------------------------+
| Encrypted QUIC Frames     |
|   STREAM frame             |
|     Stream ID = 7         |
|     HTTP/3 bytes           |
+---------------------------+
```

QUIC adds transport-level information and provides encryption integration, reliability, loss detection, flow control, congestion control, and stream management.

## UDP and IP

The QUIC packet becomes the payload of a UDP datagram.

```text
+----------------------+
| UDP Header           |
+----------------------+
| QUIC Packet          |
+----------------------+
```

The UDP datagram is then carried inside an IP packet.

```text
+----------------------+
| IP Header            |
+----------------------+
| UDP Header           |
+----------------------+
| QUIC Packet          |
+----------------------+
```

UDP and IP do not understand HTTP/3 or QPACK.

## Network Journey

The packet can then travel through the network:

```text
Browser
  ↓
Operating system
  ↓
Wi-Fi / Ethernet
  ↓
Router
  ↓
ISP
  ↓
Internet
  ↓
Server network
  ↓
Server
```

Routers primarily make forwarding decisions using network-layer information. They do not need to understand the HTTP request.

## Server Decapsulation

The server reverses the encapsulation process:

```text
IP packet
    ↓
UDP datagram
    ↓
QUIC packet
    ↓
QUIC STREAM frame
    ↓
QUIC stream bytes
    ↓
HTTP/3 HEADERS frame
    ↓
QPACK decoding
    ↓
HTTP request
```

The HTTP server eventually reconstructs:

```text
GET /index.html
```

along with its decoded headers.

## Response Path

The response follows the reverse direction.

```text
HTTP response
     ↓
HTTP/3 HEADERS / DATA
     ↓
QPACK compression where applicable
     ↓
QUIC stream
     ↓
QUIC STREAM frames
     ↓
QUIC packets
     ↓
UDP
     ↓
IP
     ↓
Network
     ↓
Client
```

## Encapsulation

The complete downward path is an example of encapsulation:

```text
HTTP/3 data
    ↓
+-----------------------+
| QUIC STREAM frame     |
|   HTTP/3 data         |
+-----------------------+
          ↓
+-----------------------+
| QUIC packet           |
|   QUIC frames         |
+-----------------------+
          ↓
+-----------------------+
| UDP datagram          |
|   QUIC packet         |
+-----------------------+
          ↓
+-----------------------+
| IP packet             |
|   UDP datagram        |
+-----------------------+
```

The receiver performs decapsulation in the opposite order.

## Real World Example

For a browser request:

```text
GET https://example.com/index.html
```

The important conceptual transformations are:

```text
HTTP semantics
      ↓
HTTP/3 HEADERS
      ↓
QPACK compressed headers
      ↓
QUIC Stream 7
      ↓
QUIC STREAM frame
      ↓
QUIC packet
      ↓
UDP datagram
      ↓
IP packet
      ↓
Network
```

The exact packetization may differ in a real implementation. One HTTP/3 frame can span multiple QUIC packets, and a QUIC packet can contain multiple QUIC frames.

## Deep Dive

### Layer Responsibilities

```text
HTTP/3
  → HTTP semantics and HTTP/3 frames

QPACK
  → HTTP header compression

QUIC
  → streams, packets, reliability, loss recovery,
    flow control, congestion control, connection management

UDP
  → datagram transport

IP
  → packet addressing and routing
```

Each layer is intentionally unaware of details belonging to higher layers.

### Important Distinction

Do not confuse:

```text
HTTP/3 DATA frame
```

with:

```text
QUIC STREAM frame
```

The former is an HTTP/3 message-level frame. The latter is a QUIC transport frame carrying bytes belonging to a QUIC stream.

### Key Architectural Insight

One HTTP request does not remain the same representation as it travels through the stack. Each layer wraps the information from the layer above with its own protocol metadata.

This is the practical meaning of protocol layering and encapsulation.

## Hands-on Exercise

Use a packet capture or protocol-analysis tool to inspect an HTTP/3 connection if available.

Try to identify:

1. UDP packets carrying QUIC.
2. QUIC packet headers and packet numbers.
3. QUIC `STREAM` frames.
4. HTTP/3 frames inside stream data.
5. The separation between transport-level and HTTP-level information.

The goal is not to decode every encrypted field manually, but to map the observed packets back to the conceptual stack.

## Common Misconceptions

### UDP makes HTTP/3 unreliable

False. QUIC runs over UDP but implements reliability, loss recovery, flow control, congestion control, and stream management itself.

### HTTP/3 directly sends packets through UDP

False. HTTP/3 sits above QUIC.

```text
HTTP/3 → QUIC → UDP → IP
```

### HTTP/3 DATA and QUIC STREAM are the same frame

False. They belong to different protocol layers.

### Routers understand HTTP requests

Usually false. Routing decisions are primarily based on network-layer information. A router does not need to understand `GET /index.html`.

## Summary

A single HTTP/3 request passes through several layers before reaching the server. HTTP/3 creates HTTP-level frames, QPACK compresses headers, QUIC carries the resulting bytes on streams and packets, UDP transports QUIC datagrams, and IP provides network-layer delivery. The server reverses these transformations through decapsulation.

## Key Takeaways

1. HTTP/3 sits above QUIC.
2. QPACK compresses HTTP/3 headers.
3. HTTP/3 frames are carried as bytes in QUIC streams.
4. QUIC `STREAM` frames are transport frames and are distinct from HTTP/3 frames.
5. QUIC packets are carried inside UDP datagrams.
6. UDP datagrams are carried inside IP packets.
7. Each layer adds its own metadata through encapsulation.
8. The server reverses the process through decapsulation.
9. One HTTP request can become multiple frames and packets during transmission.
10. The complete stack is:

```text
HTTP/3
  ↓
QUIC
  ↓
UDP
  ↓
IP
  ↓
Network
```

## Reflection Questions

1. Why does HTTP/3 need QUIC instead of talking directly to UDP?
2. What is the difference between an HTTP/3 `DATA` frame and a QUIC `STREAM` frame?
3. Where does QPACK operate in the request path?
4. Which layer is responsible for packet loss recovery?
5. What information does a router need to forward the packet without understanding HTTP?

## What's Next

The HTTP/3 section is now consolidated. The next stage will move into the next major systems topic in the roadmap while continuing to connect concepts back to the networking and HTTP foundations built so far.
