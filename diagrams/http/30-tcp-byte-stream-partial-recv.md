# TCP Byte Stream and Partial recv() Calls

TCP does NOT preserve HTTP message boundaries.

A client may send one HTTP request:

```text
GET /hello HTTP/1.1\r\n
Host: localhost:8080\r\n
User-Agent: curl\r\n
Accept: */*\r\n
\r\n
```

But TCP may deliver the bytes in multiple pieces:

```text
                 TCP Byte Stream
                        |
                        v
              +-------------------+
              | GET /hello HTTP/1.1|
              +-------------------+
                        |
                        v
                   recv() #1
                        |
                        v
              "GET /hello HTTP/1.1\r\n"
                        |
                        v
                   recv() #2
                        |
                        v
              "Host: localhost:8080\r\n"
                        |
                        v
                   recv() #3
                        |
                        v
              "User-Agent: curl\r\n"
                        |
                        v
                   recv() #4
                        |
                        v
              "Accept: */*\r\n\r\n"
                        |
                        v
                  HTTP Parser
                        |
                        v
              Complete HTTP Request
```

The exact split is not predictable.

The same request could also arrive in fewer reads or in a different grouping.

**Key Points**
- One `send()` does not guarantee one `recv()`.
- One HTTP request does not necessarily equal one TCP read.
- TCP is a byte stream, not a message protocol.
- The HTTP server must buffer incoming bytes and determine message boundaries itself.
- HTTP headers end at the first `\r\n\r\n` sequence.
- If a request has a body, headers such as `Content-Length` help determine how many additional bytes must be read.
