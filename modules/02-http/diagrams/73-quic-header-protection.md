# Diagram 73 - QUIC Header Protection

```text
QUIC Header
    |
    +-------------------------+
    |                         |
    v                         v
First-byte bits        Packet-number bytes
    |                         |
    +------------+------------+
                 |
                 v
         Header protection
                 ^
                 |
       Header Protection Key
                 +
       Ciphertext Sample
```
