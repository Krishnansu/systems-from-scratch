# Diagram 113 — HTTP/3 Priority vs QUIC Flow Control

```text
                 Available HTTP work
                         |
                         v
                    PRIORITY
                         |
              What should go first?
                         |
              +----------+----------+
              |          |          |
             HIGH      MEDIUM       LOW
              |          |          |
              +----------+----------+
                         |
                         v
                       QUIC
                         |
                  FLOW CONTROL
                         |
                How much may I send?
                         |
                         v
                  CONGESTION CONTROL
                         |
              How much can the network
                   currently handle?
                         |
                         v
                      Network
```

Priority is scheduling intent. Flow control and congestion control constrain actual transmission.
