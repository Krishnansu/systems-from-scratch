# Diagram 79 - QUIC Receiver Protection Flow

```text
Protected QUIC Packet
          |
          v
Locate ciphertext sample
          |
          v
Generate header-protection mask
          |
          v
Remove header protection
          |
          v
Recover packet number
          |
          v
Construct AEAD nonce
          |
          v
Authenticate + decrypt
          |
          v
QUIC frames
```
