# TCP vs UDP

```text
                         Application
                              │
                ┌─────────────┴─────────────┐
                │                           │
               TCP                         UDP
                │                           │
       Reliable Byte Stream         Independent Datagrams
                │                           │
       Ordered Delivery             No Ordering Guarantee
                │                           │
       Retransmissions              No Retransmissions
                │                           │
       Flow Control                 Minimal Overhead
                │                           │
       Congestion Control            Application Decides
                │                           │
                └─────────────┬─────────────┘
                              │
                             IP
                              │
                           Network
```

**Key Points**
- TCP provides a reliable, ordered byte stream.
- UDP provides independent datagrams with minimal built-in guarantees.
- TCP handles retransmission, ordering, flow control, and congestion control.
- UDP leaves reliability and additional guarantees to the application or higher-level protocol.