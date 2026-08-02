# UDP Packet Structure

```text
  0                   15 16                  31
  ┌─────────────────────┬─────────────────────┐
  │    Source Port      │  Destination Port   │
  ├─────────────────────┼─────────────────────┤
  │       Length        │       Checksum      │
  ├─────────────────────┴─────────────────────┤
  │                                             │
  │                    Data                     │
  │                                             │
  └─────────────────────────────────────────────┘

                 UDP Header = 8 Bytes
```

**Key Points**
- Source Port identifies the sending application.
- Destination Port identifies the receiving application.
- Length contains the size of the UDP header and data.
- Checksum detects corruption in the datagram.
- The UDP header is only 8 bytes.