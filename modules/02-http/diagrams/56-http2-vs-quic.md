# Diagram 35-06 - HTTP/2 vs QUIC

## HTTP/2 over TCP

```text
HTTP/2
  |
  +-- Stream 1
  +-- Stream 3
  +-- Stream 5
          |
          v
         TCP
          |
          v
   One ordered byte stream
```

## HTTP/3 over QUIC

```text
HTTP/3
   |
   v
  QUIC
   |
   +-- Stream 1
   +-- Stream 3
   +-- Stream 5
   |
   v
  UDP
```

The architectural difference is that QUIC itself understands independent streams.
