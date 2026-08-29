# Persistent HTTP/1.1 Server Loop

```text
                 accept()
                    |
                    v
            TCP Connection
                    |
                    v
              buffer = b''
                    |
                    v
          +-------------------+
          | recv() more bytes  |<--------------------+
          +-------------------+                     |
                    |                               |
                    v                               |
             Append to Buffer                       |
                    |                               |
                    v                               |
          Complete Request?                         |
             /          \
           NO            YES
            |              |
            v              v
       recv() more     Parse Request
                           |
                           v
                      Process Request
                           |
                           v
                      Send Response
                           |
                           v
                  Remove Consumed Bytes
                           |
                           v
                 Another Complete Request?
                      /          \
                    YES           NO
                     |             |
                     +-------------+-----> recv()
```

**Key Points**
- The outer loop receives more bytes from TCP.
- The inner loop processes complete requests already present in the buffer.
- Partial requests cause the server to wait for more data.
- Multiple requests can be processed without closing the TCP connection.