# Complete HTTPS Request with TLS 1.3

```text
Browser
   |
   | https://example.com/products/123
   v
DNS Resolution
   |
   v
IP Address Found
   |
   v
TCP Three-Way Handshake
   |
   v
TCP Connection Established
   |
   v
TLS 1.3 Handshake
   |
   +-- ClientHello
   +-- ServerHello
   +-- Certificate
   +-- Certificate Validation
   +-- CertificateVerify
   +-- ECDHE Key Exchange
   +-- Traffic Key Derivation
   |
   v
Secure TLS Connection
   |
   v
HTTP Request
   |
   | GET /products/123
   v
TLS Encryption
   |
   v
Encrypted TLS Record
   |
   v
TCP
   |
   v
IP
   |
   v
Network / Routers
   |
   v
Server
   |
   v
IP -> TCP -> TLS
   |
   v
HTTP Server
   |
   v
Application
```

**Return Path**

```text
HTTP Response
      |
      v
TLS Encryption
      |
      v
TCP
      |
      v
IP
      |
      v
Network
      |
      v
Browser
      |
      v
TLS Decryption + Authentication
      |
      v
HTTP Response
```

**Key Points**
- DNS finds the server address before the connection is established.
- TCP establishes reliable transport.
- TLS establishes authentication and cryptographic keys.
- HTTP application data is then encrypted by TLS.
- TCP transports encrypted TLS records.
- The server reverses the process to recover the HTTP request.