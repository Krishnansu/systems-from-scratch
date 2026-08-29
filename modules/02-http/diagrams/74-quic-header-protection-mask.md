# Diagram 74 - QUIC Header-Protection Mask Generation

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
       +------------------+
       |                  |
       v                  v
First-byte bits     Packet-number bytes
```
