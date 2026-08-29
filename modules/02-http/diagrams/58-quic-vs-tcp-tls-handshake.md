# Diagram 36-01 - QUIC vs TCP + TLS Establishment

## TCP + TLS

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

## QUIC

```text
Client                         Server
  |                              |
  | Initial + ClientHello ------>|
  |<----- Initial/Handshake -----|
  |------ Handshake ------------>|
  |                              |
  |------ 1-RTT HTTP/3 --------->|
```

QUIC removes the separate TCP handshake and integrates TLS handshake progress with QUIC connection establishment.
