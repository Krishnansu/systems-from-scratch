# HTTP/3, QUIC, and UDP

```text
HTTP/3
   │
   ▼
 QUIC
   │
   ├── Reliability
   ├── Congestion Control
   ├── Multiplexed Streams
   ├── Connection Migration
   └── TLS 1.3 Encryption
   │
   ▼
 UDP
   │
   ├── Source Port
   ├── Destination Port
   ├── Length
   └── Checksum
   │
   ▼
 IP
   │
   ▼
Network
```

### Why QUIC Uses UDP

```text
Traditional HTTP/2

HTTP/2
   │
   ▼
 TCP
   │
   └── One ordered byte stream


Modern HTTP/3

HTTP/3
   │
   ▼
 QUIC
   │
   ├── Stream A ──► Independent
   ├── Stream B ──► Independent
   └── Stream C ──► Independent
   │
   ▼
 UDP
```

**Key Points**
- HTTP/3 uses QUIC instead of TCP.
- QUIC uses UDP as its underlying packet transport.
- UDP itself does not provide reliability or ordering guarantees.
- QUIC implements its own reliability, congestion control, encryption, and multiplexed streams.
- QUIC's stream model can avoid some head-of-line blocking problems associated with TCP's single ordered byte stream.
- QUIC is not simply "UDP made reliable"; it is a complete modern transport protocol built over UDP.