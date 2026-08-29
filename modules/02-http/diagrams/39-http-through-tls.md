# HTTP Through TLS

```text
HTTP Request

GET / HTTP/1.1
Host: example.com
        │
        ▼
+-------------------+
|       TLS         |
|     Encrypt       |
+-------------------+
        │
        ▼
Encrypted TLS Records
        │
        ▼
+-------------------+
|       TCP         |
|  Ordered Bytes    |
+-------------------+
        │
        ▼
+-------------------+
|        IP         |
| Routing / Address |
+-------------------+
        │
        ▼
     Network
```

**Key Point**

TCP does not understand HTTP. TLS protects the HTTP bytes, and TCP transports the resulting encrypted byte stream.