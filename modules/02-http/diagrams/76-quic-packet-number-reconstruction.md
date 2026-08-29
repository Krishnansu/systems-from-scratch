# Diagram 76 - QUIC Packet Number Reconstruction

```text
Largest previously received PN
              |
              v
      Truncated PN received
              |
              v
     Candidate full numbers
              |
              v
   Packet-number reconstruction
              |
              v
      Full packet number
```

The receiver uses packet-number state and the encoded packet-number length to select the appropriate full value.
