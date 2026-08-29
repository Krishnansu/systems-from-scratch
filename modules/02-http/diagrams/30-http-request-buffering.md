# HTTP Request Buffering

```text
                TCP Socket
                    |
                    | recv()
                    v
              +-----------+
              |  Buffer   |
              +-----------+
                    |
                    v
          Is Request Complete?
                    |
             +------+------+
             |             |
            NO            YES
             |             |
             v             v
      Keep in Buffer   Parse Request
             |             |
             |             v
             |       Process Request
             |             |
             |             v
             |       Send Response
             |             |
             |             v
             |      Remove Consumed
             |           Bytes
             |             |
             +-------------+
                    |
                    v
              recv() more
```

**Key Points**
- Incoming TCP bytes are accumulated in a buffer.
- The server waits until a complete HTTP request is available.
- Incomplete requests remain in the buffer.
- After parsing a request, consumed bytes are removed while remaining bytes are preserved.