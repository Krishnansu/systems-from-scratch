# TCP and HTTP Boundary

```text
                         CLIENT

                    curl / Browser
                           |
                           | HTTP Request
                           v
                    HTTP Message
                           |
                           | Serialize to bytes
                           v
                    TCP Byte Stream
                           |
                           v
                 +-------------------+
                 |   Python Socket   |
                 |                   |
                 |      recv()       |
                 +-------------------+
                           |
                           v
                     Python bytes
                           |
                           | Parse bytes
                           v
                    HTTP Request
                           |
                           v
                    Application
```

**Important Distinction**

TCP does not understand HTTP.

TCP provides:
- Reliable delivery
- Ordered delivery
- A continuous byte stream

HTTP provides:
- Methods
- URLs / request targets
- Headers
- Status codes
- Request and response semantics

The Python application sits above the TCP socket and interprets the byte stream according to HTTP rules.
