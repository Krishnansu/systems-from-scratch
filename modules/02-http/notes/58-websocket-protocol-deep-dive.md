# Lesson 58 — WebSocket Protocol Deep Dive

## Objectives

- Understand the WebSocket frame structure.
- Understand FIN, opcodes, masking, payload lengths, and fragmentation.
- Distinguish data frames from control frames.
- Understand Ping/Pong and the WebSocket close handshake.
- Understand how WebSocket framing sits on top of TCP's byte stream.

## Core Ideas

After the HTTP Upgrade handshake, communication switches from HTTP request/response to the WebSocket protocol. WebSocket messages are transmitted as frames over a TCP connection.

- `FIN` indicates whether a frame is the final fragment of a message.
- `Opcode` identifies the frame type.
- `0x1` = Text, `0x2` = Binary, `0x8` = Close, `0x9` = Ping, `0xA` = Pong.
- Text frames contain UTF-8 text; JSON is only an application-level choice.
- Binary frames carry arbitrary binary application data.
- Client → server frames are masked; server → client frames are not.
- Masking is not encryption. TLS provides confidentiality for `wss://`.
- Payload length uses compact variable-length encoding.
- A logical message can be fragmented across multiple frames.
- Control frames include Close, Ping, and Pong and can appear between fragmented data frames.
- TCP provides a byte stream; WebSocket provides frame/message structure above it.

## Frame Mental Model

```text
┌───────────────┐
│ FIN / Opcode  │
├───────────────┤
│ MASK / Length │
├───────────────┤
│ Masking Key   │  ← client → server
├───────────────┤
│ Payload       │
└───────────────┘
```

## Message vs Frame

```text
Logical Message
      │
      ├── Frame
      ├── Frame
      └── Frame
```

A message may consist of multiple frames. TCP itself only provides a byte stream and has no concept of WebSocket message boundaries.

## Masking

Client-to-server frames are masked using a fresh 4-byte masking key. Masking prevents a client from directly controlling predictable bytes through intermediaries; it does **not** provide confidentiality.

```text
payload XOR masking_key → masked payload
```

For confidentiality, use TLS:

```text
WebSocket
    ↓
TLS
    ↓
TCP
```

## Control Frames

```text
0x8 → Close
0x9 → Ping
0xA → Pong
```

Ping/Pong can be used for liveness detection. Close frames support a graceful WebSocket shutdown.

## Practical Example

```javascript
socket.send(JSON.stringify({
  type: "chat",
  message: "hello"
}));
```

The application creates JSON, WebSocket wraps it in a text frame, and TCP transports the resulting bytes.

## Key Takeaways

- WebSocket is a framed protocol running traditionally over TCP.
- Frames provide structure on top of TCP's byte stream.
- Masking is not encryption.
- Ping/Pong and Close are protocol-level control mechanisms.
- A message and a frame are different concepts.

## Reflection Questions

1. Why does WebSocket need framing when TCP already transports bytes reliably?
2. Why is masking not equivalent to encryption?
3. What is the difference between a WebSocket message and a frame?
4. Why can control frames appear between fragmented data frames?

## Related Lessons

- Lesson 57 — WebSockets
- Lesson 59 — WebSocket Lifecycle & Reliability
- Lesson 60 — WebSockets at Scale
