# Lesson 29 - HTTP/2 to HTTP/3: The Evolution Continues

## What I Learned

The evolution from HTTP/1.1 to HTTP/3 is driven by progressively identifying and removing limitations at different layers.

## HTTP/1.1

HTTP/1.1 uses a textual representation and has limited request parallelism.

```text
HTTP/1.1
   |
   v
TCP
```

Multiple connections can provide parallelism, but add connection and TLS overhead. Pipelining is constrained by response ordering.

## HTTP/2

HTTP/2 introduces binary framing and multiplexed streams:

```text
HTTP/2
  |
  +-- Stream 1
  +-- Stream 3
  +-- Stream 5
          |
          v
         TCP
```

This allows many logical HTTP exchanges to share one TCP connection.

## Remaining Problem

TCP still provides one ordered byte stream.

```text
HTTP/2 Streams
       |
       v
      TCP
       |
       v
Ordered byte stream
       |
       v
TCP head-of-line blocking
```

## QUIC

QUIC moves stream multiplexing into the transport layer and runs over UDP.

```text
HTTP/3
   |
   v
 QUIC
   |
   +-- Stream 1
   +-- Stream 2
   +-- Stream 3
   |
   v
  UDP
   |
   v
  IP
```

QUIC provides transport functionality that HTTP/3 can use without relying on TCP's single ordered byte stream.

## Evolution

```text
HTTP/1.1
    |
    | Limited parallelism
    v
Multiple TCP Connections / Pipelining
    |
    | Overhead / ordering limitations
    v
HTTP/2
    |
    | Multiplexed streams
    v
One TCP Connection
    |
    | TCP-level HOL blocking
    v
QUIC
    |
    | Transport-level streams
    v
HTTP/3
```

## Key Insight

HTTP/2 and HTTP/3 are not simply newer versions with more features. Their evolution reflects a change in where multiplexing and transport responsibilities are handled.

The next stage is to understand QUIC itself: how it uses UDP while providing reliability, streams, congestion control and connection management.