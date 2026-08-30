# Diagram 114 — HTTP/3 ↔ QUIC Layer Boundary

```text
                    APPLICATION
                         |
                         v
                       HTTP/3
                         |
        +----------------+----------------+
        |                |                |
     HEADERS            DATA          SETTINGS
        |                |                |
        +----------------+----------------+
                         |
                    HTTP/3 bytes
                         |
                         v
                        QUIC
                         |
        +----------------+----------------+
        |                |                |
     STREAM            ACK         FLOW CONTROL
        |                                |
        +----------------+----------------+
                         |
                         v
                   QUIC packet
                         |
                         v
                        UDP
                         |
                         v
                         IP
                         |
                         v
                      NETWORK
```

HTTP/3 defines what the bytes mean. QUIC defines how they are transported.
