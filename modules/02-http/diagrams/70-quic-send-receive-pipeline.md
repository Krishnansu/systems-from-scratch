# Diagram 37-06 - QUIC Packet Protection Send/Receive Pipeline

## Sender

```text
HTTP/3
  |
  v
STREAM frame
  |
  v
QUIC payload
  |
  v
AEAD encryption
  |
  v
Ciphertext + Tag
  |
  v
Header protection
  |
  v
Protected QUIC packet
  |
  v
UDP
```

## Receiver

```text
UDP
  |
  v
QUIC packet
  |
  v
Locate ciphertext sample
  |
  v
Remove header protection
  |
  v
Recover packet number
  |
  v
Construct AEAD nonce
  |
  v
Authenticate + decrypt
  |
  v
QUIC frames
  |
  v
HTTP/3
```
