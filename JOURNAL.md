# Journal

## Lesson 46 — HTTP/3 Request/Response Lifecycle

Completed an end-to-end walkthrough of an HTTP/3 request and response. Traced the journey from DNS and HTTP/3 discovery through QUIC connection establishment, the HTTP/3 control stream and SETTINGS, QPACK header compression, request-stream creation, HTTP/3 HEADERS/DATA frames, QUIC STREAM frames, QUIC packets, UDP, and the reverse path at the server. Consolidated the separation of responsibilities between HTTP/3, QPACK, QUIC, UDP, and IP. Also connected packet loss, flow control, congestion control, and QPACK dependencies to the complete lifecycle. This lesson establishes the complete mental model for how an HTTP/3 request actually travels through the stack.
