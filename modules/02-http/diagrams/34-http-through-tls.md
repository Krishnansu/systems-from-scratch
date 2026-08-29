# HTTP Data Through TLS

```text
Browser
   |
   | GET /products/123 HTTP/1.1
   v
  HTTP
   |
   v
  TLS
   |
   | Encrypt + Authenticate
   v
Encrypted TLS Record
   |
   v
  TCP
   |
   | Reliable Byte Stream
   v
   IP
   |
   v
Network
   |
   v
Server
```

**Server Side**

```text
Network
   |
   v
IP
   |
   v
TCP
   |
   v
TLS
   |
   | Decrypt + Authenticate
   v
HTTP
   |
   v
Application
```

**Key Point**
- TCP transports encrypted TLS bytes and does not understand the HTTP semantics inside them.