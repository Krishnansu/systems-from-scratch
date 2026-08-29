# Diagram 35-07 - HTTP/3 to QUIC to UDP

```text
+---------------------------+
| HTTP/3                    |
+---------------------------+
            |
            v
+---------------------------+
| QUIC                      |
|                           |
|  Streams                  |
|  Packets                  |
|  Frames                   |
|  Reliability              |
|  Flow control             |
|  Congestion control       |
|  Connection management    |
|  TLS integration          |
+---------------------------+
            |
            v
+---------------------------+
| UDP                       |
+---------------------------+
            |
            v
+---------------------------+
| IP                        |
+---------------------------+
```

Receiving direction:

```text
IP packet
    |
    v
UDP datagram
    |
    v
QUIC packet
    |
    +-- Header
    +-- Frames
           |
           v
    Stream reassembly
           |
           v
        HTTP/3
```
