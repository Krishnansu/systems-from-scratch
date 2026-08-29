# Lesson 27 - HTTP/2 Multiplexing

## What I Learned

HTTP/2 multiplexing allows multiple logical HTTP streams to share a single TCP connection.

Instead of requiring all data for one request to be completed before another request progresses, frames belonging to different streams can be interleaved.

## Without Multiplexing

Conceptually:

```text
AAAA BBBB CCCC
```

One logical exchange is completed before the next progresses.

## With HTTP/2 Multiplexing

```text
A1 B1 C1 A2 B2 C2 A3 B3 C3
```

Data from multiple streams can be interleaved.

## Architecture

```text
                 One TCP Connection
                         |
        +----------------+----------------+
        |                |                |
        v                v                v
     Stream 1         Stream 3         Stream 5
       HTML             CSS               JS
        |                |                |
      Frames           Frames           Frames
        \                |                /
         +---------------+---------------+
                         |
                         v
                    TCP byte stream
```

## Why This Helps

HTTP/1.1 often needed multiple TCP connections to achieve parallelism.

HTTP/2 can instead use:

```text
One TCP connection
       |
       +-- Stream 1
       +-- Stream 3
       +-- Stream 5
       +-- Stream 7
```

This reduces connection overhead while allowing multiple logical exchanges to progress concurrently.

## Important Boundary

HTTP/2 understands streams. TCP does not.

```text
HTTP/2
  ↓
Streams
  ↓
Frames
  ↓
TCP
  ↓
One ordered byte stream
```

Therefore HTTP/2 multiplexing is an HTTP-layer feature, not a TCP-layer feature.

## Key Insight

HTTP/2 solved the HTTP/1.1 request-level parallelism problem by introducing multiplexed streams, but it still inherits TCP's ordered byte-stream behavior.

This leaves one major problem for the next stage of the HTTP evolution: TCP-level head-of-line blocking.