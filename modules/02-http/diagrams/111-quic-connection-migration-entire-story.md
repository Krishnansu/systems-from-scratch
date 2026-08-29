# Diagram 111 - QUIC Connection Migration: Entire Story

```text
                         SAME QUIC CONNECTION
                              CID = ABC123
                                   |
              +--------------------+--------------------+
              |                                         |
              v                                         v
          OLD PATH                                  NEW PATH
              |                                         |
       192.168.1.20                               10.20.30.40
              |                                         |
            Wi-Fi                                     Mobile
              |                                         |
              +--------------------+--------------------+
                                   |
                                   v
                                 Server


Migration sequence:

Client                         Server
  |                               |
  | Packet #500                   |
  | CID = ABC123                  |
  |------------------------------>|
  |                               |
  |   Wi-Fi disappears            |
  |                               |
  | Packet #501                   |
  | CID = ABC123                  |
  |==============================>|
  |                               |
  |                  PATH_CHALLENGE
  |<------------------------------|
  |                               |
  | PATH_RESPONSE                 |
  |------------------------------>|
  |                               |
  |        NEW PATH VALIDATED     |
  |                               |
  | Packet #502                   |
  | CID = ABC123                  |
  |==============================>|
```

## Key Idea

The logical QUIC connection remains the same (`CID = ABC123`) while packets move from the old network path to the new path. The new path is validated using `PATH_CHALLENGE` and `PATH_RESPONSE` before it is trusted.
