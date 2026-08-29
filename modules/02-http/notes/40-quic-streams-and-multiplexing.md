# Lesson 40 - QUIC Streams & Multiplexing

## Objectives

- Understand QUIC streams.
- Understand stream IDs and stream offsets.
- Understand bidirectional and unidirectional streams.
- Understand how QUIC multiplexes streams.
- Understand stream-level ordering versus packet-level tracking.
- Understand how QUIC avoids TCP's connection-level head-of-line blocking.
- Understand the limits of stream independence.

## Concept Summary

A QUIC connection can contain many independent streams. Each stream is an ordered byte sequence identified by a Stream ID and reconstructed using stream offsets.

Unlike TCP, QUIC does not expose one connection-wide ordered byte stream to the application.

## Core Ideas

### Multiple Streams Per Connection

```text
                 QUIC Connection
                       |
        +--------------+--------------+
        |              |              |
        v              v              v
    Stream 4        Stream 8       Stream 12
        |              |              |
        v              v              v
     Data A          Data B         Data C
```

### TCP vs QUIC Ordering

TCP:

```text
TCP Connection
      |
      v
One ordered byte stream
      |
      v
Missing byte
      |
      v
Later bytes cannot be delivered
```

QUIC:

```text
QUIC Connection
      |
      +--- Stream 4
      |
      +--- Stream 8
      |
      +--- Stream 12
```

Ordering is maintained independently within each stream.

### Stream Frames

Stream data is carried inside STREAM frames.

```text
QUIC Packet
    |
    +----------------------+
    | STREAM Frame         |
    |                      |
    | Stream ID            |
    | Offset               |
    | Length               |
    | Data                 |
    +----------------------+
```

The Stream ID identifies the stream and the offset identifies where the bytes belong within that stream.

### Packet Number vs Stream Offset

These are different namespaces solving different problems.

```text
                 QUIC
                   |
          +--------+--------+
          |                 |
          v                 v
    Packet-level         Stream-level
      tracking             ordering
          |                 |
          v                 v
   Packet Number        Stream Offset
```

Packets can arrive out of order while stream data is reassembled according to stream offsets.

### Bidirectional Streams

Both endpoints can send data.

```text
Client                         Server
   |                              |
   |------ Stream data ---------->|
   |                              |
   |<----- Stream data -----------|
   |                              |
```

### Unidirectional Streams

Data flows in one direction only.

```text
Client                         Server
   |                              |
   |====== Stream data ==========>|
   |                              |
```

HTTP/3 uses unidirectional streams for several control-oriented purposes.

## Multiplexing

Multiple streams share one QUIC connection and can be distributed across packets.

```text
Stream 4  ----+
Stream 8  ----+----> QUIC packets ----> UDP
Stream 12 ----+
```

A packet can carry data from different streams, and different packets can carry different parts of the same stream.

## Loss and Stream Independence

Suppose a packet carrying Stream 4 data is lost.

```text
Packet 100 → Stream 4 ─── X
Packet 101 → Stream 8 ─────→
Packet 102 → Stream 12 ────→
```

QUIC can continue processing Stream 8 and Stream 12 data while the missing Stream 4 data is recovered, assuming no connection-level constraint prevents progress.

The retransmitted Stream 4 data can appear in a new packet.

```text
Lost Packet 100
      |
      v
Stream 4 data remains needed
      |
      v
New Packet 110
      |
      v
Stream 4 data retransmitted
```

## The Precise HOL Model

QUIC does not eliminate every kind of waiting.

If Stream 4 has a missing byte:

```text
Stream 4
A B C [D] E F
       |
       v
    waits
```

But Stream 8 can continue:

```text
Stream 8
P Q R S
       |
       v
   continues
```

Connection-level congestion, flow control or connection failure can still affect multiple streams.

## Why This Matters for HTTP/3

HTTP/2 multiplexes streams but carries them over TCP.

```text
HTTP/2
  |
  v
Multiple HTTP streams
  |
  v
TCP ordered byte stream
  |
  v
Connection-level HOL blocking
```

HTTP/3 maps HTTP operations onto QUIC streams.

```text
HTTP/3
   |
   v
QUIC streams
   |
   v
QUIC packets
   |
   v
UDP
```

This removes TCP's connection-wide ordering constraint from the transport path.

## Practical Example

A browser uses one QUIC connection for:

```text
Stream 4  -> /index.html
Stream 8  -> /style.css
Stream 12 -> /app.js
```

If a packet containing part of `/index.html` is lost, the missing Stream 4 data may need retransmission, but successful Stream 8 and Stream 12 data does not inherently need to wait for Stream 4.

## Production Perspective

QUIC streams allow browsers and other HTTP/3 clients to multiplex many logical operations over one connection without inheriting TCP's connection-wide ordered-byte-stream blocking behavior.

However, streams still share connection-level resources such as congestion-control capacity and connection-level flow-control limits.

## Common Mistakes

- QUIC streams are not independent network connections.
- A stream can still experience its own ordering stall.
- QUIC does not provide unlimited bandwidth to every stream.
- Packet numbers and stream offsets are different concepts.
- QUIC's HOL improvement is specifically about TCP's connection-level transport ordering.

## Key Takeaways

1. One QUIC connection can contain many streams.
2. Each stream is an independently ordered byte sequence.
3. STREAM frames carry Stream ID, offset and data information.
4. Packet numbers track packets; stream offsets order stream bytes.
5. A lost packet affecting Stream 4 does not inherently block Stream 8.
6. Stream-level waiting still exists.
7. Congestion control and connection-level flow control remain shared.
8. This architecture is a major reason HTTP/3 avoids TCP-level HOL blocking.

## Reflection Questions

1. Why are stream offsets needed if QUIC already has packet numbers?
2. What is the difference between bidirectional and unidirectional streams?
3. Why can Stream 8 continue when Stream 4 has missing data?
4. Why doesn't QUIC need to retransmit an entire packet?
5. What kinds of problems can still affect every stream in a connection?
6. Why does HTTP/3 use QUIC streams instead of putting everything into one TCP stream?

## Related Lessons

- Lesson 39 - QUIC Reliability, Loss Detection & ACKs
- Lesson 41 - QUIC Flow Control & Congestion Control
- Lesson 42 - QUIC Connection Migration & Final Architecture
