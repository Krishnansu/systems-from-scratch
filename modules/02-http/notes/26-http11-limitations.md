# Lesson 27 - Why HTTP/1.1 Wasn't Enough

## Objectives

- Understand why HTTP/1.1 became limiting as websites grew more complex.
- Understand the relationship between persistent connections and multiple requests.
- Understand HTTP/1.1 pipelining and its ordering requirement.
- Understand head-of-line blocking.
- Understand why browsers used multiple TCP connections.
- Understand why HTTP/2 introduced multiplexed streams.
- Understand the remaining TCP-level limitation in HTTP/2.
- Build the conceptual bridge from HTTP/1.1 → HTTP/2 → QUIC → HTTP/3.

## 1. The Problem with Modern Websites

A modern website may require many resources:

```text
Website
   │
   ├── HTML
   ├── CSS
   ├── JavaScript
   ├── Images
   ├── Fonts
   └── Other resources
```

The browser therefore needs to perform many HTTP requests.

The challenge is how to perform these requests efficiently while avoiding excessive connection overhead and unnecessary waiting.

## 2. One Request at a Time

A simplified HTTP/1.1 connection can look like:

```text
Client                         Server

Request A ------------------->
             <--------------- Response A

Request B ------------------->
             <--------------- Response B

Request C ------------------->
             <--------------- Response C
```

If Request A takes a long time, subsequent requests may have to wait.

```text
Request A ------------------->
                         [processing...]
                         [processing...]
                         [processing...]

             <--------------- Response A

Request B ------------------->
             <--------------- Response B
```

This limits parallelism.

## 3. Multiple TCP Connections

Browsers could use multiple TCP connections to perform requests concurrently:

```text
Connection 1 → Request A
Connection 2 → Request B
Connection 3 → Request C
Connection 4 → Request D
```

This allows parallel work, but TCP connections have overhead.

A connection requires TCP state and connection establishment. With HTTPS, TLS setup may also be involved.

```text
TCP Connection
      ↓
TLS Session
      ↓
HTTP
```

Using many connections therefore means maintaining more transport and security state.

## 4. Persistent Connections

HTTP/1.1 supports persistent connections, allowing multiple HTTP exchanges to use the same TCP connection:

```text
TCP Connection
      │
      ├── Request 1
      ├── Response 1
      ├── Request 2
      ├── Response 2
      ├── Request 3
      ├── Response 3
      └── ...
```

This avoids establishing a new TCP connection for every request.

However, simply reusing one connection does not solve all parallelism problems.

## 5. HTTP/1.1 Pipelining

HTTP/1.1 allows requests to be sent without waiting for the previous response:

```text
Client                         Server

Request A ------------------->
Request B ------------------->
Request C ------------------->

             <--------------- Response A
             <--------------- Response B
             <--------------- Response C
```

The important restriction is that responses must remain in request order.

```text
Request A
Request B
Request C

        ↓

Response A
Response B
Response C
```

The server cannot simply return Response B before Response A even if B is ready first.

## 6. Head-of-Line Blocking

Suppose:

```text
Request A → expensive / slow
Request B → simple / fast
```

Request B may complete first, but if the connection requires ordered responses, B cannot move ahead of A.

This is called head-of-line blocking.

### Queue Analogy

Imagine a checkout queue:

```text
Customer A → complicated purchase
Customer B → one item
Customer C → one item
```

Even though B is ready quickly, B must wait for A.

HTTP/1.1 pipelining has a similar ordering limitation.

## 7. TCP's Role

The deeper limitation comes from TCP's ordered byte stream.

TCP provides:

- Reliable delivery
- Ordered delivery
- Retransmission
- Flow control
- Congestion control

TCP does not understand HTTP requests or responses.

It sees:

```text
byte byte byte byte byte byte...
```

For example, multiple logical pieces of application data might be interleaved conceptually as:

```text
A1 A2 A3 A4 B1 B2 B3 B4
```

If A3 is lost:

```text
A1 A2 [A3 missing] A4 B1 B2 B3 B4
```

TCP cannot deliver the later bytes to the application as though A3 had not existed. It maintains its ordered byte-stream abstraction.

Therefore, unrelated application data sharing the same TCP stream can be affected by packet loss.

## 8. The Fundamental HTTP/1.1 Limitation

The problem can be summarized as:

```text
HTTP/1.1
    ↓
One ordered sequence of HTTP messages
    ↓
TCP
    ↓
One ordered byte stream
```

HTTP/1.1 needs multiple independent requests to make progress efficiently, but its traditional request/response model and pipelining behavior make parallelism difficult.

The alternatives each have drawbacks:

```text
Multiple TCP Connections
        │
        └── Connection / TLS overhead

HTTP/1.1 Pipelining
        │
        └── Ordered responses
                ↓
          Head-of-line blocking
```

## 9. Why HTTP/2 Was Introduced

HTTP/2 changes the HTTP layer by introducing multiple logical streams inside one connection.

Conceptually:

```text
                 One TCP Connection
                         │
        ┌────────────────┼────────────────┐
        ▼                ▼                ▼
     Stream 1         Stream 3         Stream 5
       HTML             CSS               JS
```

Instead of treating the connection as a simple sequence of complete HTTP exchanges, HTTP/2 can multiplex multiple streams over the same connection.

## 10. Multiplexing

Multiplexing allows pieces of different streams to be interleaved:

```text
A1 B1 C1 A2 B2 C2 A3 B3 C3
```

instead of requiring all of A to complete before B and C can make progress:

```text
AAAA BBBB CCCC
```

The major idea is:

```text
Multiple logical streams
          +
One TCP connection
```

This reduces the need to open many separate TCP connections.

## 11. HTTP/2 Still Uses TCP

HTTP/2 solves important HTTP-level limitations, but it still sits on TCP:

```text
HTTP/2
  │
  ├── Stream A
  ├── Stream B
  └── Stream C
          │
          ▼
        TCP
          │
          ▼
   Ordered byte stream
```

Therefore, HTTP/2 cannot completely eliminate TCP-level head-of-line blocking.

If TCP must wait for retransmission of missing bytes, the HTTP/2 layer above TCP can also be affected.

This creates the next major question:

> What if the transport layer itself supported independent streams?

That question leads to QUIC.

## 12. Evolution of HTTP

The progression is:

```text
HTTP/1.1
    │
    │ Limited parallelism
    ▼
Multiple TCP connections
    │
    │ Connection overhead
    ▼
HTTP/1.1 Pipelining
    │
    │ Ordered responses
    ▼
Head-of-line blocking
    │
    ▼
HTTP/2
    │
    │ Multiplexed streams
    ▼
TCP-level head-of-line blocking remains
    │
    ▼
QUIC
    │
    ▼
HTTP/3
```

## Key Takeaways

- HTTP/1.1 persistent connections allow multiple requests to reuse a TCP connection.
- Multiple TCP connections provide parallelism but introduce connection and TLS overhead.
- HTTP/1.1 pipelining allows multiple requests to be sent without waiting for responses.
- Pipelined responses must remain ordered.
- Ordered responses can create head-of-line blocking.
- TCP itself provides a single ordered byte stream.
- HTTP/2 introduces multiplexed logical streams over one TCP connection.
- HTTP/2 improves HTTP-level parallelism but remains subject to TCP-level head-of-line blocking.
- QUIC addresses the transport-level limitation and provides the foundation for HTTP/3.

## Mental Model

```text
HTTP/1.1
   ↓
Need parallel requests
   ↓
Multiple TCP connections OR pipelining
   ↓
Connection overhead OR ordering problems
   ↓
HTTP/2
   ↓
Multiplexed streams
   ↓
But still TCP
   ↓
TCP head-of-line blocking
   ↓
QUIC
   ↓
HTTP/3
```

## Next

The next lesson will examine HTTP/2 itself: its binary framing model, streams, frames and multiplexing.