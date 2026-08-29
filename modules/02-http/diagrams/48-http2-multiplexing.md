# HTTP/2 Multiplexing

```text
Stream 1 → HTML
Stream 3 → CSS
Stream 5 → JavaScript

Frames can be interleaved:

HEADERS(S1)
HEADERS(S3)
HEADERS(S5)
DATA(S1)
DATA(S3)
DATA(S5)
DATA(S1)
DATA(S5)
```

Conceptually:

```text
Without multiplexing:
AAAA BBBB CCCC

With multiplexing:
A1 B1 C1 A2 B2 C2 A3 B3 C3
```

**Key Point**

HTTP/2 allows multiple logical streams to make progress over one TCP connection.