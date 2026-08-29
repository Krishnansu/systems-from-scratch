# Diagram 98 - QUIC Flow-Control Window Growth

```text
Receiver                         Sender
   |                               |
   | MAX_STREAM_DATA = 100 KB      |
   |------------------------------>|
   |                               |
   |       data arrives            |
   |<------------------------------|
   |                               |
   | consume data                  |
   |                               |
   | MAX_STREAM_DATA = 200 KB      |
   |------------------------------>|
```
