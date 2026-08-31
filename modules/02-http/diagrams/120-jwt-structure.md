# Diagram 120 — JWT Structure

```text
                    JSON WEB TOKEN

        +----------------+----------------+----------------+
        |     HEADER     |    PAYLOAD     |   SIGNATURE    |
        +----------------+----------------+----------------+
                |                |                |
                v                v                v
          Algorithm        Claims / data     Cryptographic
          Token type       sub = 42          proof
                           role = user
                           exp = ...

        HEADER.PAYLOAD.SIGNATURE

        Header + Payload
              |
              v
        Signing algorithm
              |
              v
          Signature

IMPORTANT:
Header and payload are normally encoded, NOT encrypted.
The signature protects integrity/authenticity.
```
