# Diagram 37-07 - QUIC Packet Number Truncation and Reconstruction

```text
Sender

Full Packet Number
0x0000001234
       |
       v
Transmit selected low-order bytes
       |
       v
Truncated PN
0x34
```

Receiver:

```text
Largest previously received PN
          |
          v
Truncated PN received
          |
          v
Candidate full packet numbers
          |
          v
Select valid closest value
          |
          v
Reconstructed full PN
```

QUIC reduces packet overhead by transmitting only the required packet-number bytes.
