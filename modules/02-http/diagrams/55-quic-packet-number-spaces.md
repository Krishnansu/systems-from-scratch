# Diagram 35-05 - QUIC Packet Number Spaces

```text
                 QUIC Connection
                        |
        +---------------+---------------+
        |               |               |
     Initial        Handshake      Application
      Space           Space          Data Space
        |               |               |
   Initial packets  Handshake      1-RTT packets
                    packets
```

Each packet number space has separate packet-number and acknowledgment/loss-recovery treatment.
