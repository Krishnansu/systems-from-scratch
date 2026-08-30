# Diagram 113 — HTTP/3 Frame Inside a QUIC Stream

```text
QUIC Stream 7

+--------------------------------------------------+
| HTTP/3 HEADERS frame                             |
|                                                  |
| +----------------------------------------------+ |
| | QPACK-compressed header block                | |
| |                                              | |
| | :method = GET                                | |
| | :scheme = https                              | |
| | :authority = example.com                      | |
| | :path = /index.html                           | |
| +----------------------------------------------+ |
+--------------------------------------------------+

                    ↓

QUIC STREAM frame
  Stream ID = 7
  Offset    = 0
  Data      = bytes above
```

The HTTP/3 frame is not itself a QUIC frame. It is application-layer data carried by a QUIC `STREAM` frame.
