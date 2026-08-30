# Journal

## Lesson 46 — HTTP/3 Request/Response Lifecycle

Completed an end-to-end walkthrough of an HTTP/3 request and response. Traced the journey from DNS and HTTP/3 discovery through QUIC connection establishment, the HTTP/3 control stream and SETTINGS, QPACK header compression, request-stream creation, HTTP/3 HEADERS/DATA frames, QUIC STREAM frames, QUIC packets, UDP, and the reverse path at the server. Consolidated the separation of responsibilities between HTTP/3, QPACK, QUIC, UDP, and IP. Also connected packet loss, flow control, congestion control, and QPACK dependencies to the complete lifecycle. This lesson establishes the complete mental model for how an HTTP/3 request actually travels through the stack.

## Lesson 47 — HTTP/3 Error Handling & Connection Shutdown

Studied HTTP/3 and QUIC error handling at both stream and connection scope. Clarified that `RESET_STREAM`, `STOP_SENDING`, and `CONNECTION_CLOSE` are QUIC transport mechanisms and are not part of the HTTP/3 `SETTINGS` frame. Distinguished HTTP status codes such as 2xx/4xx/5xx from `H3_*` HTTP/3 protocol error codes. Covered `GOAWAY` as an HTTP/3 graceful-shutdown mechanism and compared it with QUIC `CONNECTION_CLOSE`. Also compared HTTP/2's `RST_STREAM` and `GOAWAY` with the corresponding HTTP/3/QUIC architecture, reinforcing the key distinction that QUIC understands streams as transport primitives while TCP provides a single byte stream.
