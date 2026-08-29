# Routing - Packet Journey Across Networks

```text
                    Internet
                        |
                  +-------------+
                  | ISP Router  |
                  +-------------+
                        |
                  +-------------+
                  | Home Router |
                  |192.168.1.1  |
                  +-------------+
                        |
                 +---------------+
                 | Home Switch   |
                 +---------------+
                  /             \
                 /               \
        Laptop                Phone
    192.168.1.10         192.168.1.20

Destination: 8.8.8.8

Laptop
    │
    │  Dest MAC = Router
    │  Dest IP  = 8.8.8.8
    ▼
Home Router
    │
    │ Removes Ethernet Header
    │ Looks at Routing Table
    │ Creates NEW Ethernet Frame
    ▼
ISP Router
    ▼
Internet
```

**Key Points**
- Router forwards packets between different networks.
- Ethernet (MAC) headers are rewritten at every hop.
- IP addresses remain unchanged throughout the journey.
- The default gateway is the first router a host sends packets to.