# Lesson 56 — Compression

## Objectives

- Understand why compression exists and what problem it solves.
- Understand the CPU-versus-bandwidth trade-off.
- Distinguish request-body compression from response-body compression.
- Understand `Accept-Encoding` and `Content-Encoding`.
- Understand gzip and Brotli at a practical level.
- Understand compression with caching and `Vary: Accept-Encoding`.
- Distinguish HTTP body compression from HTTP/2 HPACK and HTTP/3 QPACK header compression.

## Concept Summary

Compression reduces the number of bytes transferred by exploiting redundancy in data. It trades computation for lower network transfer cost.

```text
Original data
     |
     | compression
     v
Smaller representation
     |
     | network
     v
     Client
     |
     | decompression
     v
Original data
```

The overall trade-off is:

```text
More compression
      |
      +--> more CPU work
      |
      +--> fewer network bytes
```

Compression is most useful for data with redundancy, such as JSON, HTML, CSS, JavaScript, XML, and text. Already-compressed formats such as JPEG, PNG, WebP, AVIF, MP4, and ZIP generally provide little additional benefit.

## Core Ideas

### 1. Request and Response Compression

Compression is not limited to responses. Both HTTP request and response bodies can have a content encoding.

Typical web traffic compresses responses more often because requests are frequently small while API responses can be large.

```text
Request:
Client -- compressed body --> Server -- decompress --> application

Response:
Server -- compress --> Client -- decompress --> application
```

For a request:

```http
Content-Encoding: gzip
```

means the request body is gzip-compressed.

For a response:

```http
Content-Encoding: br
```

means the response body uses Brotli.

### 2. Accept-Encoding

`Accept-Encoding` is sent by a client to advertise supported content encodings.

```http
Accept-Encoding: gzip, br
```

Conceptually:

> What encodings can I receive?

### 3. Content-Encoding

`Content-Encoding` identifies the encoding applied to the message body.

```http
Content-Encoding: br
```

Conceptually:

> What encoding is this body using?

These headers should not be confused:

```text
Accept-Encoding
      |
      +--> client capability

Content-Encoding
      |
      +--> actual body encoding
```

### 4. Why Compression Works

Compression exploits redundancy. Repeated characters, strings, structures, and patterns can often be represented more efficiently.

JSON is particularly suitable because field names, delimiters, and values often repeat across large responses.

### 5. Compression and Encryption

Compression generally happens before encryption because encrypted data is intentionally made to appear random and therefore usually has little exploitable redundancy.

```text
Application data
      |
      v
Compression
      |
      v
Encryption
      |
      v
Network
```

### 6. gzip and Brotli

`gzip` is a widely supported general-purpose HTTP compression format.

Brotli (`br`) is designed with web content in mind and often provides better compression than gzip for text-based web assets, depending on compression level and workload.

Neither algorithm is universally optimal. Compression level determines the CPU-versus-size trade-off.

### 7. Compression Level

Higher compression levels generally require more CPU and can produce smaller output.

```text
Lower level
  -> faster compression
  -> larger output

Higher level
  -> slower compression
  -> smaller output
```

For dynamic responses, excessive compression can waste application CPU. Static assets can often be compressed ahead of time during a build or deployment.

### 8. Static vs Dynamic Content

Dynamic response:

```text
Request
  -> application generates response
  -> compress
  -> send
```

Static asset:

```text
Build time
  -> compress asset
  -> store compressed representation
  -> serve
```

Pre-compressing static assets avoids repeating expensive compression work for every request.

### 9. Request Compression

Large request bodies can also benefit from compression.

Example:

```http
POST /bulk-import
Content-Type: application/json
Content-Encoding: gzip
```

The server receives the compressed body and decompresses it before parsing the JSON.

This is useful for large JSON/XML payloads, bulk ingestion, analytics uploads, and service-to-service traffic.

For a tiny request body, compression overhead may outweigh the network savings.

### 10. Caching and Vary

Different clients can support different encodings.

```text
Client A -> Accept-Encoding: br, gzip
Client B -> Accept-Encoding: gzip
Client C -> no compression
```

The server may therefore produce different representations of the same logical resource.

When a response varies according to `Accept-Encoding`, caches need to account for that variation:

```http
Vary: Accept-Encoding
```

Conceptually:

```text
/app.js + br
/app.js + gzip
/app.js + identity
```

are different wire representations of the same logical resource.

### 11. Do Not Compress Everything

Compression is not automatically beneficial.

Avoid unnecessary compression when:

- the response is very small;
- the content is already compressed;
- CPU is more constrained than bandwidth;
- compression latency outweighs network savings.

Common already-compressed formats include JPEG, PNG, WebP, AVIF, MP4, and ZIP.

### 12. Body Compression vs Header Compression

HTTP body compression is separate from HTTP header compression.

```text
HTTP body compression
  -> gzip / Brotli

HTTP header compression
  -> HPACK in HTTP/2
  -> QPACK in HTTP/3
```

HPACK and QPACK solve the problem of reducing repetitive HTTP header overhead; they are not replacements for gzip or Brotli body compression.

## Practical Example

Suppose an API generates a 10 MB JSON response.

Without compression:

```text
Application
    |
    | 10 MB
    v
 Network
    |
    v
 Client
```

With compression:

```text
Application
    |
    | 10 MB JSON
    v
Compression
    |
    | 1 MB
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
10 MB logical response
```

The client ultimately receives the same logical data, but only 1 MB crosses the network.

The benefit must be evaluated against the CPU cost of compression and decompression.

## Production Perspective

A production compression policy should consider:

1. Is the content compressible?
2. Is it large enough to justify compression?
3. Does the client support the chosen encoding?
4. Is gzip or Brotli more appropriate?
5. What compression level is appropriate?
6. Is CPU or bandwidth the primary bottleneck?
7. Is the response cached?
8. Can compressed static representations be generated ahead of time?
9. Is the content already compressed?
10. Does caching correctly vary representations by `Accept-Encoding`?

A common production pattern is to compress text-based responses and static assets while avoiding unnecessary compression of already-compressed media.

## Common Mistakes

- Assuming only responses can be compressed.
- Confusing `Accept-Encoding` with `Content-Encoding`.
- Thinking compression always reduces total latency without considering CPU cost.
- Compressing already-compressed media.
- Confusing body compression with HPACK/QPACK.
- Forgetting that a cache may need separate representations for different encodings.
- Assuming the highest compression level is always best.

## Key Takeaways

- Compression reduces network bytes by exploiting redundancy.
- It trades CPU for bandwidth and potentially lower transfer latency.
- Both request and response bodies can be compressed.
- `Accept-Encoding` advertises supported encodings.
- `Content-Encoding` identifies the encoding actually applied to the body.
- gzip and Brotli are common HTTP body compression formats.
- Static assets can often be pre-compressed.
- `Vary: Accept-Encoding` matters when cached representations differ by encoding.
- Already-compressed content usually should not be compressed again.
- HPACK and QPACK are header-compression mechanisms, separate from body compression.

## Reflection Questions

1. Why are HTTP responses generally compressed more often than requests?
2. What is the difference between `Accept-Encoding` and `Content-Encoding`?
3. Why does compression usually happen before encryption?
4. Why can aggressive compression reduce bandwidth while increasing server CPU usage?
5. Why can a cache not blindly serve a Brotli representation to every client?
6. Why is compressing a JPEG usually not useful?
7. What is the difference between Brotli body compression and QPACK header compression?

## Related Lessons

- Lesson 45 — QPACK: HTTP/3 Header Compression
- Lesson 50 — HTTP/3 Performance & Trade-offs
- Lesson 55 — Caching

## What’s Next

**Lesson 57 — WebSockets**

Move from HTTP request/response communication to persistent, bidirectional communication between clients and servers.
