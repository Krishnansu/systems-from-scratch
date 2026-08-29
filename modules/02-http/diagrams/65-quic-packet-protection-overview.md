# Diagram 37-01 - QUIC Packet Protection Overview

```text
QUIC Packet
    |
    +-------------------------+
    |                         |
    v                         v
Payload protection       Header protection
    |                         |
    v                         v
   AEAD                 Masks selected bits
    |                         |
    v                         v
Ciphertext + Tag        Protected header
```

Payload protection and header protection are distinct cryptographic operations.
