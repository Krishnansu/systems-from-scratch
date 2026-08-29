# Inspecting TLS with Python

```text
TLS Socket
    │
    ├── version()
    │      └── Negotiated TLS version
    │
    ├── cipher()
    │      └── Negotiated cipher information
    │
    └── getpeercert()
           ├── Subject
           ├── Issuer
           ├── Validity
           └── Subject Alternative Names
```

**Key Point**

Python's `ssl` module exposes useful information about the TLS session after the handshake has completed.