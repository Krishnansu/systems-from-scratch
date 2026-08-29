# Partial HTTP Request Across Multiple TCP Reads

```text
TCP recv() #1

GET /hello HTTP/1.1\r\n
Host: local

        |
        v

      Buffer
+-------------------------+
| Partial HTTP Request    |
+-------------------------+
        |
        | Request incomplete
        v
      Wait

        |
        | recv() #2
        v

host\r\n\r\n

        |
        v

      Buffer
+-------------------------+
| Complete HTTP Request  |
+-------------------------+
        |
        v
    HTTP Parser
        |
        v
    HTTP Request
```

**Key Points**
- A request can be split across multiple TCP reads.
- The server must not process an incomplete request.
- The partial bytes remain buffered until more data arrives.
- TCP segmentation and socket read boundaries are independent of HTTP message boundaries.