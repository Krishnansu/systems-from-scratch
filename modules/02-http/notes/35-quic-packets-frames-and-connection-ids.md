# Lesson 35 - QUIC Packets, Frames & Connection IDs

## Objectives

- Understand the relationship between UDP datagrams, QUIC packets and QUIC frames.
- Understand important QUIC frame types.
- Distinguish packet numbers from stream offsets.
- Understand QUIC streams at the transport layer.
- Understand Connection IDs and why QUIC uses them.
- Understand the basic idea of connection migration.
- Understand the difference between long and short QUIC headers at a high level.
- Understand QUIC packet number spaces at a high level.

## Prerequisites

- Lesson 27 - HTTP/2 Fundamentals
- Lesson 28 - HTTP/2 Frames and Streams
- Lesson 29 - HTTP/2 Multiplexing
- Lesson 30 - TCP Head-of-Line Blocking and the Need for QUIC
- Lesson 31 - HTTP/2 to HTTP/3
- Lesson 32 - HTTP/2 Flow Control & Stream Management
- Lesson 33 - HTTP/2 Stream Prioritization & Scheduling
- Lesson 34 - QUIC Fundamentals

## Theory

QUIC is a transport protocol running over UDP. UDP provides datagram delivery, while QUIC provides reliability, streams, flow control, congestion control, connection management and TLS integration.

The basic protocol hierarchy is:

```text
HTTP/3
   |
   v
 QUIC
   |
   v
 UDP datagram
   |
   v
 IP packet
```

A QUIC packet contains a header followed by one or more QUIC frames.

```text
+------------------------------------------+
| QUIC Packet Header                       |
+------------------------------------------+
| Frame 1                                  |
+------------------------------------------+
| Frame 2                                  |
+------------------------------------------+
| Frame 3                                  |
+------------------------------------------+
| ...                                      |
+------------------------------------------+
```

Packets are transport containers. Frames carry specific protocol information.

## Real World Example

Consider an HTTP/3 connection carrying HTML and CSS:

```text
QUIC Connection
 |
 +-- Stream 4 -> HTML
 |
 +-- Stream 8 -> CSS
```

A single QUIC packet might contain:

```text
Packet #200
 |
 +-- STREAM frame -> Stream 4, offset 100
 |
 +-- STREAM frame -> Stream 8, offset 50
 |
 +-- ACK frame
```

Therefore:

```text
1 QUIC packet
     |
     +-- multiple frames
              |
              +-- potentially multiple streams
```

This is different from treating a packet as equivalent to an HTTP request, stream or message.

## Deep Dive

### 1. QUIC Packets and Frames

A QUIC packet is the transport-level unit carried inside a UDP datagram. Frames are the units that describe QUIC operations inside the packet.

Important frame types include:

| Frame | Purpose |
|---|---|
| `STREAM` | Carries data belonging to a QUIC stream |
| `ACK` | Acknowledges received QUIC packets |
| `CRYPTO` | Carries TLS handshake data |
| `MAX_DATA` | Increases the connection-level flow-control limit |
| `MAX_STREAM_DATA` | Increases a stream-level flow-control limit |
| `MAX_STREAMS` | Controls the number of streams that may be created |
| `RESET_STREAM` | Abruptly terminates a stream |
| `STOP_SENDING` | Requests that the peer stop sending on a stream |
| `CONNECTION_CLOSE` | Closes the QUIC connection |

A useful comparison with HTTP/2 is:

```text
HTTP/2 frames -> HTTP-layer protocol operations
QUIC frames   -> transport-layer protocol operations
```

### 2. STREAM Frames

A `STREAM` frame carries bytes belonging to one QUIC stream.

Conceptually, it contains:

```text
+-----------------------------+
| Stream ID                   |
+-----------------------------+
| Stream Offset               |
+-----------------------------+
| Length                      |
+-----------------------------+
| Stream Data                 |
+-----------------------------+
```

The exact wire format uses variable-length fields and flags, but these fields provide the correct mental model.

### 3. Why Streams Need Offsets

TCP presents one connection-wide ordered byte stream:

```text
byte 0 -> byte 1 -> byte 2 -> byte 3 -> ...
```

QUIC has independent streams, so each stream has its own byte-offset space:

```text
Stream 4:
  offset 0 -> A
  offset 1 -> B
  offset 2 -> C

Stream 8:
  offset 0 -> X
  offset 1 -> Y
  offset 2 -> Z
```

There is no single application-visible ordering that forces Stream 4 and Stream 8 into one global byte sequence.

This is one of the foundations for avoiding TCP's cross-stream head-of-line blocking.

### 4. Packet Numbers vs Stream Offsets

These two concepts must not be confused.

```text
Packet number
  -> identifies a QUIC packet for transport purposes
  -> used for acknowledgments and loss detection

Stream offset
  -> identifies a byte position within a stream
  -> used for stream reassembly and ordering
```

For example:

```text
Packet #100
 |
 +-- STREAM 4, offset 500
```

The `100` and `500` refer to completely different things.

### 5. ACK Frames

QUIC acknowledges packets rather than acknowledging an application stream as one global byte sequence.

Suppose the receiver gets:

```text
Packet 100 -> received
Packet 101 -> received
Packet 102 -> lost
Packet 103 -> received
Packet 104 -> received
```

An ACK can describe the received packet ranges. The sender can use this information for loss detection.

The important distinction is:

```text
ACK -> packet-level transport information
STREAM offset -> stream-level ordering information
```

### 6. Loss and Retransmission

Suppose packet `#102` contains data for two streams and is lost:

```text
Packet #102
 |
 +-- Stream 4 data
 +-- Stream 8 data
```

QUIC does not simply resend the exact same packet as packet `#102`.

Instead, after loss detection, the relevant stream data can be placed into new packets:

```text
Packet #102 -> lost

        |
        v
Loss detected
        |
        v
New packet
 +-- retransmitted Stream 4 data
 +-- retransmitted Stream 8 data if needed
```

This distinction becomes important when studying QUIC loss recovery.

### 7. Connection IDs

A QUIC connection has Connection IDs that allow packets to be associated with the logical connection independently of the current network path.

Conceptually:

```text
QUIC Connection
Connection ID = ABC123
 |
 +-- Stream 4
 +-- Stream 8
 +-- Stream 12
```

A Connection ID is not a Stream ID.

```text
Connection ID -> identifies the QUIC connection
Stream ID     -> identifies a stream within that connection
```

### 8. Why Connection IDs Matter

Traditional TCP connection identity is closely tied to the endpoint tuple:

```text
source IP
source port
destination IP
destination port
```

If a mobile device changes from Wi-Fi to cellular, its source IP can change.

QUIC's Connection ID allows the logical connection to remain identifiable even when the network path changes, subject to QUIC's path validation and security rules.

### 9. Connection Migration

Conceptually:

```text
Before:

Client
  |
 Wi-Fi
  |
Internet
  |
Server

Connection ID = ABC123
```

After a network change:

```text
Client
  |
Cellular
  |
Internet
  |
Server

Connection ID = ABC123
```

The network path changed, but the logical QUIC connection can continue using the same connection identity.

Connection migration is not simply accepting packets from arbitrary addresses. QUIC performs path validation and has additional mechanisms to prevent attacks.

### 10. Connection ID vs Stream ID

Keep the hierarchy clear:

```text
QUIC Connection
 |
 +-- Connection ID -> identifies the connection
 |
 +-- Stream 4
 +-- Stream 8
 +-- Stream 12
       |
       +-- Stream IDs identify streams
```

### 11. Long and Short Headers

QUIC has two major packet-header forms:

```text
Long Header
Short Header
```

At a high level:

```text
Long Header
 |
 +-- Initial
 +-- 0-RTT
 +-- Handshake
 +-- Retry

Short Header
 |
 +-- 1-RTT application traffic
```

The exact packet formats and encryption rules will be studied later. For now, the important point is that QUIC uses different header forms for different stages and types of traffic.

### 12. Packet Number Spaces

QUIC separates packet numbers into different packet number spaces associated with different connection stages.

At a high level:

```text
Initial packet number space
Handshake packet number space
Application Data packet number space
```

These spaces have separate acknowledgment and loss-recovery treatment.

This prevents packets from different cryptographic stages from being treated as one undifferentiated sequence.

### 13. QUIC Packet Structure

The complete mental model is:

```text
QUIC Packet
 |
 +-- Header
 |    |
 |    +-- Header form
 |    +-- Connection ID information
 |    +-- Packet number information
 |
 +-- Frames
      |
      +-- STREAM
      +-- ACK
      +-- CRYPTO
      +-- Flow-control frames
      +-- Connection-control frames
```

### 14. HTTP/3 to QUIC to UDP

The receiving path can be visualized as:

```text
IP packet
   |
   v
UDP datagram
   |
   v
QUIC packet
   |
   +-- header
   |
   +-- frames
          |
          +-- STREAM data
          +-- ACK
          +-- control information
   |
   v
QUIC stream reassembly
   |
   v
HTTP/3
```

This hierarchy is extremely useful when debugging network behavior.

## Hands-on Exercise

Consider this packet:

```text
Connection ID = ABC123
Packet Number = 200

Frames:
  STREAM
    Stream ID = 4
    Offset = 100
    Data = "hello"

  STREAM
    Stream ID = 8
    Offset = 50
    Data = "body"

  ACK
    acknowledges packets 198-199
```

Answer:

1. How many streams are represented in the packet?
2. How many frames does the packet contain?
3. What does packet number `200` identify?
4. What does Stream 4 offset `100` identify?
5. If packet `200` is lost, is packet `200` retransmitted byte-for-byte?
6. Can Stream 8 continue independently if Stream 4 has missing data?
7. What identifies the QUIC connection?
8. What identifies the individual streams?
9. Why can one packet contain data from multiple streams?
10. Which information is transport-level and which is stream-level?

## Common Misconceptions

### "A QUIC packet is a stream."

No. A packet can contain multiple frames, and those frames can belong to multiple streams.

### "A packet number identifies stream bytes."

No. Packet numbers are used for transport-level packet tracking. Stream offsets identify positions within individual streams.

### "QUIC retransmits lost packets exactly as they were."

More accurately, QUIC detects lost packets and retransmits the relevant data in new packets.

### "Connection ID and Stream ID are the same thing."

No. Connection IDs identify connections; Stream IDs identify streams inside connections.

### "UDP makes QUIC unreliable."

UDP itself is unreliable, but QUIC builds reliable transport semantics above UDP.

### "QUIC eliminates every kind of head-of-line blocking."

No. A stream can still wait for its own missing data. The important improvement is eliminating TCP's connection-level ordering dependency across independent streams.

## Summary

QUIC packets are transport-level containers carried in UDP datagrams. Each packet contains a header and one or more frames. Frames perform specific transport operations such as carrying stream data, acknowledging packets, carrying TLS handshake data and controlling flow or connection state.

QUIC streams have independent stream offsets, while QUIC packets have packet numbers used for transport-level loss detection and acknowledgments. These are separate namespaces serving different purposes.

QUIC Connection IDs identify logical connections independently of the current network path, enabling mechanisms such as connection migration. Stream IDs identify individual streams within those connections.

## Key Takeaways

1. A UDP datagram carries QUIC packet data.
2. A QUIC packet contains a header and one or more frames.
3. A frame carries a specific QUIC protocol operation.
4. `STREAM` frames carry data belonging to individual QUIC streams.
5. Packet numbers are for transport-level tracking.
6. Stream offsets provide ordering within individual streams.
7. ACK frames acknowledge received QUIC packets.
8. Lost packets are not simply replayed; relevant data is sent again in new packets.
9. Connection IDs identify QUIC connections, while Stream IDs identify streams.
10. Connection IDs enable QUIC to support connection migration.
11. QUIC has long and short packet-header forms.
12. QUIC separates packet number spaces for different connection stages.

## Reflection Questions

1. Why does QUIC need both packets and frames?
2. Why are packet numbers and stream offsets separate concepts?
3. Why can one QUIC packet contain data from multiple streams?
4. Why does QUIC retransmit stream data rather than simply replaying a lost packet?
5. How does a Connection ID differ from a TCP connection's endpoint tuple?
6. Why are Connection IDs useful when a device changes networks?
7. How does connection migration preserve the logical connection while the network path changes?
8. What is the relationship between a QUIC packet, a QUIC frame and a QUIC stream?
9. Why is the packet/frame distinction useful when debugging QUIC?
10. How does the QUIC packet architecture support HTTP/3's multiplexed streams?

## What's Next

### Lesson 36 - QUIC Connection Establishment & TLS 1.3

Next we will follow a QUIC connection from the first Initial packets through the TLS 1.3 handshake to encrypted 1-RTT application traffic.

We will study:

```text
Client
  |
  | Initial
  v
Server
  |
  | TLS 1.3 handshake
  v
Handshake keys
  |
  v
1-RTT encrypted traffic
```

The main question will be:

> How does QUIC establish a secure transport connection while performing TLS 1.3, and why can this be faster than TCP + TLS?
