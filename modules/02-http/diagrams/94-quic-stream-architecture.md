# Diagram 94 - QUIC Stream Architecture

```text
                    QUIC Connection
                           |
             +-------------+-------------+
             |             |             |
             v             v             v
         Stream 4       Stream 8      Stream 12
             |             |             |
             v             v             v
          ordered       ordered       ordered
           bytes         bytes         bytes
             \             |             /
              \            |            /
               +-----------+-----------+
                           |
                           v
                      QUIC Packets
                           |
                           v
                          UDP
```
