# Lesson 21 - HTTP/1.1 Persistent Connections and Buffer Management

## Objectives

- Understand the difference between HTTP statelessness and TCP connection persistence.
- Understand how HTTP/1.1 reuses TCP connections.
- Learn how a server handles multiple HTTP requests over one connection.
- Understand why request buffering is essential for persistent connections.
- Understand HTTP/1.1 request ordering and pipelining at a high level.

## Concept Summary

HTTP is stateless, but the underlying TCP connection can remain open and carry multiple HTTP requests and responses.

```text
HTTP
  |
  | Stateless application protocol
  v
Multiple HTTP Requests
  |
  v
Persistent TCP Connection
  |
  | Reliable ordered byte stream
  v
IP
```

Statelessness answers whether the HTTP application protocol requires the server to remember previous requests.

Persistence answers whether the underlying TCP connection can be reused for additional requests.

These are separate concepts.

## Core Ideas

### 1. Persistent Connections

Without persistence:

```text
TCP Connection 1
    |
    +-- Request 1
    +-- Response 1
    +-- Close

TCP Connection 2
    |
    +-- Request 2
    +-- Response 2
    +-- Close
```

With persistence:

```text
One TCP Connection
    |
    +-- Request 1
    +-- Response 1
    |
    +-- Request 2
    +-- Response 2
    |
    +-- Request 3
    +-- Response 3
    |
    +-- Eventually Close
```

HTTP/1.1 uses persistent connections by default unless the connection is closed or otherwise terminated.

### 2. Connection Lifetime

A persistent connection is not permanent.

It may close because of:

- Server idle timeout.
- Client idle timeout.
- `Connection: close`.
- Server shutdown.
- Resource limits.
- Network failure.

```text
Persistent Connection
        |
        v
Requests / Responses
        |
        v
Idle or Close Condition
        |
        v
TCP Connection Closed
```

The exact idle timeout is generally a server or infrastructure configuration rather than one universal HTTP value.

### 3. Buffer Management

A single TCP read may contain multiple HTTP requests.

```text
TCP Buffer
+-------------------+-------------------+
|    Request 1      |    Request 2      |
+-------------------+-------------------+
```

After parsing Request 1, the server must preserve Request 2.

```text
Before Parsing
+-------------------+-------------------+
|    Request 1      |    Request 2      |
+-------------------+-------------------+

After Parsing Request 1
+-------------------+
|    Request 2      |
+-------------------+
```

The unconsumed bytes become the new buffer.

### 4. Two-Level Server Loop

A persistent HTTP server conceptually needs two loops.

```text
Outer Loop
    |
    +-- recv() more TCP bytes
    |
    +-- Append bytes to buffer
    |
    v
Inner Loop
    |
    +-- Is there a complete HTTP request?
          |
          +-- No -> Wait for more bytes
          |
          +-- Yes
                |
                +-- Parse request
                +-- Remove consumed bytes
                +-- Process request
                +-- Send response
                +-- Check for another request
```

The outer loop obtains more bytes from TCP.

The inner loop processes all complete HTTP requests already available in the buffer.

### 5. Partial and Multiple Requests

The buffer may contain:

```text
Complete Request 1 + Partial Request 2
```

The server should:

1. Parse Request 1.
2. Send Response 1.
3. Remove Request 1 from the buffer.
4. Keep the partial Request 2.
5. Receive more TCP bytes.
6. Append them to the existing buffer.
7. Parse Request 2 when complete.

```text
recv() #1
    |
    v
+-------------------+----------------------+
| Complete Request 1| Partial Request 2    |
+-------------------+----------------------+
          |
          v
    Process Request 1
          |
          v
    Response 1
          |
          v
    Keep Partial Request 2
          |
          v
recv() #2
          |
          v
    Complete Request 2
```

## HTTP/1.1 Request Ordering

HTTP/1.1 requests and responses are ordered on a connection.

Conceptually:

```text
Request 1
    |
    v
Response 1
    |
    v
Request 2
    |
    v
Response 2
```

HTTP/1.1 pipelining allowed clients to send multiple requests without waiting for each response, but responses still needed to preserve ordering.

```text
Client                         Server

GET /a ----------------------->
GET /b ----------------------->

        <---------------------- 200 OK /a
        <---------------------- 200 OK /b
```

If `/a` is slow, `/b` can be affected by the ordering requirement. This contributes to head-of-line blocking concerns and motivates HTTP/2 multiplexing.

## Practical Example

A simplified connection handler can conceptually follow:

```python
buffer = b""

while True:
    data = connection.recv(4096)

    if not data:
        break

    buffer += data

    while True:
        result = parse_request(buffer)

        if result is None:
            break

        request, buffer = result

        response = create_response(request)

        connection.sendall(response)
```

The key design is that `parse_request()` returns both:

```text
Parsed Request
+
Remaining Buffer
```

This allows the server to process multiple requests received together without losing bytes belonging to later requests.

## Production Perspective

Production HTTP servers must carefully manage persistent connections, buffering, timeouts and resource limits. Keeping connections alive improves efficiency by avoiding repeated TCP connection establishment, but idle connections consume server resources.

Persistent connections also make correct message framing essential. The server must know exactly where one HTTP request ends before it can safely parse the next request.

## Common Mistakes

- Assuming persistent means permanent.
- Confusing HTTP statelessness with TCP connection lifetime.
- Closing the TCP connection after every response.
- Discarding bytes after the first parsed request.
- Assuming each `recv()` corresponds to exactly one HTTP request.
- Ignoring connection timeout and resource management.

## Key Takeaways

- HTTP can remain stateless while TCP connections remain persistent.
- HTTP/1.1 can reuse one TCP connection for multiple requests.
- Persistent connections reduce the overhead of establishing new TCP connections.
- Servers need a buffer because TCP does not preserve HTTP message boundaries.
- A parser must return both the parsed request and remaining unconsumed bytes.
- Multiple complete requests may exist in one TCP receive buffer.
- Partial requests must remain buffered until more data arrives.
- HTTP/1.1 request ordering creates limitations that HTTP/2 later addresses with multiplexing.

## Reflection Questions

- Why can HTTP be stateless while a TCP connection remains open?
- What should happen if one `recv()` contains two complete HTTP requests?
- What should happen if a request is split across three `recv()` calls?
- Why must a server preserve bytes belonging to a second request?

## Related Lessons

- Lesson 14 - Transmission Control Protocol (TCP)
- Lesson 17 - HTTP Fundamentals
- Lesson 18 - HTTP Request Journey Across All Layers
- Lesson 19 - Building a TCP/HTTP Server in Python
- Lesson 20 - HTTP Request Parsing
