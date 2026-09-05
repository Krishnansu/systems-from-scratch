# Diagram 130 — WebSocket Bidirectional Communication

```text
              Persistent WebSocket

Client <================================> Server
   |                                      |
   | text / binary                        |
   |------------------------------------->|
   |                                      |
   |<-------------------------------------|
   |              event                   |
   |                                      |
   |<-------------------------------------|
   |             notification             |
   |                                      |
   |------------------------------------->|
   |              message                 |
```
