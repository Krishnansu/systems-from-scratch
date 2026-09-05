# Diagram 128 — HTTP Compression and Caching

```text
Client
  |
  | Accept-Encoding: br, gzip
  v
Cache / Server
  |
  +--> /app.js + br
  |
  +--> /app.js + gzip
  |
  +--> /app.js + identity
  |
  v
Vary: Accept-Encoding
```

The logical resource can have multiple wire representations depending on the client's supported content encodings.
