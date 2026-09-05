# Lesson 57 — WebSockets

## Objectives

- Understand why WebSockets exist.
- Understand the HTTP Upgrade handshake.
- Understand persistent bidirectional communication.
- Understand WebSocket frames and control messages.
- Understand production concerns around scaling, load balancing, and reconnection.

## Prerequisites

- HTTP request/response model
- HTTP persistent connections
- TCP fundamentals
- Lesson 56 — Compression

## Theory

Traditional HTTP follows a request/response model:

```text
Client ── request ──> Server
Client <─ response ── Server
```

Applications such as chat, multiplayer games, collaborative tools, and live dashboards often need the server to send data whenever an event occurs.

Polling repeatedly creates requests, while long polling keeps an HTTP request open until an event occurs. WebSockets provide a persistent, bidirectional communication channel.

A WebSocket connection begins with an HTTP Upgrade request:

```http
GET /chat HTTP/1.1
Host: example.com
Upgrade: websocket
Connection: Upgrade
Sec-WebSocket-Key: <random-value>
Sec-WebSocket-Version: 13
```

The server accepts with:

```http
HTTP/1.1 101 Switching Protocols
Upgrade: websocket
Connection: Upgrade
Sec-WebSocket-Accept: <computed-value>
```

After the handshake, communication uses WebSocket frames rather than normal HTTP request/response messages.

## Core Ideas

### 1. Persistent Bidirectional Channel

```text
Client <=====================> Server
             WebSocket
```

Either side can send messages independently.

### 2. WebSocket Framing

WebSocket provides message framing over the underlying transport.

Common frame types:

- `0x1` — Text
- `0x2` — Binary
- `0x8` — Close
- `0x9` — Ping
- `0xA` — Pong

### 3. Text vs Binary

WebSocket does not require JSON. JSON is an application-level format that can be carried inside text frames. Binary frames can carry arbitrary binary application data.

### 4. Ping/Pong

Ping/pong can be used as a heartbeat mechanism to detect broken or unusable connections.

```text
Server ─── PING ───> Client
Server <── PONG ──── Client
```

### 5. Closing

WebSocket defines a protocol-level close handshake before the underlying connection terminates.

### 6. Scaling

Long-lived connections introduce infrastructure concerns:

- large numbers of concurrent connections
- connection ownership by individual servers
- load balancing
- reconnection after failures
- shared state
- cross-server message delivery

If users are connected to different WebSocket servers, a shared broker or messaging system can distribute events between them.

### 7. Reconnection and Resynchronization

A connection can fail because of server, network, or intermediary failures. Production clients commonly reconnect using backoff and may need to resynchronize missed state after reconnecting.

## Real World Example

Chat application:

```text
User A
  |
  v
WebSocket Server 1
  |
  v
Message Broker
  |
  v
WebSocket Server 2
  |
  v
User B
```

User A and User B can maintain WebSocket connections to different application servers while the message broker distributes events between those servers.

## Deep Dive

### WebSocket vs HTTP

| Property | HTTP | WebSocket |
|---|---|---|
| Communication model | Request/response | Bidirectional |
| Connection | Often reusable | Long-lived |
| Server can initiate application data | Not normally | Yes |
| Message structure | HTTP messages | WebSocket frames |
| Typical use | APIs, CRUD, documents | Real-time communication |

WebSockets are not universally better than HTTP. They solve a different communication pattern.

### WebSocket vs Raw TCP

TCP provides a reliable ordered byte stream. It does not define application-level messages. WebSocket adds standardized framing, control messages, and close semantics on top of the transport.

### WebSockets and Load Balancers

An established WebSocket connection is associated with its current backend connection. If that backend fails, the client generally reconnects and may be routed to another server.

### WebSockets and Shared State

When multiple WebSocket servers exist, connection-local state is not automatically shared. Brokers, shared stores, or other messaging infrastructure may be required to coordinate events across servers.

## Hands-on Exercise

1. Build a minimal WebSocket server and client.
2. Open two clients simultaneously.
3. Send a message from one client and broadcast it to the other.
4. Kill the server and observe the client connection failure.
5. Implement reconnection with a small backoff.
6. Restart the server and observe what application state the client needs to resynchronize.

## Common Misconceptions

- WebSockets are not simply HTTP requests that never finish.
- WebSockets do not require JSON.
- WebSockets are not inherently faster than HTTP.
- WebSocket connections can still fail because the underlying network fails.
- A load balancer cannot simply migrate an established TCP/WebSocket connection to another backend.
- WebSockets do not automatically solve cross-server state or message distribution.

## Summary

WebSockets provide a persistent, bidirectional communication channel suited to applications that require server-initiated and client-initiated events. They begin with an HTTP Upgrade handshake and then use WebSocket frames for communication. Their production complexity comes primarily from managing large numbers of long-lived connections, failures, reconnection, and distributed state.

## Key Takeaways

- WebSockets address the limitations of HTTP request/response for real-time bidirectional communication.
- The connection begins with an HTTP Upgrade handshake.
- `101 Switching Protocols` confirms the protocol switch.
- WebSocket frames provide standardized application-level framing and control messages.
- Text and binary messages are both supported.
- Ping/pong helps monitor connection health.
- Long-lived connections create scaling and failure-management concerns.
- Production systems often need reconnection, resynchronization, and shared messaging infrastructure.

## Reflection Questions

1. Why is polling inefficient for real-time applications?
2. Why does WebSocket start with an HTTP Upgrade handshake?
3. Why is raw TCP not equivalent to WebSocket?
4. What happens to a WebSocket connection when its backend server fails?
5. How can two clients connected to different WebSocket servers exchange messages?
6. When might SSE be preferable to WebSockets?

## What's Next

Lesson 58 — Consolidation
