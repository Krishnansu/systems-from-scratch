# HTTP/2 Multiplexing Over TCP

```text
                 One TCP Connection
                         │
        ┌────────────────┼────────────────┐
        ▼                ▼                ▼
     Stream 1         Stream 3         Stream 5
       HTML             CSS               JS
        │                │                │
        └────────────────┼────────────────┘
                         │
                         ▼
                 Interleaved Data

              A1 B1 C1 A2 B2 C2 A3 B3 C3
```

**Key Points**
- HTTP/2 creates multiple logical streams.
- Streams can be multiplexed over one TCP connection.
- This reduces the need for many parallel TCP connections.
- HTTP/2 still relies on TCP underneath.