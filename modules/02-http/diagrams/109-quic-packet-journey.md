# Diagram 109 - QUIC Packet Journey

```text
Application data
       |
       v
     Stream
       |
       v
   QUIC frames
       |
       v
   QUIC packet
       |
       +--> Packet number
       |
       +--> Connection ID
       |
       +--> Header protection
       |
       +--> AEAD encryption
       |
       v
      UDP
       |
       v
      IP
       |
       v
    Network
```
