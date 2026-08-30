# Diagram 115 — HTTP/3 Layer Responsibilities

```text
HTTP/3
  |
  +-- HTTP semantics
  +-- HEADERS / DATA / SETTINGS / GOAWAY
  |
  v
QPACK
  |
  +-- Header compression
  +-- Static table
  +-- Dynamic table
  |
  v
QUIC
  |
  +-- Streams
  +-- Packets
  +-- Reliability
  +-- Loss recovery
  +-- Flow control
  +-- Congestion control
  +-- Connection IDs
  +-- Connection migration
  +-- TLS integration
  |
  v
UDP
  |
  +-- Datagram transport
  |
  v
IP
  |
  +-- Addressing
  +-- Routing
```

The main lesson is separation of responsibilities: higher layers define application meaning while lower layers provide increasingly general transport and network services.
