# Encapsulation & Decapsulation Lifecycle

```text
Application

HTTP Request
      │
      ▼
+----------------------+
| TCP Header           |
| HTTP Data            |
+----------------------+
      │
      ▼
+----------------------+
| IP Header            |
| TCP Segment          |
+----------------------+
      │
      ▼
+----------------------+
| Ethernet Header      |
| IP Packet            |
| Ethernet Trailer     |
+----------------------+
      │
      ▼
Bits
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        Network
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Bits
      │
      ▼
Ethernet Frame
      │
      ▼
IP Packet
      │
      ▼
TCP Segment
      │
      ▼
HTTP Request
```

## Layer Responsibilities

| Layer | Adds |
|------|------|
| Application | HTTP Request |
| Transport | TCP Header |
| Internet | IP Header |
| Link | Ethernet Header & Trailer |
| Physical | Bits on the medium |

## Important
- Every layer wraps the layer above.
- Routers replace Ethernet frames but forward IP packets.
- The original application data remains unchanged throughout the journey.
