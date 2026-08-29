# HTTP/2 Streams and Frames

```text
                 One TCP Connection
                         |
                         v
                       HTTP/2
                         |
          +--------------+--------------+
          |              |              |
          v              v              v
      Stream 1        Stream 3        Stream 5
          |              |              |
       Frames         Frames         Frames
          |              |              |
       HEADERS         HEADERS         HEADERS
          |              |              |
        DATA           DATA           DATA
```

A stream is a logical HTTP/2 communication channel. Frames are the units carried within that stream.

**Key Point**

One TCP connection can contain many HTTP/2 streams.