# Diagram 36-05 - QUIC Packet Number Spaces

```text
                 QUIC Connection
                        |
        +---------------+---------------+
        |               |               |
     Initial        Handshake      Application
      Space           Space          Data Space
        |               |               |
   Initial packets  Handshake       1-RTT packets
                    packets
```

Packet numbers are scoped to their packet number space. A packet number in one space is not the same packet number as the same numeric value in another space.
