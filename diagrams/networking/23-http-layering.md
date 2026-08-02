# Where HTTP Fits in the Network Stack

```text
┌───────────────────────────────────────────┐
│              APPLICATION                  │
│                                           │
│   Browser / API Client / Backend Service  │
└─────────────────────┬─────────────────────┘
                      │
                      │ HTTP
                      ▼
┌───────────────────────────────────────────┐
│             APPLICATION PROTOCOL          │
│                                           │
│          HTTP / HTTP/2 / HTTP/3           │
└──────────────┬───────────────────┬────────┘
               │                   │
               │ HTTP/1.1, HTTP/2  │ HTTP/3
               ▼                   ▼
             TCP                  QUIC
               │                   │
               │                   ▼
               │                  UDP
               │                   │
               └─────────┬─────────┘
                         ▼
                        IP
                         │
                         ▼
                 Ethernet / Wi-Fi
                         │
                         ▼
                      Network
```

**Key Points**
- The browser is an application that uses HTTP.
- HTTP defines application-level communication semantics.
- TCP transports HTTP/1.1 and HTTP/2 data as a reliable byte stream.
- HTTP/3 uses QUIC as its transport protocol.
- QUIC uses UDP as its underlying packet transport.
- IP handles addressing and routing.
- Lower layers transport the data across the physical network.