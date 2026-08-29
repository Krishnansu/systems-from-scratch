# HTTP Request Framing

```text
TCP Byte Buffer

+--------------------------------------------------+
| Request Line                                     |
| GET /hello HTTP/1.1                              |
|                                                  |
| Headers                                          |
| Host: localhost                                  |
| Content-Length: 5                               |
|                                                  |
| \\r\\n\\r\\n                                         |
|                                                  |
| Body                                             |
| Hello                                            |
+--------------------------------------------------+

                    |
                    |
                    v

             HTTP Parser
                    |
          +---------+---------+
          |                   |
          v                   v
     Header End          Content-Length
     \\r\\n\\r\\n                 5
          |                   |
          +---------+---------+
                    |
                    v
              Read 5 Bytes
                    |
                    v
                 Body
                 Hello
```

**Key Points**
- `\\r\\n\\r\\n` marks the end of the HTTP header section.
- `Content-Length` tells the server how many bytes belong to the body.
- The server must wait if the complete body has not arrived yet.
- Correct message framing is essential for persistent connections.