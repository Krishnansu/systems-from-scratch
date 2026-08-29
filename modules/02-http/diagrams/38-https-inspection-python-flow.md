# HTTPS Inspection with Python

```text
Python Program
      │
      │ DNS lookup
      ▼
     DNS
      │
      ▼
 IP Address
      │
      │ socket.create_connection()
      ▼
 TCP Three-Way Handshake
      │
      ▼
 TCP Connection
      │
      │ ssl.wrap_socket()
      ▼
 TLS Handshake
      │
      ├── ClientHello
      ├── ServerHello
      ├── Certificate
      ├── Certificate Verification
      ├── Key Exchange
      └── Traffic Keys
      │
      ▼
 Secure TLS Connection
      │
      │ HTTP Request
      ▼
 TLS Encryption
      │
      ▼
 TCP
      │
      ▼
 IP
      │
      ▼
 Network
      │
      ▼
 Server
      │
      ▼
 HTTP Response
      │
      ▼
 TLS
      │
      ▼
 TCP
      │
      ▼
 Python Program
```

**Key Point**

Python exposes the APIs, but the operating system performs the underlying TCP/IP networking. TLS protects the HTTP data before TCP transports it.