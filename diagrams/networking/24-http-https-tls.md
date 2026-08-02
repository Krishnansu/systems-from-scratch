# HTTP vs HTTPS and TLS

## HTTP

```text
HTTP
 │
 ▼
TCP
 │
 ▼
IP
 │
 ▼
Network
```

## HTTPS

```text
HTTPS
 │
 ▼
HTTP
 │
 ▼
TLS
 │
 ▼
TCP
 │
 ▼
IP
 │
 ▼
Network
```

### TLS Provides

```text
TLS
 │
 ├── Encryption
 ├── Authentication
 └── Integrity
```

**Key Points**
- HTTPS is HTTP secured using TLS.
- TLS encrypts application data so it cannot be easily read by network observers.
- TLS authenticates the server using certificates and public-key cryptography.
- TLS protects the integrity of data exchanged between client and server.
- TLS will be studied in detail in a dedicated future lesson.