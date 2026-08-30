# Diagram 112 — HTTP/3 Request End-to-End

```text
                         HTTP/3 REQUEST

Client
  |
  | GET /index.html
  v
HTTP/3
  |
  | HEADERS frame
  v
QPACK
  |
  | compressed header block
  v
QUIC Stream 7
  |
  | STREAM frame
  v
QUIC Packet
  |
  v
UDP Datagram
  |
  v
IP Packet
  |
  v
================ NETWORK ================
  |
  v
IP Packet
  |
  v
UDP Datagram
  |
  v
QUIC Packet
  |
  v
QUIC STREAM frame
  |
  v
QUIC Stream 7
  |
  v
HTTP/3 HEADERS
  |
  v
QPACK decode
  |
  v
HTTP Request
  |
  v
Server Application
```

The diagram shows the complete request path and the reverse decapsulation path at the server.
