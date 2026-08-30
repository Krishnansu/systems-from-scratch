# Diagram 113 — HTTP/3 Error and Shutdown Scope

```text
                       HTTP/3 / QUIC CONNECTION
                                  |
                +-----------------+-----------------+
                |                                   |
                v                                   v
          STREAM-LEVEL                         CONNECTION-LEVEL
                |                                   |
       +--------+--------+                    +-----+------+
       |                 |                    |            |
       v                 v                    v            v
 RESET_STREAM      STOP_SENDING           GOAWAY    CONNECTION_CLOSE
       |                 |                    |            |
       v                 v                    v            v
Terminate/reset     Stop receiving      Graceful HTTP   Terminate
one stream          stream data         shutdown        QUIC connection
```

HTTP/3 error codes (`H3_*`) describe the HTTP/3-level reason for a protocol or operation failure, while QUIC provides the underlying stream and connection control mechanisms.
