# Lesson 60 — WebSockets at Scale

## Objectives

- Understand horizontal scaling of WebSocket servers.
- Understand connection ownership and load balancing.
- Understand cross-server messaging and fan-out.
- Understand connection registries and presence.
- Understand backend failure and client reconnection.
- Understand why message brokers become useful.

## Concept Summary

A single WebSocket server can maintain many persistent connections, but large systems require multiple WebSocket servers. Established WebSocket connections remain attached to the server that owns them, so scaling introduces distributed connection state and cross-server messaging problems.

## Core Ideas

- **Horizontal scaling:** run multiple WebSocket servers behind a load balancer.
- **Connection ownership:** once established, a WebSocket connection normally remains attached to one server.
- **Sticky sessions:** can simplify connection-oriented routing but do not solve server failure or cross-server messaging.
- **Connection registry:** maps users/connections to the WebSocket server currently owning them.
- **Message broker:** allows WebSocket servers to exchange events when the target client is connected elsewhere.
- **Fan-out:** one event may need to be delivered to clients connected to many different servers.
- **Presence:** online/offline state becomes distributed state when clients are spread across servers.
- **Server failure:** existing connections are lost; clients reconnect to another available server and may resume/resynchronize state.

## Architecture

```text
                       Internet
                           |
                           v
                    Load Balancer
                    /     |     \\
                   v      v      v
                 WS-1   WS-2   WS-3
                   \\      |      /
                    \\     |     /
                     v    v    v
                   Message Broker
                         |
              +----------+----------+
              v                     v
        Backend Services       Presence /
              |                Registry
              v
           Database
```

## Cross-Server Messaging

Example:

```text
Client A -> WS-1 -> Message Broker -> WS-2 -> Client B
```

WS-1 does not need to own Client B's socket. The broker distributes the event to the appropriate WebSocket server, which delivers it through its local connection.

## Connection Registry

A distributed registry can conceptually maintain:

```text
user_id -> server_id

Alice      -> WS-1
Krishnansu -> WS-2
Emma       -> WS-3
```

The exact implementation depends on the system and consistency requirements.

## Failure Recovery

If WS-2 fails:

```text
Client -> WS-2  X

Client -> Load Balancer -> WS-3
                      |
                      v
                authenticate
                      |
                 resume/resync
```

The existing TCP/WebSocket connection is not transparently moved between servers.

## Production Perspective

At scale, WebSocket infrastructure is not just a socket server. It becomes a distributed system involving:

- Load balancing
- Long-lived connection management
- Connection/presence registries
- Cross-server event delivery
- Broadcasting and fan-out
- Failure detection and recovery
- Reconnection and state synchronization

Redis Pub/Sub can be used as a conceptual example of a message-distribution layer, but messaging systems will be studied in depth in the dedicated Messaging module.

## Common Mistakes

- Assuming a load balancer can migrate an existing WebSocket connection.
- Assuming sticky sessions solve all scaling problems.
- Assuming every WebSocket server can directly access every client's socket.
- Treating connection reliability as message reliability.
- Ignoring reconnect behavior after server failure.

## Key Takeaways

- WebSockets scale horizontally by running multiple connection-owning servers.
- Established connections remain associated with their current server.
- Multiple servers create distributed connection-state problems.
- Message brokers enable cross-server communication and fan-out.
- Presence and connection registries become distributed state.
- Server failure requires client reconnection and potentially state recovery.
- WebSockets at scale are fundamentally a distributed-systems problem.

## Reflection Questions

1. Why cannot a load balancer simply move an existing WebSocket connection to another server?
2. Why does a message broker become useful with multiple WebSocket servers?
3. Where could `user_id -> server_id` information be maintained?
4. What happens to connected clients when their WebSocket server crashes?
5. Why are sticky sessions not a complete scaling solution?

## Related Lessons

- Lesson 57 — WebSockets
- Lesson 58 — WebSocket Protocol Deep Dive
- Lesson 59 — WebSocket Lifecycle & Reliability
- Lesson 61 — HTTP vs WebSocket vs WebRTC
