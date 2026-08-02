# Python TCP Server Lifecycle

```text
                     Python Program
                           |
                           v
                       socket()
                           |
                           v
                        bind()
                           |
                           v
                       listen()
                           |
                           v
                       accept()
                           |
                           v
                    TCP Connection
                           |
                           v
                         recv()
                           |
                           v
                       Raw Bytes
                           |
                           v
                    HTTP Parsing
                           |
                           v
                   HTTP Response
                           |
                           v
                         send()
                           |
                           v
                    TCP Connection
                           |
                           v
                        Client
```

**Key Points**
- `socket()` creates the socket endpoint.
- `bind()` associates the server with an IP address and port.
- `listen()` puts the socket into listening mode.
- `accept()` waits for an incoming TCP connection.
- `recv()` reads bytes from the TCP byte stream.
- The application interprets those bytes as HTTP.
- `send()` writes the serialized HTTP response bytes back to the client.
