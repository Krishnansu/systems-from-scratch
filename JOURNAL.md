# Journal

## Lesson 44 — HTTP/3 Streams & Frame Types

Covered the HTTP/3 stream model and how HTTP/3 maps onto QUIC. Learned the distinction between bidirectional request streams and unidirectional streams used for connection control and QPACK. Studied HTTP/3 frame types including HEADERS, DATA, SETTINGS, and GOAWAY. A key distinction was established between HTTP/3 frames and QUIC STREAM frames: HTTP/3 frames carry HTTP-level meaning, while QUIC STREAM frames carry bytes belonging to a QUIC stream.

## Lesson 45 — QPACK: HTTP/3 Header Compression

Covered QPACK and why HTTP/3 uses it instead of HPACK. Learned about the predefined static table, mutable connection-specific dynamic table, and dedicated QPACK encoder/decoder streams. Clarified that the static table is never dynamically updated during a connection; it is fixed by the QPACK specification. Dynamic-table entries can create dependencies that temporarily block an individual request stream, but this is distinct from TCP's transport-level head-of-line blocking.
