# Lesson 46 — HTTP/3 Request/Response Lifecycle

## 1. The Big Picture

HTTP/3 runs on top of QUIC. A complete HTTP/3 request therefore passes through several layers:

```text
Browser
   |
   v
DNS
   |
   v
Server IP / HTTP/3 discovery
   |
   v
QUIC connection
   |
   v
HTTP/3
   |
   v
Request / Response
```

The important idea is that each layer has a different responsibility.

## 2. Step 1 — DNS and HTTP/3 Discovery

The browser first needs to discover where the server is and, in modern deployments, whether HTTP/3 is available.

Conceptually:

```text
Browser
   |
   | example.com?
   v
DNS
   |
   | Server IP + service information
   v
Browser
```

DNS and HTTP/3 discovery are outside the HTTP/3 transport itself, but they establish the information needed to connect.

## 3. Step 2 — Establish the QUIC Connection

The client establishes a QUIC connection with the server.

QUIC integrates TLS 1.3 into the transport handshake and establishes the cryptographic state needed for secure communication.

A simplified handshake looks like:

```text
Client                         Server
  |                              |
  |-------- Initial ------------>|
  |                              |
  |<------- Initial/Handshake ---|
  |                              |
  |-------- Handshake ---------->|
  |                              |
  |<------ 1-RTT packets --------|
  |                              |
```

The exact packet exchange is more detailed, but the key point is that HTTP/3 uses the resulting secure QUIC connection rather than establishing a separate TCP connection.

## 4. Step 3 — HTTP/3 Control Stream

Once HTTP/3 is operating over the QUIC connection, each endpoint establishes its HTTP/3 control stream.

The control stream carries connection-level HTTP/3 information.

A `SETTINGS` frame is exchanged on the control stream.

```text
QUIC Connection
       |
       +---- Control Stream
                 |
                 +---- SETTINGS
```

The control stream is unidirectional.

## 5. Step 4 — QPACK

HTTP/3 uses QPACK to compress HTTP header fields.

QPACK has:

- A predefined static table
- A connection-specific dynamic table
- An encoder stream
- A decoder stream

The static table is already known by both endpoints and does not get dynamically updated during a connection.

The dynamic table can change during the connection and therefore requires synchronization.

```text
HTTP Headers
     |
     v
   QPACK
     |
     v
Compressed Header Block
```

## 6. Step 5 — Create a Request Stream

An HTTP/3 request/response exchange uses a bidirectional QUIC stream.

For example:

```text
QUIC Connection
       |
       +---- Stream 4
               |
               v
          HTTP Request
```

The same stream can carry the request from client to server and the response from server to client.

```text
Client ------------------------> Server
             Request

Client <------------------------ Server
             Response
```

## 7. Step 6 — Encode the Request Headers

Suppose the browser wants:

```http
GET /index.html
```

with headers such as:

```text
:method: GET
:scheme: https
:authority: example.com
:path: /index.html
```

HTTP/3 represents these headers in a `HEADERS` frame.

The header block is encoded using QPACK.

```text
HTTP headers
     |
     v
   QPACK
     |
     v
Compressed header block
     |
     v
HTTP/3 HEADERS frame
```

Common fields may use references to the QPACK static table, while dynamic entries can be used when appropriate.

## 8. Step 7 — HTTP/3 Frames Become QUIC Stream Bytes

This is an important layering boundary.

The HTTP/3 `HEADERS` frame is an HTTP/3-level structure. QUIC does not understand its HTTP meaning.

Instead, the HTTP/3 frame is serialized into bytes and those bytes are carried on the QUIC stream.

```text
HTTP/3 HEADERS
       |
       v
Serialized bytes
       |
       v
QUIC Stream 4
       |
       v
QUIC STREAM frame
       |
       v
QUIC packet
```

Similarly, HTTP/3 `DATA` frames are simply bytes from QUIC's perspective.

## 9. Step 8 — QUIC Packetization and Transmission

QUIC takes stream data and places it into QUIC packets.

Conceptually:

```text
HTTP/3
   |
   v
QUIC Stream 4
   |
   v
QUIC STREAM frame
   |
   v
Encryption
   |
   v
QUIC packet
   |
   v
UDP
   |
   v
IP / Network
```

QUIC is responsible for transport-level concerns such as:

- Reliability
- Packet loss detection
- Retransmission
- Flow control
- Congestion control
- Stream ordering
- Encryption
- Connection migration

HTTP/3 does not reimplement these mechanisms.

## 10. Step 9 — Server Receives the Request

The server processes the received data in the reverse direction through the protocol stack.

```text
UDP
 |
 v
QUIC packet
 |
 v
Decrypt / process QUIC
 |
 v
QUIC STREAM frame
 |
 v
QUIC Stream 4
 |
 v
HTTP/3 HEADERS
 |
 v
QPACK decode
 |
 v
HTTP headers
 |
 v
HTTP request
```

The application can now process:

```text
GET /index.html
```

## 11. Step 10 — Server Generates a Response

Suppose the server responds with:

```text
:status: 200
content-type: text/html
```

and a body:

```html
<html>
  <body>Hello!</body>
</html>
```

HTTP/3 represents this conceptually as:

```text
HEADERS
  :status = 200
  content-type = text/html

DATA
  <html>...
```

The response headers are compressed using QPACK.

## 12. Step 11 — Response Travels on the Same Request Stream

The server sends the response back on the same bidirectional request stream.

```text
Client                         Server
  |                              |
  |------ Request Stream ------->|
  |         HEADERS              |
  |                              |
  |<----- Request Stream --------|
  |         HEADERS              |
  |         DATA                 |
  |         DATA                 |
  |                              |
```

The stream is bidirectional, so both request and response data can use it.

## 13. Step 12 — QUIC Handles Transport Details

The HTTP/3 layer does not need to know whether packets are lost or reordered at the network level.

QUIC handles this below HTTP/3.

For example:

```text
Packet 100 -> HEADERS    ✓
Packet 101 -> DATA A     ✓
Packet 102 -> DATA B     X
Packet 103 -> DATA C     ✓
```

QUIC detects that data associated with the lost packet is missing and retransmits the necessary stream data.

Another QUIC stream can continue independently:

```text
Stream 4  -> waiting for missing data
Stream 8  -> continues
Stream 12 -> continues
```

This is the transport-level stream independence that avoids TCP's single ordered byte-stream head-of-line blocking.

## 14. Step 13 — Flow Control

QUIC flow control prevents a sender from overwhelming the receiver with more data than the receiver is prepared to buffer/process.

There are two important scopes:

```text
QUIC Flow Control
       |
       +---- Connection-level
       |
       +---- Stream-level
```

The receiver can advertise more available capacity using mechanisms such as `MAX_DATA` and `MAX_STREAM_DATA`.

This is a QUIC responsibility, not an HTTP/3 responsibility.

## 15. Step 14 — Congestion Control

Flow control and congestion control solve different problems.

Flow control asks:

> Can the receiver accept more data?

Congestion control asks:

> Can the network safely carry more data?

```text
QUIC
 |
 +---- Flow control
 |       |
 |       v
 |   Receiver capacity
 |
 +---- Congestion control
         |
         v
     Network capacity
```

Both operate below HTTP/3.

## 16. QPACK Dependencies During the Lifecycle

A response header block may reference a dynamic QPACK table entry that the decoder has not processed yet.

Conceptually:

```text
Response HEADERS
       |
       v
     QPACK
       |
       v
Needs Dynamic Entry #50
       |
       v
Is entry available?
     /       \
   Yes        No
    |          |
    v          v
 Decode      Wait
```

This can temporarily block the affected HTTP/3 stream.

However, this is different from TCP head-of-line blocking:

```text
Stream 4 -> blocked by its QPACK dependency
Stream 8 -> can continue
Stream 12 -> can continue
```

QUIC provides independent transport streams, while QPACK manages its own application-level dependencies.

## 17. Complete End-to-End Lifecycle

A simplified complete request/response path is:

```text
                         BROWSER
                            |
                            v
                           DNS
                            |
                            v
                    Server IP / HTTP/3
                            |
                            v
                    QUIC Connection
                            |
             +--------------+--------------+
             |              |              |
             v              v              v
         Control        QPACK streams   Request
          Stream                           Stream
             |                              |
          SETTINGS                        HEADERS
                                            |
                                            v
                                      QPACK encode
                                            |
                                            v
                                      QUIC STREAM
                                            |
                                            v
                                        QUIC packet
                                            |
                                            v
                                           UDP
                                            |
                                            v
                                         Network
                                            |
                                            v
                                          Server
                                            |
                                            v
                                      QUIC processing
                                            |
                                            v
                                      HTTP/3 HEADERS
                                            |
                                            v
                                        QPACK decode
                                            |
                                            v
                                      HTTP request
                                            |
                                            v
                                        Application
                                            |
                                            v
                                      HTTP response
                                            |
                                     +------+------+
                                     |             |
                                     v             v
                                  HEADERS        DATA
                                     |             |
                                     +------+------+
                                            |
                                            v
                                      QUIC Stream
                                            |
                                            v
                                      QUIC packets
                                            |
                                            v
                                           UDP
                                            |
                                            v
                                          Client
                                            |
                                            v
                                         Browser
```

## 18. Responsibility by Layer

| Layer | Primary responsibility |
|---|---|
| DNS | Resolve the service/server information needed to connect |
| HTTP/3 | HTTP semantics, requests, responses, HTTP/3 frames |
| QPACK | HTTP header compression |
| QUIC streams | Independent logical byte streams |
| QUIC | Reliability, loss detection, flow control, congestion control, encryption, migration |
| UDP | Datagram transport |
| IP | Network routing |

This separation is one of the most important architectural ideas in HTTP/3.

## 19. The Most Important Architectural Insight

HTTP/3 does not need to solve transport problems itself because QUIC already provides the transport abstraction it needs.

```text
HTTP/3
   |
   | HTTP semantics
   v
QPACK
   |
   | Header compression
   v
QUIC
   |
   | Streams, reliability, flow control,
   | congestion control, encryption
   v
UDP
   |
   v
Network
```

This allows HTTP/3 to focus on HTTP while QUIC handles the transport.

## 20. Key Takeaways

1. DNS provides the information needed to locate the server and discover HTTP/3 support.
2. QUIC establishes the secure transport connection.
3. HTTP/3 uses a control stream for connection-level HTTP/3 information such as SETTINGS.
4. HTTP requests and responses use bidirectional QUIC streams.
5. HTTP/3 headers are represented in HEADERS frames and compressed with QPACK.
6. HTTP/3 DATA and HEADERS frames become bytes carried by QUIC streams.
7. QUIC STREAM frames carry those bytes and QUIC packets transport them over UDP.
8. The server reverses the process to recover the HTTP request.
9. The response travels back through HTTP/3 and QUIC on the request stream.
10. QUIC handles reliability, loss recovery, flow control, congestion control, encryption, and connection migration.
11. QPACK can introduce application-level header dependencies, but these do not recreate TCP's global transport-level head-of-line blocking.
12. The key architectural principle is separation of concerns: HTTP/3 handles HTTP semantics while QUIC handles transport.
