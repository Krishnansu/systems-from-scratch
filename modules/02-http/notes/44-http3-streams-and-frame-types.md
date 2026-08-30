# Lesson 44 — HTTP/3 Streams & Frame Types

## 1. HTTP/3 Layering

HTTP/3 runs on top of QUIC:

```text
HTTP/3
  |
  | HTTP/3 frames
  v
QUIC streams
  |
  | QUIC frames / packets
  v
QUIC transport
  |
  v
UDP
```

HTTP/3 provides HTTP semantics, while QUIC provides transport functionality such as streams, reliability, flow control, congestion control, loss detection, and packet protection.

## 2. HTTP/3 Uses QUIC Streams

HTTP/3 does not create an independent transport multiplexing mechanism. It uses QUIC's native streams.

Conceptually:

```text
QUIC Connection
       |
       +---- Request Stream
       |
       +---- Request Stream
       |
       +---- Request Stream
       |
       +---- Control Stream
```

Each HTTP request/response exchange can use its own QUIC bidirectional stream.

## 3. Request Streams

Request streams are bidirectional because both endpoints need to send data:

```text
Client                         Server
  |                              |
  |------ HTTP Request --------->|
  |                              |
  |<----- HTTP Response ---------|
  |                              |
```

A request stream can contain HTTP/3 frames such as `HEADERS` and `DATA`.

For example:

```text
Request Stream
      |
      +---- HEADERS
      |
      +---- DATA
      |
      +---- DATA
```

A GET request with no body may contain only a HEADERS frame on the request side.

## 4. HTTP/3 Control Stream

Connection-level HTTP information is carried on a dedicated unidirectional control stream.

An important control-stream frame is `SETTINGS`.

```text
QUIC Connection
       |
       +---- Request Stream
       +---- Request Stream
       +---- Control Stream
                         |
                         +---- SETTINGS
```

The SETTINGS frame is the first frame on the HTTP/3 control stream.

## 5. Unidirectional Streams

HTTP/3 also uses QUIC unidirectional streams for specialized purposes.

Important examples include:

- Control stream
- QPACK encoder stream
- QPACK decoder stream

A unidirectional stream has a single sender:

```text
Client --------------------> Server
```

or:

```text
Server --------------------> Client
```

## 6. Important HTTP/3 Frames

Important HTTP/3 frame types include:

- `HEADERS`
- `DATA`
- `SETTINGS`
- `CANCEL_PUSH`
- `PUSH_PROMISE`
- `GOAWAY`
- `MAX_PUSH_ID`
- `PRIORITY_UPDATE`

For the basic mental model, `HEADERS`, `DATA`, `SETTINGS`, and `GOAWAY` are especially important.

### HEADERS

Carries HTTP header information.

Example request:

```text
HEADERS
  :method = GET
  :scheme = https
  :authority = example.com
  :path = /index.html
```

The header block is encoded using QPACK.

### DATA

Carries HTTP message content.

```text
HEADERS
  :status = 200
  content-type = text/html

DATA
  <html>...
```

### SETTINGS

Communicates HTTP/3 connection-level configuration and appears on the control stream.

### GOAWAY

Allows an endpoint to gracefully stop accepting new requests while existing work is handled according to HTTP/3 semantics.

## 7. HTTP/3 Frame vs QUIC Frame

These are different framing layers.

```text
HTTP/3 HEADERS or DATA
          |
          v
     QUIC stream bytes
          |
          v
   QUIC STREAM frame
          |
          v
      QUIC packet
          |
          v
          UDP
```

An HTTP/3 `DATA` frame means:

> These bytes are HTTP message body content.

A QUIC `STREAM` frame means:

> These bytes belong to a particular QUIC stream, at a particular stream offset.

QUIC does not understand whether the stream bytes represent HTTP/3 HEADERS, DATA, or some other application-level structure.

## 8. HTTP/3 and QUIC Stream Independence

Suppose a browser requests three resources:

```text
QUIC Connection
       |
       +---- Stream A -> /index.html
       |
       +---- Stream B -> /style.css
       |
       +---- Stream C -> /app.js
```

If Stream B experiences packet loss, QUIC does not require Stream A or Stream C to wait for the missing Stream B bytes.

```text
Stream A  ----✓---------✓---------✓
Stream B  ----✓----X----✓---------
Stream C  ----✓---------✓---------✓
```

This is a major architectural advantage HTTP/3 gets from QUIC.

## 9. End-to-End Request Journey

A request such as `GET /hello` follows this conceptual path:

```text
HTTP request
     |
     v
HTTP/3 HEADERS
     |
     v
QUIC request stream
     |
     v
QUIC STREAM frame
     |
     v
QUIC packet
     |
     v
UDP
     |
     v
Internet
```

At the server the process is reversed.

## 10. Key Takeaways

1. HTTP/3 runs directly over QUIC.
2. HTTP/3 uses QUIC streams for multiplexing.
3. Request/response exchanges use bidirectional streams.
4. HTTP/3 has a dedicated control stream.
5. QPACK uses dedicated unidirectional streams.
6. `HEADERS` carries HTTP headers.
7. `DATA` carries HTTP message content.
8. `SETTINGS` carries connection-level HTTP configuration.
9. HTTP/3 frames and QUIC frames are different layers.
10. QUIC provides the stream-level transport machinery that HTTP/3 builds upon.
