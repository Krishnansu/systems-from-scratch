# Diagram 108 - Complete QUIC Architecture

```text
                         QUIC
                           |
        +------------------+------------------+
        |                  |                  |
        v                  v                  v
   Connection          Security           Reliability
        |                  |                  |
        v                  v                  v
 Connection IDs       TLS 1.3             ACKs
 Migration            AEAD                Loss detection
 Path validation      Header protection   RTT
        |
        v
     Streams
        |
        v
   Multiplexing
        |
        v
   Flow Control
        |
        +------------------+
                           |
                           v
                  Congestion Control
                           |
                           v
                          UDP
```
