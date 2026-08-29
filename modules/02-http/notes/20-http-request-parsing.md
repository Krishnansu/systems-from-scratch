# Lesson 20 - HTTP Request Parsing

## Objectives

- Understand how a TCP byte stream becomes an HTTP request.
- Understand why `recv()` does not necessarily return one complete HTTP request.
- Learn HTTP request framing using headers and `Content-Length`.
- Build a clear mental model of buffering and partial requests.

## Concept Summary

TCP provides a reliable, ordered byte stream. It does not understand HTTP message boundaries.

An HTTP server therefore needs to collect TCP bytes in a buffer and parse the bytes according to HTTP rules.

```text
TCP Socket
    |
    | Raw bytes
    v
Receive Buffer
    |
    v
Find HTTP Headers
    |
    v
Parse Request Line
    |
    v
Parse Headers
    |
    v
Determine Body Length
    |
    v
Read Complete Request
    |
    v
HTTPRequest Object
```

## Core Ideas

### 1. TCP Does Not Preserve HTTP Messages

A single `recv()` call may contain:

- Less than one HTTP request.
- Exactly one HTTP request.
- Multiple HTTP requests.

```text
TCP recv()
    |
    +-- Partial Request
    |
    +-- Complete Request
    |
    +-- Request 1 + Request 2
```

The application must therefore implement its own message parsing.

### 2. HTTP Headers End at CRLF CRLF

The end of the HTTP header section is represented by:

```text
\\r\\n\\r\\n
```

Conceptually:

```text
GET /hello HTTP/1.1\\r\\n
Host: localhost\\r\\n
Content-Length: 5\\r\\n
\\r\\n
Hello
```

The parser first searches for the end of the headers.

### 3. Content-Length Determines Body Size

For requests with a body, the server needs to know how many bytes belong to the body.

```text
Headers
    |
    v
Content-Length: 5
    |
    v
Read exactly 5 bytes
    |
    v
Hello
```

If the buffer does not yet contain all required bytes, the request is incomplete and the server must wait for more data.

### 4. Buffering Partial Requests

A request may arrive across multiple TCP reads.

```text
recv() #1
    |
    v
GET /hello HTTP/1.1\\r\\n
Host: local
    |
    v
Incomplete
    |
    v
Keep in Buffer
    |
    v
recv() #2
    |
    v
host\\r\\n\\r\\n
    |
    v
Complete HTTP Request
```

The server must never assume that one `recv()` contains a complete request.

### 5. Parsing the Request

The parser extracts:

- Method
- Path
- HTTP version
- Headers
- Body

These values can be represented as an `HTTPRequest` object.

```text
Raw TCP Bytes
      |
      v
HTTP Parser
      |
      +-- Method
      +-- Path
      +-- Version
      +-- Headers
      +-- Body
      |
      v
HTTPRequest
```

## Practical Example

A simplified parser follows this flow:

```python
header_end = buffer.find(b"\\r\\n\\r\\n")

if header_end == -1:
    return None
```

The parser then extracts headers and determines the body size using `Content-Length`.

If the complete request has not arrived:

```python
if len(buffer) < body_end:
    return None
```

Once the complete request is available, it can be converted into an `HTTPRequest` object.

## Production Perspective

Real HTTP servers must handle TCP fragmentation and coalescing correctly. The operating system and TCP stack are free to split or combine network data independently of HTTP message boundaries.

Production servers therefore maintain receive buffers and implement robust HTTP message framing instead of assuming one socket read equals one HTTP request.

## Common Mistakes

- Assuming one `recv()` equals one HTTP request.
- Assuming headers and body always arrive together.
- Ignoring `Content-Length` when parsing request bodies.
- Treating TCP packets as equivalent to HTTP messages.
- Discarding bytes that belong to the next request.

## Key Takeaways

- TCP is a byte stream, not a message protocol.
- HTTP servers must implement HTTP message parsing above TCP.
- Headers end at `\\r\\n\\r\\n`.
- `Content-Length` can determine the size of a request body.
- Partial requests must remain buffered until complete.
- A robust server must correctly handle fragmented and coalesced TCP data.

## Reflection Questions

- Why can't a server assume one `recv()` contains one HTTP request?
- What happens if `Content-Length` says 100 bytes but only 50 have arrived?
- What happens if one `recv()` contains two complete HTTP requests?

## Related Lessons

- Lesson 14 - Transmission Control Protocol (TCP)
- Lesson 17 - HTTP Fundamentals
- Lesson 18 - HTTP Request Journey Across All Layers
- Lesson 19 - Building a TCP/HTTP Server in Python
- Lesson 21 - HTTP/1.1 Persistent Connections and Buffer Management
