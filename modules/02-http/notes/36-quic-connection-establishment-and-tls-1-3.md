# Lesson 36 - QUIC Connection Establishment & TLS 1.3

## Objectives

- Understand how a fresh QUIC connection is established.
- Understand how QUIC integrates TLS 1.3 into connection establishment.
- Understand QUIC Initial, Handshake and 1-RTT encryption levels.
- Understand how TLS handshake messages are carried using QUIC CRYPTO frames.
- Understand why QUIC does not need a TCP handshake.
- Understand the high-level difference between a fresh handshake and 0-RTT resumption.
- Understand why 0-RTT introduces replay considerations.

## Prerequisites

- Lesson 27 - HTTP/2 Fundamentals
- Lesson 29 - HTTP/2 Multiplexing
- Lesson 30 - TCP Head-of-Line Blocking and the Need for QUIC
- Lesson 31 - HTTP/2 to HTTP/3
- Lesson 32 - HTTP/2 Flow Control & Stream Management
- Lesson 33 - HTTP/2 Stream Prioritization & Scheduling
- Lesson 34 - QUIC Fundamentals
- Lesson 35 - QUIC Packets, Frames & Connection IDs

## Theory

QUIC runs over UDP and provides the transport features that TCP normally provides, including reliability, congestion control, flow control and multiplexed streams. TLS 1.3 provides authentication and cryptographic key establishment.

Unlike HTTPS over TCP, QUIC does not require a separate TCP handshake before starting TLS.

```text
TCP + TLS:

TCP handshake
      |
      v
TLS handshake
      |
      v
HTTP
```

QUIC combines transport establishment and TLS handshake progress:

```text
QUIC Initial
     |
     +-- TLS ClientHello
     |
     v
QUIC Handshake
     |
     +-- TLS handshake messages
     |
     v
1-RTT application traffic
     |
     +-- HTTP/3
```

TLS is not replaced by QUIC. TLS 1.3 is integrated into QUIC through CRYPTO frames and provides the cryptographic secrets used for packet protection.

## Real World Example

When a browser opens an HTTP/3 connection to a server for the first time, the client can immediately send a QUIC Initial packet over UDP. That packet can contain a CRYPTO frame carrying the TLS ClientHello.

```text
Client                                  Server
  |                                       |
  | QUIC Initial                          |
  | CRYPTO: TLS ClientHello               |
  |-------------------------------------->|
  |                                       |
  | QUIC Initial / Handshake              |
  | CRYPTO: TLS handshake data            |
  |<--------------------------------------|
  |                                       |
  | QUIC Handshake                        |
  | CRYPTO: TLS handshake data            |
  |-------------------------------------->|
  |                                       |
  | QUIC 1-RTT                            |
  | STREAM: HTTP/3 request                |
  |-------------------------------------->|
```

The important idea is that TLS handshake bytes travel inside QUIC packets instead of waiting for a separately established TCP connection.

## Deep Dive

### 1. QUIC and TLS Responsibilities

The responsibilities remain distinct:

| Component | Responsibility |
|---|---|
| QUIC | Packets, streams, ACKs, loss detection, flow control, congestion control and connection management |
| TLS 1.3 | Authentication, key exchange and cryptographic secrets |
| HTTP/3 | Application-level HTTP semantics |
| UDP | Datagram delivery |

A useful mental model is:

```text
HTTP/3
   |
   v
 QUIC
 +--------------------------+
 | Transport responsibilities|
 | TLS 1.3 integration       |
 +--------------------------+
   |
   v
 UDP
```

### 2. CRYPTO Frames

TLS handshake messages are carried in QUIC `CRYPTO` frames.

```text
QUIC Initial packet
   |
   +-- CRYPTO frame
          |
          +-- TLS ClientHello
```

CRYPTO frames are not QUIC streams. TLS handshake data has its own offsets and is associated with the relevant encryption level.

### 3. Initial Packets

A fresh QUIC connection begins with Initial packets.

The client can send:

```text
Initial packet
   |
   +-- QUIC header
   +-- CRYPTO frame
         |
         +-- TLS ClientHello
```

Initial packets use QUIC Initial packet-protection keys rather than the eventual 1-RTT application keys.

### 4. TLS Handshake Progression

At a high level, the connection progresses through cryptographic stages:

```text
Initial
  |
  v
Handshake
  |
  v
1-RTT
```

The TLS handshake produces secrets that QUIC uses to protect packets at the appropriate encryption level.

### 5. Packet Number Spaces

QUIC separates packet numbers into different packet number spaces.

```text
Initial packet number space
Handshake packet number space
Application Data packet number space
```

The same packet number can therefore appear in different spaces without representing the same packet.

This separation matches the different cryptographic stages and their independent acknowledgment/loss-recovery state.

### 6. Initial Keys vs 1-RTT Keys

Initial packet protection keys are available before the TLS handshake has produced normal application traffic secrets. They allow the Initial exchange to be protected.

Later, TLS 1.3 derives application traffic secrets. QUIC uses these to protect normal 1-RTT application packets.

```text
Connection start
      |
      v
Initial keys
      |
      v
Handshake keys
      |
      v
1-RTT application keys
```

The exact QUIC key derivation and packet-protection process is covered in the next lessons.

### 7. Why QUIC Does Not Need a TCP Handshake

UDP allows the client to send a datagram immediately.

```text
Client
  |
  | UDP datagram containing QUIC Initial
  v
Server
```

There is no separate:

```text
SYN
SYN-ACK
ACK
```

exchange before the QUIC/TLS handshake begins.

This removes the extra TCP connection-establishment phase found in traditional HTTPS.

### 8. Fresh QUIC Connection vs TCP + TLS

Traditional HTTPS has conceptually separate establishment stages:

```text
Client                         Server
  |                              |
  | TCP SYN -------------------->|
  |<------------- SYN-ACK -------|
  | TCP ACK -------------------->|
  |                              |
  | TLS ClientHello ------------>|
  |<----------- TLS response ----|
  |<---------- TLS handshake ----|
  | TLS handshake -------------->|
  |                              |
  | HTTP ----------------------->|
```

QUIC starts with its own Initial packet and carries TLS handshake data immediately:

```text
Client                         Server
  |                              |
  | Initial + ClientHello ------>|
  |<----- Initial/Handshake -----|
  |------ Handshake ------------>|
  |                              |
  |------ 1-RTT HTTP/3 --------->|
```

The exact number of packets and timing depends on packetization, network conditions, server behavior and handshake details, but the architectural difference is the removal of a separate TCP handshake.

### 9. QUIC Reliability During the Handshake

UDP itself provides no retransmission or ordering guarantees. QUIC supplies these mechanisms.

If a packet carrying TLS handshake data is lost:

```text
Initial packet
     |
     X  lost
     |
     v
QUIC loss detection
     |
     v
TLS CRYPTO data sent again
in a new QUIC packet
```

QUIC retransmits the relevant data rather than treating the original packet as an immutable object that must be replayed byte-for-byte.

### 10. 1-RTT Application Traffic

Once the TLS handshake has progressed far enough for application traffic secrets to be available, endpoints can use 1-RTT packet protection.

HTTP/3 data is then carried in QUIC STREAM frames:

```text
HTTP/3 request
      |
      v
QUIC STREAM frame
      |
      v
QUIC 1-RTT packet
      |
      v
UDP datagram
```

### 11. 0-RTT

If a client has previously established a connection with the server, TLS 1.3 session resumption can provide information that allows the client to send 0-RTT application data during a new connection attempt.

Conceptually:

```text
Client
  |
  | Initial + TLS ClientHello
  | + 0-RTT application data
  |--------------------------------->
  |
Server
```

This can reduce application startup latency because the client does not have to wait for the complete handshake before sending eligible application data.

### 12. Why 0-RTT Has Replay Concerns

0-RTT data can potentially be replayed by an attacker. Therefore applications must be careful about operations that change server state.

```text
Read-only request
   -> easier to reason about

State-changing operation
   -> replay risk must be considered
```

0-RTT is therefore a latency optimization with security/application-level trade-offs, not a general-purpose replacement for normal 1-RTT traffic.

### 13. TLS Does Not Provide QUIC Reliability

TLS and QUIC have different jobs.

```text
TLS 1.3
  |
  +-- Authentication
  +-- Key exchange
  +-- Traffic secrets

QUIC
  |
  +-- Packet delivery
  +-- ACKs
  +-- Loss detection
  +-- Retransmission of needed data
  +-- Streams
  +-- Flow control
  +-- Congestion control
```

This separation is essential to understanding the architecture.

### 14. Complete Mental Model

```text
                    HTTP/3
                       |
                       v
                     QUIC
                       |
        +--------------+--------------+
        |                             |
   Transport                    TLS 1.3
        |                             |
   Packets                         Handshake
   Streams                         Key exchange
   ACKs                            Secrets
   Reliability                     Authentication
        |                             |
        +--------------+--------------+
                       |
                       v
                      UDP
```

The TLS handshake supplies cryptographic state while QUIC supplies transport state.

## Hands-on Exercise

Given this trace:

```text
Client                                  Server
  |                                       |
  | Initial                               |
  | CRYPTO: ClientHello                   |
  |-------------------------------------->|
  |                                       |
  | Initial                               |
  | CRYPTO: TLS response                  |
  |<--------------------------------------|
  |                                       |
  | Handshake                             |
  | CRYPTO: TLS handshake data            |
  |<--------------------------------------|
  |                                       |
  | Handshake                             |
  | CRYPTO: TLS handshake data            |
  |-------------------------------------->|
  |                                       |
  | 1-RTT                                 |
  | STREAM: HTTP/3 request                |
  |-------------------------------------->|
```

Answer:

1. Which protocol establishes cryptographic secrets?
2. Which protocol provides reliable transport?
3. Where is the TLS ClientHello carried?
4. Why is there no TCP SYN/SYN-ACK exchange?
5. Why are Initial and Handshake separate packet number spaces?
6. What is the purpose of 1-RTT keys?
7. What happens if the Initial packet containing ClientHello is lost?
8. What does 0-RTT allow a returning client to do?
9. Why must 0-RTT data be treated carefully?
10. Which protocol understands HTTP/3 STREAM frames?

## Common Misconceptions

### "QUIC replaces TLS."

No. QUIC integrates TLS 1.3 for authentication and key establishment.

### "TLS makes QUIC reliable."

No. QUIC provides reliability. TLS provides cryptographic security.

### "QUIC performs a TCP handshake first."

No. QUIC runs directly over UDP and starts with QUIC packets.

### "TLS handshake messages are carried in QUIC STREAM frames."

No. QUIC uses dedicated `CRYPTO` frames for TLS handshake data.

### "Initial packets use the final application keys."

No. Initial packets use Initial packet-protection keys. Later stages use Handshake and 1-RTT keys.

### "1-RTT means the entire QUIC handshake always takes one round trip."

No. 1-RTT refers to the normal application traffic encryption level and its associated keys.

### "0-RTT is free latency reduction with no security implications."

No. 0-RTT introduces replay considerations and should only be used safely by applications.

## Summary

QUIC combines transport establishment with TLS 1.3 rather than performing a separate TCP handshake followed by TLS. A client begins with QUIC Initial packets that can carry TLS ClientHello data in CRYPTO frames. As the TLS handshake progresses, QUIC moves through Initial, Handshake and 1-RTT encryption levels.

QUIC remains responsible for transport reliability, acknowledgments, loss detection, flow control, congestion control and streams. TLS provides authentication and cryptographic key establishment. Once application traffic secrets are available, HTTP/3 data can be carried in 1-RTT STREAM frames.

TLS 1.3 session resumption can also enable 0-RTT application data for returning clients, but 0-RTT has replay-security considerations.

## Key Takeaways

1. QUIC runs directly over UDP and does not use TCP.
2. QUIC integrates TLS 1.3 into connection establishment.
3. TLS handshake messages are carried in QUIC CRYPTO frames.
4. QUIC provides transport reliability; TLS provides cryptographic security.
5. QUIC progresses through Initial, Handshake and 1-RTT encryption levels.
6. Initial packets use Initial packet-protection keys, not final application keys.
7. QUIC has separate packet number spaces for different connection stages.
8. Once application traffic secrets are available, HTTP/3 can use 1-RTT protected STREAM frames.
9. A lost handshake packet is handled by QUIC's loss-recovery machinery.
10. TLS 1.3 session resumption can enable 0-RTT application data.
11. 0-RTT introduces replay considerations.
12. QUIC removes the separate TCP handshake required by traditional HTTPS.

## Reflection Questions

1. Why does QUIC integrate TLS 1.3 instead of simply running TLS over a QUIC byte stream?
2. What responsibilities belong to QUIC and which belong to TLS?
3. Why are TLS handshake messages carried in CRYPTO frames?
4. Why can a QUIC client send a TLS ClientHello immediately without a TCP handshake?
5. What distinguishes Initial, Handshake and 1-RTT encryption levels?
6. Why are packet number spaces separated?
7. How does QUIC recover when a packet carrying handshake data is lost?
8. Why is 0-RTT possible for a returning client but not normally for a completely new client?
9. Why does 0-RTT create replay concerns?
10. Why can QUIC establish secure application traffic with less connection-establishment overhead than TCP + TLS?

## What's Next

### Lesson 37 - QUIC Packet Protection & Encryption

Next we will examine how QUIC protects packets after TLS provides the necessary secrets.

We will study:

```text
QUIC packet
   |
   +-- Payload encryption
   |
   +-- Header protection
   |
   +-- Packet authentication
```

The main question will be:

> Once TLS has produced the secrets, how exactly does QUIC turn them into encrypted and authenticated packets on the wire?
