# Diagram 123 — JWT Signing & Distributed Verification

```text
                 ASYMMETRIC JWT SIGNING

                 Authentication Server
                         |
                         | Private Key
                         v
                       SIGN
                         |
                         v
                        JWT
                         |
              +----------+----------+
              |          |          |
              v          v          v
          Service A   Service B   Service C
              |          |          |
              |          |          |
          Public Key  Public Key  Public Key
              |          |          |
              v          v          v
           VERIFY      VERIFY      VERIFY


SYMMETRIC SIGNING

             Shared Secret
                /      \
               /        \
            SIGN        VERIFY
               \        /
                \      /
                  JWT


ASYMMETRIC MODEL:

Private key → kept by issuer
Public key  → distributed to verifiers

This is useful when many services need to verify tokens without
being given the ability to issue new ones.
```
