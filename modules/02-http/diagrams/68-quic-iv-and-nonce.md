# Diagram 37-04 - QUIC IV and AEAD Nonce

```text
        IV
         +
 Packet Number
         |
         v
       XOR
         |
         v
      Nonce
         |
         v
        AEAD
```

The IV is the base cryptographic value. The packet number makes the nonce packet-specific.
