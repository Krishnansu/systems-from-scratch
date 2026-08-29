# Diagram 93 - HTTP/2 vs HTTP/3 Head-of-Line Blocking

```text
HTTP/2
  |
  v
Multiple HTTP streams
  |
  v
TCP ordered byte stream
  |
  v
Connection-level HOL blocking


HTTP/3
   |
   v
QUIC streams
   |
   v
QUIC packets
   |
   v
UDP
```
