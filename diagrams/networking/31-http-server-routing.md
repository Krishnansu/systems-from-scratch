# Simple HTTP Server Routing

```text
                       HTTP Request
                            |
                            v
                     HTTP Parser
                            |
                            v
                  Method + Path + Headers
                            |
                            v
                         Router
                            |
             +--------------+--------------+
             |              |              |
             v              v              v
          /hello         /about         /other
             |              |              |
             v              v              v
       Hello Handler   About Handler   404 Handler
             |              |              |
             v              v              v
          200 OK         200 OK         404 Not Found
             |              |              |
             +--------------+--------------+
                            |
                            v
                    HTTP Response
                            |
                            v
                       TCP Socket
                            |
                            v
                          Client
```

**Key Points**
- The HTTP parser extracts the request path.
- The router maps the path to application logic.
- Different paths can execute different handlers.
- The handler produces an HTTP response.
- The response is sent back through the TCP connection.
