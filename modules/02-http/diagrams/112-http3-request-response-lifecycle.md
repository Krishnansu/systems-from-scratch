# Diagram 112 — HTTP/3 Request/Response Lifecycle

```text
                         BROWSER
                            |
                            v
                           DNS
                            |
                            v
                    Server IP / HTTP/3
                            |
                            v
                    QUIC Connection
                            |
             +--------------+--------------+
             |              |              |
             v              v              v
         Control        QPACK streams   Request
          Stream                           Stream
             |                              |
          SETTINGS                        HEADERS
                                            |
                                            v
                                      QPACK encode
                                            |
                                            v
                                      QUIC STREAM
                                            |
                                            v
                                      QUIC packet
                                            |
                                            v
                                           UDP
                                            |
                                            v
                                         Network
                                            |
                                            v
                                          Server
                                            |
                                            v
                                      QUIC processing
                                            |
                                            v
                                      HTTP/3 HEADERS
                                            |
                                            v
                                        QPACK decode
                                            |
                                            v
                                      HTTP request
                                            |
                                            v
                                        Application
                                            |
                                            v
                                      HTTP response
                                            |
                                     +------+------+
                                     |             |
                                     v             v
                                  HEADERS        DATA
                                     |             |
                                     +------+------+
                                            |
                                            v
                                      QUIC Stream
                                            |
                                            v
                                      QUIC packets
                                            |
                                            v
                                           UDP
                                            |
                                            v
                                          Client
                                            |
                                            v
                                         Browser
```

## Layering Boundary

```text
HTTP/3 HEADERS / DATA
          |
          v
      Stream bytes
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

The important distinction is that HTTP/3 defines the meaning of its frames, while QUIC transports the resulting bytes and provides the transport guarantees.
