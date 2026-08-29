# Diagram 37-02 - QUIC Packet-Protection Key Material

```text
TLS 1.3 Traffic Secret
          |
          v
   QUIC key derivation
          |
     +----+----+
     |    |    |
     v    v    v
    Key   IV  HP Key
     |    |    |
     |    |    +----> Header protection
     |    |
     |    +---------> Nonce construction
     |
     +--------------> AEAD payload protection
```
