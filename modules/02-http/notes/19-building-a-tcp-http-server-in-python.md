# Building a TCP/HTTP Server in Python

## Objectives

- Build a TCP server using Python sockets.
- Observe raw HTTP requests.
- Understand the boundary between TCP and HTTP.
- Construct and send a basic HTTP response.
- Implement simple HTTP routing.

## Concept Summary

A web server can be built on top of raw TCP sockets. The socket API provides access to the TCP connection, while the application interprets the resulting byte stream as HTTP.

This lesson intentionally avoids HTTP frameworks such as Flask or FastAPI to expose the underlying mechanics.

## Basic Server Lifecycle

```text
Python Program
      |
      v
socket()
      |
      v
bind()
      |
      v
listen()
      |
      v
accept()
      |
      v
TCP Connection
      |
      v
recv()
      |
      v
Raw Bytes
      |
      v
HTTP Parsing
      |
      v
HTTP Response
      |
      v
send()
```

## Minimal TCP Server

```python
import socket

server = socket.socket(
    socket.AF_INET,
    socket.SOCK_STREAM
)

server.bind(("localhost", 8080))
server.listen()

connection, address = server.accept()

data = connection.recv(4096)

print(data.decode())

connection.close()
server.close()
```

## Observing HTTP

A client such as curl can send:

```http
GET /hello HTTP/1.1
Host: localhost:8080
User-Agent: curl
Accept: */*
```

The TCP socket does not know that these bytes represent HTTP. The application interprets the byte stream according to HTTP rules.

```text
TCP Connection
      |
      v
recv()
      |
      v
Python bytes
      |
      | decode / parse
      v
HTTP Request
```

## HTTP Response

A basic response can be manually constructed:

```http
HTTP/1.1 200 OK
Content-Type: text/plain
Content-Length: 13

Hello, World!
```

The server serializes this response into bytes and sends them through the TCP connection.

## Simple Routing

```text
GET /hello
    |
    v
200 OK
Hello, World!

GET /about
    |
    v
200 OK
This is my server.

Any other path
    |
    v
404 Not Found
```

## Important TCP Reality

TCP provides a byte stream, not complete HTTP messages.

A single HTTP request may be split across multiple `recv()` calls, or multiple pieces may be available together. Therefore, production HTTP servers cannot assume that one `recv(4096)` call contains exactly one complete HTTP request.

```text
Sender
  |
  | HTTP bytes
  v
TCP Byte Stream
  |
  +---- recv() #1 ----+
  |                   |
  +---- recv() #2 ----+
  |                   |
  +---- recv() #3 ----+
                      |
                      v
                HTTP Parser
```

The HTTP layer must determine when the request headers are complete and, when necessary, how much body data must be read.

## Key Takeaways

- A TCP socket provides a byte stream.
- HTTP is implemented above the TCP socket.
- `recv()` returns bytes, not HTTP request objects.
- The application must parse HTTP semantics.
- The server must serialize HTTP responses before sending them.
- A production server must correctly handle partial reads and request bodies.

## Reflection Questions

- Why is `recv(4096)` not a reliable HTTP message boundary?
- How does `Content-Length` help determine how much request body to read?
- What would happen if two HTTP requests use the same persistent TCP connection?

## Preview of Next Lesson

The next lesson will build a proper HTTP/1.1 request parser that handles request lines, headers, request bodies and `Content-Length`.

## Related Lessons

- Lesson 14 - TCP
- Lesson 16 - How the Web Works
- Lesson 17 - HTTP Fundamentals
- Lesson 18 - HTTP Request Journey Across Layers
