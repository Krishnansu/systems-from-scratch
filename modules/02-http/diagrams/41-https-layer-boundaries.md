# HTTPS Layer Boundaries

```text
+-----------------------------+
| HTTP                        |
| Requests, responses,        |
| methods, headers, status    |
+-----------------------------+
              │
              ▼
+-----------------------------+
| TLS                         |
| Encryption, authentication, |
| integrity                   |
+-----------------------------+
              │
              ▼
+-----------------------------+
| TCP                         |
| Reliable ordered byte       |
| stream                      |
+-----------------------------+
              │
              ▼
+-----------------------------+
| IP                          |
| Addressing and routing      |
+-----------------------------+
              │
              ▼
+-----------------------------+
| Network / Link              |
| Local transmission          |
+-----------------------------+
```

**Key Point**

HTTPS is HTTP carried through TLS, with TLS carried over the transport connection.