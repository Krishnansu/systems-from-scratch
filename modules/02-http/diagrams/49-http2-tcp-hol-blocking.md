# HTTP/2 Still Has TCP Head-of-Line Blocking

```text
HTTP/2 Streams

Stream A → A1 A2 A3 A4
Stream B → B1 B2 B3 B4
Stream C → C1 C2 C3 C4
        |
        v
       TCP
        |
        v
One ordered byte stream
```

If a TCP segment is lost:

```text
A1 A2 [missing] A4 B1 B2 B3 C1 C2 ...
          |
          v
     Retransmission
```

TCP does not understand that the bytes belong to different HTTP/2 streams. Its ordered byte-stream semantics remain in effect.

**Key Point**

HTTP/2 multiplexes at the HTTP layer, but TCP remains a single ordered byte stream.