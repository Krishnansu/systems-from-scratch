# Diagram 37-05 - QUIC Header Protection

```text
Ciphertext Sample
       +
Header Protection Key
       |
       v
Mask Generation
       |
       v
      Mask
       |
       +-------------------+
       |                   |
       v                   v
First-byte bits      Packet-number bytes
       |                   |
       v                   v
Protected header     Protected PN
```

Header protection masks selected header bits. It is separate from AEAD payload encryption.
