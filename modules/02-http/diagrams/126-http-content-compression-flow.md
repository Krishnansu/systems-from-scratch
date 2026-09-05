# Diagram 126 — HTTP Content Compression Flow

```text
Client
  |
  | Accept-Encoding: gzip, br
  v
Server
  |
  | generate response body
  v
Compressible?
  |          \
 No           Yes
  |             |
  |        gzip / Brotli
  |             |
  +------->----+
             |
             | Content-Encoding
             v
          Network
             |
             v
           Client
             |
             v
        Decompression
             |
             v
        Original body
```
