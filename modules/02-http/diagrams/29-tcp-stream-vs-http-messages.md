# TCP Byte Stream vs HTTP Messages

```text
                    TCP
                     |
                     | Continuous Byte Stream
                     v
+--------------------------------------------------+
| GET /hello HTTP/1.1\r\n                          |
| Host: localhost\r\n\r\n                          |
| GET /about HTTP/1.1\r\n                          |
| Host: localhost\r\n\r\n                          |
+--------------------------------------------------+
                     |
                     |
                     | HTTP Parser
                     v
          +-----------------------+
          |      HTTP Request 1   |
          +-----------------------+
                     |
                     v
          +-----------------------+
          |      HTTP Request 2   |
          +-----------------------+
```

**Key Points**
- TCP provides a continuous ordered byte stream.
- TCP does not know where one HTTP request ends and another begins.
- The HTTP server must parse the byte stream and reconstruct HTTP message boundaries.
- One `recv()` may contain a partial request, one request, or multiple requests.