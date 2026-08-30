# Lesson 49 — HTTP/3 ↔ QUIC Integration

## Objectives

- Establish the exact boundary between HTTP/3 and QUIC.
- Distinguish HTTP/3 frames from QUIC frames.
- Understand how HTTP/3 bytes travel through QUIC to the network.
- Identify which responsibilities belong to HTTP/3 and which belong to QUIC.
- Understand the layering of QPACK, HTTP/3 streams, QUIC streams, packets, and UDP.

## Concept Summary

HTTP/3 defines HTTP semantics and application-layer framing. QUIC provides the secure transport underneath it.

The core mental model is:

```text
HTTP/3 → WHAT the application data means
QUIC   → HOW those bytes are transported
```

## Core Architecture

```text
Application
    |
    v
HTTP/3
    |
    | HTTP/3 bytes / frames
    v
QUIC streams
    |
    | QUIC STREAM frames
    v
QUIC packets
    |
    v
UDP datagrams
    |
    v
IP
    |
    v
Network
```

## HTTP/3 Frames vs QUIC Frames

HTTP/3 defines frames such as:

- `HEADERS`
- `DATA`
- `SETTINGS`
- `GOAWAY`
- `PUSH_PROMISE`
- `PRIORITY_UPDATE`

QUIC defines frames such as:

- `STREAM`
- `ACK`
- `CRYPTO`
- `RESET_STREAM`
- `STOP_SENDING`
- `PATH_CHALLENGE`
- `PATH_RESPONSE`
- `CONNECTION_CLOSE`
- flow-control frames

An HTTP/3 frame is application-protocol data carried by QUIC. It is not itself a QUIC frame.

## Example: HTTP/3 DATA Inside QUIC

Suppose an HTTP response body contains `Hello!`.

```text
HTTP/3 DATA frame
        |
        | bytes
        v
QUIC STREAM frame
        |
        v
QUIC packet
        |
        v
UDP datagram
```

The QUIC layer does not need to understand that the bytes represent an HTTP/3 `DATA` frame.

## QPACK Layering

QPACK belongs to HTTP/3.

```text
HTTP headers
     |
     v
QPACK encoding
     |
     v
HTTP/3 HEADERS frame
     |
     v
QUIC stream
```

QPACK encoder and decoder streams are HTTP/3 concepts transported using QUIC unidirectional streams.

## Control Stream

HTTP/3 defines a control stream carrying connection-level HTTP/3 information such as `SETTINGS` and `GOAWAY`.

```text
HTTP/3 Control Stream
        |
        v
QUIC unidirectional stream
```

HTTP/3 defines the meaning of the bytes; QUIC provides the transport stream.

## Responsibility Boundary

### HTTP/3 owns

- HTTP methods and semantics
- Request and response structure
- HTTP headers
- QPACK
- HTTP/3 frames
- HTTP status codes
- HTTP/3 error codes
- HTTP/3 control information

### QUIC owns

- Transport streams
- QUIC frames
- Packetization
- Acknowledgements
- Loss detection and recovery
- Flow control
- Congestion control
- Connection IDs
- Connection migration
- Path validation
- Transport-level stream termination
- Transport connection termination
- TLS 1.3 handshake integration

## What QUIC Does Not Need to Know

QUIC generally treats HTTP/3 data as bytes. It does not need to understand:

```text
GET /index.html
404 Not Found
Content-Type: text/html
```

Those meanings belong to HTTP/3.

## What HTTP/3 Does Not Need to Know

HTTP/3 does not need to manage:

```text
Packet numbers
ACK frames
RTT estimation
Congestion window
Packet loss
PATH_CHALLENGE
Connection IDs
```

Those belong to QUIC.

## Loss Recovery

If a packet carrying stream data is lost, QUIC detects the loss and retransmits the lost stream data in a later packet. HTTP/3 does not need to know the original packet number.

```text
Packet 101
    |
    X lost
    |
    v
QUIC detects lost stream data
    |
    v
New packet carries the data again
```

## Connection Migration

Connection migration is also handled by QUIC.

```text
Old network path
       |
       X
       |
       v
QUIC path validation
       |
       v
New network path
       |
       v
Existing HTTP/3 streams continue
```

HTTP/3 does not need to rebuild the HTTP requests merely because the underlying network path changed.

## Production Perspective

The separation of responsibilities is a major architectural benefit of HTTP/3 over QUIC. HTTP/3 can focus on application protocol behavior while QUIC handles secure, multiplexed transport concerns.

This separation also explains why HTTP/3 can benefit from QUIC capabilities such as independent streams and connection migration without embedding transport-specific logic into HTTP itself.

## Common Mistakes

- Treating an HTTP/3 `DATA` frame as a QUIC `STREAM` frame.
- Thinking QPACK is part of QUIC.
- Thinking HTTP/3 manages congestion control.
- Thinking QUIC understands HTTP methods or status codes.
- Thinking connection migration requires HTTP/3 requests to restart.
- Confusing an HTTP/3 stream with the QUIC transport primitive that carries it.

## Key Takeaways

1. HTTP/3 defines HTTP semantics and application-layer framing.
2. QUIC provides the transport underneath HTTP/3.
3. HTTP/3 frames are bytes carried inside QUIC streams, commonly via QUIC `STREAM` frames.
4. `DATA` is an HTTP/3 frame; `STREAM` is a QUIC frame.
5. QPACK belongs to HTTP/3.
6. HTTP/3 control and QPACK streams are transported using QUIC streams.
7. QUIC handles loss recovery, flow control, congestion control, and connection migration.
8. HTTP/3 does not need to understand packet-level transport behavior.
9. The core layering model is `HTTP/3 → QUIC → UDP → IP`.

## Reflection Questions

- If a QUIC packet is lost, why does HTTP/3 not need to know which packet was lost?
- Why can QUIC migrate a connection without HTTP/3 rebuilding every request?
- What is the difference between an HTTP/3 stream and a QUIC transport stream?

## Related Lessons

- Lesson 43 — HTTP/3 Fundamentals
- Lesson 44 — HTTP/3 Streams & Frame Types
- Lesson 45 — QPACK: HTTP/3 Header Compression
- Lesson 46 — HTTP/3 Request/Response Lifecycle
- Lesson 47 — HTTP/3 Error Handling & Connection Shutdown
- Lesson 50 — HTTP/3 Performance & Trade-offs
