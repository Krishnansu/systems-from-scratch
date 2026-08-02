# Python HTTP Server - Full Architecture

```text
                         CLIENT
                    Browser / curl
                           |
                           | HTTP Request
                           v
                    TCP Connection
                           |
                           v
                     Python Socket
                           |
                           | recv()
                           v
                      Byte Buffer
                           |
                           v
                    HTTP/1.1 Parser
                           |
              +------------+------------+
              |            |            |
              v            v            v
           Method        Headers       Body
              |            |            |
              +------------+------------+
                           |
                           v
                     Request Object
                           |
                           v
                         Router
                           |
                           v
                        Handler
                           |
              +------------+------------+
              |            |            |
              v            v            v
           Business      Cache       Database
           Logic
              |            |            |
              +------------+------------+
                           |
                           v
                    Response Object
                           |
                           v
                   HTTP Serializer
                           |
                           v
                         Bytes
                           |
                           | send()
                           v
                    TCP Connection
                           |
                           v
                         Client
```

**Key Points**
- The socket layer handles TCP connections and bytes.
- The HTTP parser converts bytes into structured request information.
- The router selects application logic.
- Handlers may interact with caches and databases.
- The response is converted back into HTTP bytes.
- TCP transports those bytes back to the client.

This architecture is the foundation for the HTTP server that will be developed in subsequent lessons.
