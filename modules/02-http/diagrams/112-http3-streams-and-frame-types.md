# Diagram 112 - HTTP/3 Streams and Frame Types

```text
                         QUIC CONNECTION
                                |
        +-----------------------+-----------------------+
        |                       |                       |
        v                       v                       v
 Request Stream           Request Stream          Control Stream
        |                       |                       |
        v                       v                       v
    HEADERS                  HEADERS               SETTINGS
        |                       |
        v                       v
      DATA                    DATA
        |
        +-------------------+
                            |
                            v
                      QUIC STREAM frame
                            |
                            v
                       QUIC packet
                            |
                            v
                           UDP
```

Key distinction:

```text
HTTP/3 DATA / HEADERS
          |
          | application-level meaning
          v
      HTTP/3 frame
          |
          | bytes carried by
          v
      QUIC STREAM frame
          |
          | transport-level meaning
          v
      QUIC packet
```
