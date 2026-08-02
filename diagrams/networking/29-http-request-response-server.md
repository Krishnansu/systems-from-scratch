# HTTP Request and Response Through a Python Server

```text
Client
  |
  | GET /hello HTTP/1.1
  | Host: localhost:8080
  v
TCP Connection
  |
  v
Python Socket
  |
  | recv()
  v
Raw Bytes
  |
  v
HTTP Parser
  |
  v
+----------------------+
| Method: GET          |
| Path: /hello         |
| Version: HTTP/1.1    |
+----------------------+
  |
  v
Router
  |
  | /hello
  v
Handler
  |
  v
Create Response
  |
  v
HTTP/1.1 200 OK
Content-Type: text/plain
Content-Length: 13

Hello, World!
  |
  | encode()
  v
TCP Socket
  |
  | send()
  v
TCP Connection
  |
  v
Client
  |
  v
Hello, World!
```

**Key Points**
- The client sends an HTTP request over a TCP connection.
- The socket receives bytes, not an HTTP object.
- The application parses the bytes into HTTP components.
- The router selects a handler based on the request path.
- The handler creates an HTTP response.
- The response is serialized into bytes and sent through TCP.
