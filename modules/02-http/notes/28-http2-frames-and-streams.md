# Lesson 26 - HTTP/2 Frames and Streams

## What I Learned

HTTP/2 does not send a request as one large textual message. It breaks communication into binary frames.

Frames contain information such as length, type, flags, stream ID and payload.

The Stream ID allows frames belonging to different logical HTTP exchanges to be interleaved over the same TCP connection.

## Frame Model

```text
HTTP/2 Connection
       |
       v
     Frames
       |
   +---+---+---+
   |   |   |   |
  S1  S3  S5  S1
```

## HEADERS and DATA

A request can conceptually be represented as:

```text
HEADERS
   |
   ├── :method = GET
   ├── :path = /products/123
   └── :authority = example.com
```

A request or response containing a body can use DATA frames:

```text
HEADERS
   |
   v
DATA
   |
   v
DATA
```

Large bodies can therefore be split across multiple DATA frames.

## Stream IDs

Every stream has an identifier. Frames use that identifier to associate themselves with the correct logical exchange.

```text
Frame → Stream ID 1 → Stream 1
Frame → Stream ID 3 → Stream 3
Frame → Stream ID 5 → Stream 5
```

Stream ID 0 is used for connection-level frames rather than a normal HTTP request stream.

## Pseudo-Headers

HTTP/2 represents core request information using pseudo-headers such as:

```text
:method
:path
:scheme
:authority
```

These replace concepts that HTTP/1.1 represented through the request line and Host header.

## Stream Lifecycle

A stream represents the lifetime of one logical HTTP exchange.

```text
Idle
  |
  v
Open
  |
  v
Half-closed
  |
  v
Closed
```

A stream can finish while the underlying TCP connection remains open.

Therefore:

```text
TCP connection lifetime
        !=
HTTP/2 stream lifetime
```

## Multiplexing Example

Suppose:

```text
Stream 1 → HTML
Stream 3 → CSS
Stream 5 → JavaScript
```

Frames can be transmitted as:

```text
HEADERS(S1)
HEADERS(S3)
HEADERS(S5)
DATA(S1)
DATA(S3)
DATA(S5)
DATA(S1)
DATA(S5)
```

The receiver uses Stream IDs to reconstruct each logical stream.

## Key Insight

A stream is a logical communication channel. A frame is a unit of HTTP/2 data carried over the connection.

```text
TCP Connection
      |
      v
HTTP/2
      |
      ├── Stream 1 → Frames
      ├── Stream 3 → Frames
      └── Stream 5 → Frames
```

## TCP Limitation

Although HTTP/2 streams are independent at the HTTP layer, they share one TCP connection.

TCP still provides one ordered byte stream. A lost TCP segment can therefore delay delivery of later bytes even when those bytes belong to another HTTP/2 stream.

This is the transport-level head-of-line blocking problem that leads to QUIC.