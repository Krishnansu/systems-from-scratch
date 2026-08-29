# TLS 1.3 Key Schedule

```text
       ECDHE Shared Secret
                |
                v
               HKDF
                |
                v
         TLS Key Schedule
                |
       +--------+--------+
       |                 |
       v                 v
Client Traffic       Server Traffic
    Secrets               Secrets
       |                 |
       v                 v
Client Write Key    Server Write Key
```

**Key Points**
- TLS 1.3 derives multiple secrets instead of directly using the ECDHE shared secret as a single application key.
- HKDF is used as the key derivation mechanism.
- Separate traffic secrets support key separation between directions and stages of the handshake.