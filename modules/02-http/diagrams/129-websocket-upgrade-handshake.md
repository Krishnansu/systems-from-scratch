# Diagram 129 — WebSocket Upgrade Handshake

```text
Client
  |
  | HTTP GET /chat
  | Upgrade: websocket
  | Connection: Upgrade
  v
Server
  |
  | HTTP 101 Switching Protocols
  v
WebSocket Mode
  |
  |===============================|
  |     persistent connection     |
  |===============================|
  |
Client <=========================> Server
```
