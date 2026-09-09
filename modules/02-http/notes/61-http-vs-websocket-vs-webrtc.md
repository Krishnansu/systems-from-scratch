# Lesson 61 — HTTP vs WebSocket vs WebRTC

## Core Mental Model

- HTTP = request/response communication
- WebSocket = persistent bidirectional client/server communication
- WebRTC = real-time peer-to-peer communication

## HTTP

Best for:
- REST APIs
- CRUD operations
- Authentication
- Fetching resources
- Configuration

Mental model:

```text
Client -> Request -> Server
Client <- Response <- Server
```

## WebSocket

Best for:
- Chat
- Live notifications
- Presence
- Multiplayer state
- Collaborative editing
- Real-time dashboards

Mental model:

```text
Client <==== persistent connection ====> Server
```

The server remains involved, which makes WebSocket useful when the application needs centralized authentication, persistence, routing, moderation, offline delivery, or synchronization.

## WebRTC

Best for:
- Video calls
- Audio calls
- Screen sharing
- Peer-to-peer data

Mental model:

```text
Peer A <========== real-time media/data ==========> Peer B
```

WebRTC is designed for real-time media and handles mechanisms such as codecs, congestion control, jitter handling, packet loss recovery, NAT traversal, and secure media transport.

## Why WebRTC for Video Calls?

Video/audio are continuous and bandwidth-heavy. Sending all media through a WebSocket server would make the server process and forward large amounts of traffic while requiring the application to build many media-specific mechanisms itself.

WebRTC can establish a direct peer-to-peer path when possible and is specifically designed for real-time media.

When direct connectivity fails, TURN can relay traffic.

## Why WebSocket for Chat?

Chat messages are small and usually benefit from centralized server involvement:

- Message persistence
- Offline delivery
- Authentication and authorization
- Group messaging
- Moderation
- Read receipts
- Presence
- Message history

WebRTC DataChannels can also carry chat messages, but pure peer-to-peer communication is often less convenient for applications that need the server to coordinate and persist state.

## WebSocket and WebRTC Are Complementary

A real application can use all three:

```text
                    Backend
                   /   |   \\
                  /    |    \\
               HTTP  WebSocket
                |       |
          APIs/Auth   Signaling
                        |
                        v
                     WebRTC
                        |
                 Video / Audio
```

Typical division:

- HTTP -> APIs, authentication, configuration
- WebSocket -> signaling, chat, presence, notifications
- WebRTC -> video, audio, screen sharing, peer-to-peer data

## WebRTC Signaling

WebRTC needs peers to exchange connection information before communication begins. WebRTC does not prescribe a specific signaling protocol.

Signaling can use HTTP, WebSocket, or another mechanism.

```text
Browser A -> Signaling Server -> Browser B
                  |
            SDP / ICE information
```

## Important WebRTC Concepts

- SDP (Session Description Protocol): describes session/media capabilities and parameters.
- ICE (Interactive Connectivity Establishment): finds a viable network path between peers.
- STUN: helps a peer discover its public-facing network address.
- TURN: relays traffic when a direct peer-to-peer path cannot be established.
- NAT traversal: necessary because peers are often behind routers, NATs, or firewalls.
- DataChannel: WebRTC's peer-to-peer data transport.

## Comparison

| | HTTP | WebSocket | WebRTC |
|---|---|---|---|
| Communication | Request/response | Persistent bidirectional | Peer-to-peer |
| Main use | APIs/resources | Real-time server communication | Real-time media/data |
| Chat | Excellent | Excellent | Possible |
| Video/audio | Possible but unsuitable | Possible but unsuitable | Excellent |
| Server role | Central | Central | Signaling + optional TURN |
| NAT traversal | Usually not a concern | Usually not a concern | Major concern |

## Mental Model

```text
HTTP      = "Give me something."
WebSocket = "Let's keep a channel open."
WebRTC    = "Let's communicate directly."
```

## Summary

HTTP, WebSocket, and WebRTC solve different communication problems. WebSocket is optimized for persistent client/server communication, while WebRTC is designed for efficient real-time peer-to-peer media and data. They are often used together rather than as replacements for one another.

## Key Takeaways

1. HTTP is request/response oriented.
2. WebSocket provides a persistent bidirectional client/server channel.
3. WebRTC is designed for real-time peer-to-peer media and data.
4. WebRTC is a natural fit for video/audio because it handles media-specific transport concerns.
5. WebSocket is a natural fit for chat when the server needs to persist, route, authenticate, or moderate messages.
6. WebRTC DataChannels can support chat, but that does not make WebRTC a replacement for WebSocket.
7. WebSocket is commonly useful for WebRTC signaling.
8. HTTP, WebSocket, and WebRTC can coexist in the same application.

## Reflection Questions

1. Why is WebRTC better suited to video calls than WebSocket?
2. Why is WebSocket often preferable for server-backed chat?
3. Why does WebRTC need STUN/TURN while normal HTTP usually does not?
4. What problem does WebRTC signaling solve?
5. Why might a video-calling application use both WebSocket and WebRTC?

## Preview

Next: **Lesson 62 — HTTP Module Consolidation**

The HTTP module will be consolidated from HTTP/1.1 through HTTP/2, QUIC, HTTP/3, sessions, JWT, caching, compression, WebSockets, and WebRTC into one end-to-end systems mental model.
