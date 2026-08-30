# Lesson 47 — HTTP/3 Error Handling & Connection Shutdown

## 1. Errors Have Different Scopes

HTTP/3 runs over QUIC, so errors can occur at different layers and scopes.

```text
                 Failure
                    |
          +---------+---------+
          |                   |
       Stream              Connection
          |                   |
          |            +------+------+
          |            |             |
          v            v             v
      One request   HTTP/3        QUIC
                    connection    connection
```

A stream-level problem does not necessarily mean that the entire connection must be terminated.

## 2. QUIC Stream-Level Mechanisms

QUIC provides transport-level mechanisms for terminating or stopping streams.

### RESET_STREAM

`RESET_STREAM` terminates a QUIC stream.

```text
Client                         Server

Stream 4
  |                              |
  |<--------- DATA --------------|
  |<--------- DATA --------------|
  |                              |
  | RESET_STREAM                 |
  |----------------------------->|
  |                              |
```

`RESET_STREAM` is a QUIC transport mechanism, not an HTTP/3 frame.

### STOP_SENDING

`STOP_SENDING` tells the peer that the receiver no longer wants to receive data on a stream.

```text
Client                         Server

       Stream 4
          |
          |<------- DATA --------
          |<------- DATA --------
          |
          | STOP_SENDING
          |---------------------->
```

It is also a QUIC transport mechanism.

## 3. Why RESET_STREAM and STOP_SENDING Are Different

A bidirectional stream has data flowing in both directions.

```text
Receiver
   |
   | STOP_SENDING
   |-------------------->
   |                     Sender
   |                        |
   |                     RESET_STREAM
   |<-----------------------|
```

Conceptually:

- `STOP_SENDING`: I no longer want you to send me data on this stream.
- `RESET_STREAM`: terminate/reset the stream's sending state.

## 4. HTTP/3 Error Codes

HTTP/3 defines application-level error codes such as:

```text
H3_NO_ERROR
H3_GENERAL_PROTOCOL_ERROR
H3_INTERNAL_ERROR
H3_STREAM_CREATION_ERROR
H3_CLOSED_CRITICAL_STREAM
H3_FRAME_UNEXPECTED
H3_FRAME_ERROR
H3_EXCESSIVE_LOAD
H3_ID_ERROR
H3_SETTINGS_ERROR
H3_MISSING_SETTINGS
H3_REQUEST_REJECTED
H3_REQUEST_CANCELLED
H3_REQUEST_INCOMPLETE
H3_MESSAGE_ERROR
H3_CONNECT_ERROR
H3_VERSION_FALLBACK
```

These describe HTTP/3-level protocol conditions. They are different from HTTP status codes such as `200`, `404`, and `500`.

## 5. HTTP Status Codes vs HTTP/3 Error Codes

HTTP status codes answer:

> What happened with the HTTP request?

Examples:

```text
200 OK
404 Not Found
500 Internal Server Error
```

They normally appear in an HTTP response HEADERS frame.

HTTP/3 error codes answer a different question:

> What went wrong with the HTTP/3 protocol or operation?

For example:

```text
H3_FRAME_UNEXPECTED
H3_SETTINGS_ERROR
H3_CLOSED_CRITICAL_STREAM
```

The distinction is:

```text
HTTP STATUS
     |
     v
HTTP request semantics
     |
     +---- 2xx
     +---- 4xx
     +---- 5xx

HTTP/3 ERROR
     |
     v
HTTP/3 protocol/stream operation
     |
     +---- H3_FRAME_UNEXPECTED
     +---- H3_SETTINGS_ERROR
     +---- H3_MISSING_SETTINGS
```

A `404` is not an HTTP/3 protocol error. It is a valid HTTP response indicating that a resource was not found.

## 6. H3_REQUEST_CANCELLED

`H3_REQUEST_CANCELLED` communicates the HTTP/3-level meaning that a request has been cancelled.

The transport mechanism used to terminate the associated stream is provided by QUIC.

```text
HTTP/3 meaning
      |
      v
H3_REQUEST_CANCELLED
      |
      v
QUIC stream termination
```

This demonstrates the separation between HTTP semantics and transport mechanics.

## 7. Connection-Level Shutdown: GOAWAY

HTTP/3 uses `GOAWAY` for graceful HTTP-level shutdown.

A server may have several active requests:

```text
QUIC Connection
       |
       +---- Stream 4  → request A
       +---- Stream 8  → request B
       +---- Stream 12 → request C
```

If the server wants to stop accepting new work, it can send `GOAWAY`.

Conceptually:

```text
Client                         Server

Stream 4   -------------------->
Stream 8   -------------------->
Stream 12  -------------------->

          GOAWAY
<------------------------------

New requests stop
Existing appropriate work can finish
```

`GOAWAY` is an HTTP/3 mechanism, not a QUIC transport frame.

## 8. GOAWAY vs CONNECTION_CLOSE

These operate at different layers.

```text
GOAWAY
   |
   v
HTTP/3 graceful shutdown
```

while:

```text
CONNECTION_CLOSE
   |
   v
QUIC connection termination
```

Therefore:

- `GOAWAY` means stop creating new HTTP requests while allowing appropriate existing work to finish.
- `CONNECTION_CLOSE` terminates the underlying QUIC connection.

## 9. Graceful Shutdown Sequence

A simplified graceful shutdown can look like:

```text
HTTP/3
   |
   | GOAWAY
   v
Stop accepting new HTTP requests
   |
   v
Finish existing work
   |
   v
QUIC
   |
   | CONNECTION_CLOSE
   v
Close transport connection
```

## 10. Critical Streams

Not every HTTP/3 stream has the same importance.

The HTTP/3 control stream is critical to maintaining valid connection-level protocol state.

If a request stream fails:

```text
Stream 4  → ERROR
Stream 8  → continues
Stream 12 → continues
Stream 16 → continues
```

But if a critical HTTP/3 stream is unexpectedly closed, the entire HTTP/3 connection may no longer be usable.

```text
Critical HTTP/3 stream
        |
        v
Unexpectedly closed
        |
        v
H3_CLOSED_CRITICAL_STREAM
        |
        v
HTTP/3 connection failure
```

## 11. Connection Errors vs Stream Errors

The core distinction is:

```text
Stream error
    |
    v
One request/stream affected

Connection error
    |
    v
HTTP/3 connection affected
```

A request-specific error should normally be isolated to its stream. A fundamental HTTP/3 protocol violation can require connection termination.

## 12. QUIC CONNECTION_CLOSE

QUIC provides `CONNECTION_CLOSE` to terminate the QUIC connection.

It can represent a transport-level failure or an application-level failure.

For HTTP/3, the application error can carry an HTTP/3 error code.

```text
CONNECTION_CLOSE
      |
      +---- Transport error
      |
      +---- Application error
                 |
                 v
              H3_...
```

## 13. HTTP/2 Comparison

HTTP/2 also supports stream-level and connection-level shutdown mechanisms.

### HTTP/2 Stream Reset

HTTP/2 uses the `RST_STREAM` frame to terminate an individual HTTP/2 stream.

```text
HTTP/2 connection
       |
       +---- Stream 1 → request A
       +---- Stream 3 → request B
       +---- Stream 5 → request C

RST_STREAM(Stream 3)
       |
       v
Stream 3 terminated
```

The other streams can continue.

### HTTP/2 Graceful Shutdown

HTTP/2 uses `GOAWAY` for graceful connection shutdown.

```text
Client                         Server

Stream 1  -------------------->
Stream 3  -------------------->
Stream 5  -------------------->

          GOAWAY
<------------------------------

No new streams beyond the shutdown boundary
Existing appropriate streams can finish
```

## 14. HTTP/2 vs HTTP/3 Architecture

HTTP/2:

```text
             HTTP/2
                |
       +--------+--------+
       |                 |
   RST_STREAM          GOAWAY
       |                 |
       +--------+--------+
                |
                v
               TCP
```

HTTP/3:

```text
             HTTP/3
                |
          +-----+-----+
          |           |
      HTTP-level   HTTP-level
      GOAWAY       H3 errors
          |           |
          +-----+-----+
                |
                v
              QUIC
                |
       +--------+---------+
       |        |         |
RESET_STREAM  STOP_    CONNECTION_
              SENDING     CLOSE
```

The architectural difference is important: QUIC itself understands streams, while TCP provides only one ordered byte stream.

## 15. HTTP/2 RST_STREAM vs QUIC RESET_STREAM

Conceptually they solve similar stream-lifecycle problems, but they live at different layers.

```text
HTTP/2:

HTTP/2 RST_STREAM
       |
       v
TCP

HTTP/3:

HTTP/3 semantics
       |
       v
QUIC RESET_STREAM
       |
       v
UDP
```

HTTP/2's `RST_STREAM` is an HTTP/2 frame. QUIC's `RESET_STREAM` is a transport-level operation.

## 16. Layering of Error and Shutdown Mechanisms

```text
                         HTTP/3
                            |
             +--------------+--------------+
             |                             |
          GOAWAY                       H3_* errors
             |                             |
             +--------------+--------------+
                            |
                            v
                          QUIC
                            |
          +-----------------+-----------------+
          |                 |                 |
   RESET_STREAM       STOP_SENDING      CONNECTION_CLOSE
```

This is the key layering model.

HTTP/3 defines HTTP semantics and HTTP/3 protocol errors. QUIC provides transport-level stream and connection control.

## 17. Important Mental Model

When a user cancels a request:

```text
User cancels request
       |
       v
HTTP/3 request cancellation
       |
       v
QUIC stream termination
       |
       v
Other streams unaffected
```

When a server gracefully shuts down:

```text
Server shutdown requested
       |
       v
HTTP/3 GOAWAY
       |
       v
Stop accepting new HTTP requests
       |
       v
Existing work completes
       |
       v
QUIC CONNECTION_CLOSE
```

The protocol avoids unnecessarily destroying unrelated requests.

## 18. Key Takeaways

1. HTTP/3 and QUIC have different error/shutdown mechanisms because they operate at different layers.
2. `RESET_STREAM`, `STOP_SENDING`, and `CONNECTION_CLOSE` are QUIC mechanisms, not part of the HTTP/3 `SETTINGS` frame.
3. `SETTINGS` communicates HTTP/3 configuration; it does not contain stream reset or connection-close commands.
4. HTTP status codes such as `200`, `404`, and `500` describe HTTP request/response semantics.
5. `H3_*` error codes describe HTTP/3 protocol or stream-operation failures.
6. `GOAWAY` provides graceful HTTP/3 shutdown and is different from QUIC `CONNECTION_CLOSE`.
7. A stream-specific error can normally be isolated to one request.
8. Errors affecting critical HTTP/3 protocol state can require the whole HTTP/3 connection to terminate.
9. HTTP/2 uses `RST_STREAM` and `GOAWAY` at the HTTP/2 layer, whereas HTTP/3 relies on QUIC for stream transport operations such as `RESET_STREAM` and `STOP_SENDING`.
10. The key architectural distinction is that QUIC understands streams as transport primitives while TCP does not.
