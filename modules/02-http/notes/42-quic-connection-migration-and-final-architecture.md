# Lesson 42 - QUIC Connection Migration & Final Architecture

## Objectives

- Understand why TCP connections are tied to network endpoint tuples.
- Understand QUIC Connection IDs.
- Understand connection migration.
- Understand NAT rebinding.
- Understand path validation.
- Understand why QUIC can survive some network-path changes without restarting the logical connection.
- Consolidate the major QUIC architecture concepts before HTTP/3.

## Concept Summary

TCP traditionally identifies a connection using a source IP, source port, destination IP and destination port. A network change can therefore make the old connection tuple invalid.

QUIC introduces Connection IDs so that the logical connection can remain identifiable even when the network path changes.

```text
IP address
    |
    v
"Where is this endpoint?"

Connection ID
    |
    v
"Which QUIC connection is this?"
```

## Core Ideas

### TCP Connection Identity

```text
Source IP:Port
       +
Destination IP:Port
       |
       v
TCP connection
```

If the client changes from Wi-Fi to mobile data, the source IP may change.

### QUIC Connection ID

```text
QUIC Connection
       |
       v
Connection ID
       |
       v
Logical connection identity
```

The Connection ID is distinct from the current IP address and UDP port used by the network path.

### Network Change

```text
Before:

Wi-Fi
192.168.1.20
      |
      v
    Server

After:

Mobile
10.20.30.40
      |
      v
    Server
```

Conceptually, the same QUIC connection can move from the old path to the new path.

```text
                 Same QUIC Connection
                         |
                  Connection ID
                         |
              +----------+----------+
              |                     |
           Old path              New path
              |                     |
            Wi-Fi                 Mobile
```

### Connection Migration

Connection migration means continuing a QUIC connection over a different network path.

```text
                 QUIC Connection
                       |
                 Connection ID
                       |
          +------------+------------+
          |                         |
          v                         v
       Old path                  New path
          |                         |
       Wi-Fi                    Mobile
```

The logical connection can survive while the network path changes.

### NAT Rebinding

A NAT device can change the external UDP port mapping even without an explicit Wi-Fi-to-cellular switch.

```text
Before:
Client → NAT → 203.0.113.20:62000 → Server

After:
Client → NAT → 203.0.113.20:62001 → Server
```

The apparent network tuple changed, but QUIC can use its connection identity to associate packets with the existing logical connection.

### Path Validation

A new path must not simply be trusted because packets appear from a different address.

At a high level QUIC can validate a new path using `PATH_CHALLENGE` and `PATH_RESPONSE`.

```text
Client                         Server
   |                              |
   |------ PATH_CHALLENGE ------->|
   |                              |
   |<------ PATH_RESPONSE --------|
   |                              |
   |       path validated         |
```

Path validation helps prevent blindly accepting an attacker-controlled path.

## Security Perspective

An IP address is not a cryptographic identity. QUIC therefore separates connection identity from network location and validates new paths before relying on them.

```text
New path
   |
   v
Path validation
   |
   +---- invalid ---> reject / do not migrate
   |
   v
 valid
   |
   v
Continue connection
```

## QUIC and TLS

Changing the network path does not inherently require starting a new TLS handshake for the logical QUIC connection.

```text
                 QUIC Connection
                        |
             +----------+----------+
             |                     |
          Old path              New path
             |                     |
             +----------+----------+
                        |
                        v
                 Same crypto state
```

The exact migration process includes additional protocol and security details, but the important architectural idea is that logical connection identity is independent from the current path.

## Complete QUIC Architecture

```text
                         QUIC
                           |
        +------------------+------------------+
        |                  |                  |
        v                  v                  v
   Connection          Security           Reliability
        |                  |                  |
        v                  v                  v
 Connection IDs       TLS 1.3             ACKs
 Migration            AEAD                Loss detection
 Path validation      Header protection   RTT
        |
        v
     Streams
        |
        v
   Multiplexing
        |
        v
   Flow Control
        |
        +------------------+
                           |
                           v
                  Congestion Control
                           |
                           v
                          UDP
```

## Packet Journey

```text
Application data
       |
       v
     Stream
       |
       v
   QUIC frames
       |
       v
   QUIC packet
       |
       +--> Packet number
       |
       +--> Connection ID
       |
       +--> Header protection
       |
       +--> AEAD encryption
       |
       v
      UDP
       |
       v
      IP
       |
       v
    Network
```

At the receiver the process is conceptually reversed.

```text
Network
   |
   v
   IP
   |
   v
  UDP
   |
   v
 QUIC
   |
   +--> Connection ID
   |
   +--> Header protection removal
   |
   +--> Packet number recovery
   |
   +--> AEAD authentication/decryption
   |
   +--> Frames
   |
   +--> Streams
   |
   v
Application
```

## QUIC vs HTTP/2 Transport Stack

HTTP/2:

```text
HTTP/2
   |
   v
TCP
   |
   v
TLS
   |
   v
IP
```

HTTP/3:

```text
HTTP/3
   |
   v
QUIC
   |
   v
UDP
   |
   v
IP
```

HTTP/3 moves HTTP's multiplexed operations onto QUIC streams instead of relying on one TCP ordered byte stream.

## Why QUIC Is More Than "TCP Over UDP"

QUIC combines transport functionality with modern connection and security requirements.

```text
                     QUIC
                       |
     +-----------------+------------------+
     |                 |                  |
     v                 v                  v
 Multiplexing      Security           Mobility
     |                 |                  |
 Streams            TLS 1.3          Connection IDs
     |              AEAD             Migration
     v
Independent stream ordering
```

## Practical Example

A mobile browser has a QUIC connection to a server.

```text
Stream 4  → video data
Stream 8  → metadata
Stream 12 → API request
```

The phone switches from Wi-Fi to mobile data. The network path changes, but the QUIC connection can potentially continue using the same logical connection identity after the new path is validated.

The streams, flow control, congestion control and reliability mechanisms continue to operate as part of the connection.

## Production Perspective

Connection migration is particularly useful for mobile clients and other devices whose network attachment can change. It can reduce disruption caused by changes in IP address or NAT mappings.

However, migration is not a guarantee of uninterrupted connectivity. The new path must be usable and valid, and the connection can still fail because of network blocking, timeout, peer failure or other conditions.

## Common Mistakes

- Connection ID is not the same as an IP address.
- Connection migration does not mean the network path never changes.
- QUIC does not guarantee that every network transition will succeed.
- NAT rebinding and deliberate network migration are related but distinct situations.
- Path validation is important for security.
- Connection migration does not eliminate congestion control or flow control.

## Key Takeaways

1. TCP connection identity is traditionally tied to an endpoint tuple.
2. QUIC uses Connection IDs for logical connection identity.
3. QUIC can support connection migration across network paths.
4. NAT rebinding can change the apparent network tuple without changing the logical QUIC connection.
5. New paths require validation.
6. QUIC can maintain the same logical connection and cryptographic state across supported path changes.
7. QUIC combines streams, reliability, security, flow control, congestion control and connection management.
8. HTTP/3 builds directly on this QUIC architecture.

## Reflection Questions

1. Why is tying connection identity to an IP address problematic for mobile clients?
2. What is the purpose of a QUIC Connection ID?
3. What is NAT rebinding?
4. Why does QUIC validate a new path?
5. Why doesn't a network-path change inherently require a new TLS handshake?
6. What are the major components of the complete QUIC architecture?
7. Why is HTTP/3 a natural application layer for QUIC?

## Related Lessons

- Lesson 40 - QUIC Streams & Multiplexing
- Lesson 41 - QUIC Flow Control & Congestion Control
- Lesson 43 - HTTP/3 Fundamentals
