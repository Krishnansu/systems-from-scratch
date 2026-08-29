# Diagram 35-03 - QUIC Streams and Packets

```text
                    QUIC Connection
                          |
              +-----------+-----------+
              |           |           |
          Stream 4     Stream 8    Stream 12
              |           |           |
              +-----------+-----------+
                          |
                     QUIC Packets
                          |
              +-----------+-----------+
              |           |           |
           Packet 1    Packet 2    Packet 3
              |           |           |
          STREAM 4    STREAM 8    STREAM 4
                      + STREAM 12
```

A packet is a container. Streams are logical byte sequences.

One packet can carry data for multiple streams.
