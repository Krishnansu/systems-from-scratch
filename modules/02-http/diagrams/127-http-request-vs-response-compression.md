# Diagram 127 — HTTP Request vs Response Compression

```text
REQUEST

Client
  |
  | large request body
  v
Compress
  |
  | Content-Encoding: gzip
  v
Server
  |
  v
Decompress
  |
  v
Application


RESPONSE

Application
  |
  v
Compress
  |
  | Content-Encoding: br
  v
Client
  |
  v
Decompress
  |
  v
Application data
```
