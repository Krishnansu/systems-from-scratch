# Diagram 78 - Header Protection vs Payload Protection

```text
                 QUIC Packet
                      |
            +---------+---------+
            |                   |
            v                   v
          Header             Payload
            |                   |
            v                   v
   Header Protection           AEAD
            |                   |
            v                   v
  Selected bits masked   Encrypted + authenticated
```
