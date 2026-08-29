# Diagram 101 - QUIC Multiple Sending Constraints

```text
                 Sender
                    |
          +---------+---------+
          |                   |
          v                   v
   Receiver capacity     Network capacity
          |                   |
          v                   v
    Flow control         Congestion control
          |                   |
          +---------+---------+
                    |
                    v
              Actual sending
```
