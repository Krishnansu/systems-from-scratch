# Lesson 28 - TCP Head-of-Line Blocking and the Need for QUIC

## What I Learned

HTTP/2 provides multiple independent logical streams, but all of those streams share one TCP connection.

TCP guarantees ordered delivery. It does not understand HTTP/2 stream boundaries.

Therefore packet loss in the TCP connection can delay data from multiple HTTP/2 streams.

## Example

Suppose the HTTP/2 connection contains:

```text
Stream A → A1 A2 A3 A4
Stream B → B1 B2 B3 B4
Stream C → C1 C2 C3 C4
```

These bytes are transported through one TCP connection.

If a TCP segment containing some bytes is lost, TCP must recover the missing bytes before continuing its ordered byte-stream abstraction.

```text
A1 A2 [missing] A4 B1 B2 B3 C1 C2 ...
          |
          v
     Retransmission
```

The HTTP/2 layer above TCP can therefore be affected even when the missing data belongs primarily to another stream.

## The Fundamental Limitation

```text
HTTP/2
  |
  +-- Stream A
  +-- Stream B
  +-- Stream C
          |
          v
         TCP
          |
          v
   One ordered byte stream
```

HTTP/2 has independent streams, but TCP has one ordered stream.

## Why QUIC

This leads to the next architectural question:

> What if the transport layer itself provided independent streams?

QUIC was designed around this idea.

Conceptually:

```text
HTTP/2
   |
   v
TCP
   |
   v
One ordered byte stream

versus

HTTP/3
   |
   v
QUIC
   |
   +-- Stream 1
   +-- Stream 2
   +-- Stream 3
```

QUIC runs over UDP but provides transport features such as reliability, congestion control, encryption integration and multiplexed streams.

## Key Insight

UDP itself does not provide these guarantees. QUIC builds them above UDP.

The important evolution is therefore:

```text
HTTP/1.1 → HTTP/2 → QUIC → HTTP/3
```

The next lesson will examine QUIC in detail.