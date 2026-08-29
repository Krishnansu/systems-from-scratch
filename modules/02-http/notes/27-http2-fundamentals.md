# Lesson 25 - HTTP/2 Fundamentals

## What I Learned

HTTP/2 changes how HTTP is represented and transported. Instead of the textual request/response representation used by HTTP/1.1, HTTP/2 uses binary frames.

HTTP/2 introduces logical streams inside a single TCP connection. Each stream represents an independent logical HTTP exchange, and frames belonging to different streams can be interleaved.

## HTTP/2 Architecture

```text
One TCP Connection
        |
        v
      HTTP/2
        |
   +----+----+----+
   |         |    |
Stream 1  Stream 3  Stream 5
   |         |    |
 Frames    Frames Frames
```

## Binary Framing

Conceptually, an HTTP/2 frame contains:

```text
+----------------------+
| Length               |
+----------------------+
| Type                 |
+----------------------+
| Flags                |
+----------------------+
| Stream ID            |
+----------------------+
| Payload              |
+----------------------+
```

The important fields are length, type, flags, stream ID and payload.

## Streams

A stream is a logical communication channel within an HTTP/2 connection.

```text
TCP Connection
      |
      ├── Stream 1
      ├── Stream 3
      ├── Stream 5
      └── Stream 7
```

A stream contains frames.

```text
Stream 1
   ├── HEADERS
   ├── DATA
   └── DATA
```

## Multiplexing

Frames from different streams can be interleaved over the same TCP connection.

```text
S1 S3 S5 S1 S5 S3 S1 S5
```

The Stream ID allows HTTP/2 to associate each frame with the correct logical stream.

## HTTP/2 Request

An HTTP/1.1 request such as:

```http
GET /products/123 HTTP/1.1
Host: example.com
```

is represented conceptually in HTTP/2 using a HEADERS frame containing pseudo-headers:

```text
:method: GET
:scheme: https
:authority: example.com
:path: /products/123
```

HTTP/2 does not use the textual HTTP/1.1 request line.

## Important Frames

The most important frames to understand initially are:

- HEADERS — carries HTTP header information.
- DATA — carries message body data.
- SETTINGS — communicates HTTP/2 configuration.
- WINDOW_UPDATE — manages flow control.
- PING — connection health/latency related control.
- GOAWAY — indicates connection shutdown.

## Key Insight

HTTP/2 retains HTTP semantics such as methods, headers, status codes and bodies, but changes their wire representation into a binary framing system with multiplexed streams.

## Important Limitation

HTTP/2 still runs over TCP.

```text
HTTP/2
  |
  ├── Stream 1
  ├── Stream 3
  └── Stream 5
          |
          v
         TCP
          |
          v
   Ordered byte stream
```

Therefore HTTP/2 solves HTTP-level multiplexing problems but does not completely eliminate TCP-level head-of-line blocking.