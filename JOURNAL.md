# Journal

## Lesson 46 — HTTP/3 Request/Response Lifecycle

Completed an end-to-end walkthrough of an HTTP/3 request and response. Traced the journey from DNS and HTTP/3 discovery through QUIC connection establishment, the HTTP/3 control stream and SETTINGS, QPACK header compression, request-stream creation, HTTP/3 HEADERS/DATA frames, QUIC STREAM frames, QUIC packets, UDP, and the reverse path at the server. Consolidated the separation of responsibilities between HTTP/3, QPACK, QUIC, UDP, and IP. Also connected packet loss, flow control, congestion control, and QPACK dependencies to the complete lifecycle. This lesson establishes the complete mental model for how an HTTP/3 request actually travels through the stack.

## Lesson 47 — HTTP/3 Error Handling & Connection Shutdown

Studied HTTP/3 and QUIC error handling at both stream and connection scope. Clarified that `RESET_STREAM`, `STOP_SENDING`, and `CONNECTION_CLOSE` are QUIC transport mechanisms and are not part of the HTTP/3 `SETTINGS` frame. Distinguished HTTP status codes such as 2xx/4xx/5xx from `H3_*` HTTP/3 protocol error codes. Covered `GOAWAY` as an HTTP/3 graceful-shutdown mechanism and compared it with QUIC `CONNECTION_CLOSE`. Also compared HTTP/2's `RST_STREAM` and `GOAWAY` with the corresponding HTTP/3/QUIC architecture, reinforcing the key distinction that QUIC understands streams as transport primitives while TCP provides a single byte stream.

## Lesson 48 — HTTP/3 Push & Prioritization

Studied HTTP/3 Server Push, `PUSH_PROMISE`, and why Server Push became uncommon in modern browser deployments due to cache uncertainty, wasted bandwidth, and scheduling complexity. Compared Server Push with client-side preload and clarified that preload is a web-platform hint rather than an HTTP/3 transport feature. Covered HTTP/3 prioritization and `PRIORITY_UPDATE`, emphasizing that priority is scheduling intent rather than a delivery guarantee and that QUIC flow control and congestion control still constrain transmission.

## Lesson 49 — HTTP/3 ↔ QUIC Integration

Established the exact responsibility boundary between HTTP/3 and QUIC. Traced HTTP/3 frames through QUIC streams, QUIC `STREAM` frames, QUIC packets, UDP, and IP. Clarified that QPACK and HTTP/3 control streams belong to HTTP/3 while QUIC provides the underlying transport streams. Consolidated the distinction between HTTP/3 `DATA` and QUIC `STREAM`, and connected QUIC-owned mechanisms such as flow control, loss recovery, congestion control, TLS integration, connection IDs, and connection migration to the HTTP/3 layer.

## Lesson 50 — HTTP/3 Performance & Trade-offs

Studied why HTTP/3 can outperform HTTP/2 under particular network conditions, focusing on QUIC's independent streams and elimination of TCP-level cross-stream head-of-line blocking. Reviewed QUIC/TLS handshake latency, 0-RTT and its replay caveat, connection migration, and why UDP itself is not inherently faster than TCP. Covered the additional implementation and packet-processing complexity introduced by QUIC and the practical reality that HTTP/3 is not universally faster than HTTP/2. Consolidated the HTTP/1.1 → HTTP/2 → HTTP/3 evolution as a sequence of architectural responses to specific limitations.

## Lesson 51 — HTTP Evolution: The Big Consolidation

Consolidated the full HTTP/1.1 → HTTP/2 → QUIC → HTTP/3 evolution. Focused on why HTTP/1.1 needed better concurrency, why HTTP/2 introduced multiplexing, and why multiplexing over TCP still leaves TCP-level cross-stream head-of-line blocking. Connected that limitation to the architectural motivation for QUIC and then to HTTP/3's adaptation of HTTP semantics to QUIC. Also consolidated QPACK, QUIC flow control, integrated TLS, 0-RTT, connection migration, and the distinction between HTTP-level errors and transport-level failures. The main mental model is that each generation addresses a specific architectural limitation rather than simply being a universally 'better' HTTP version.

## Lesson 52 — Build an HTTP/3 Request From Scratch

Traced a single HTTP/3 GET request through the complete protocol stack: HTTP semantics → HTTP/3 HEADERS → QPACK → QUIC stream → QUIC STREAM frame → QUIC packet → UDP → IP → network, and then through the reverse decapsulation path at the server. Reinforced the distinction between HTTP/3 frames and QUIC transport frames, especially `DATA` versus `STREAM`, and consolidated protocol layering, encapsulation, decapsulation, and layer responsibilities. This lesson serves as the second major HTTP/3 consolidation and completes the end-to-end mental model for how an HTTP/3 request actually becomes network traffic and is reconstructed at the receiver.

## Lesson 53 — Sessions

Started the Higher-Level HTTP section by studying how applications maintain continuity over stateless HTTP. Learned the distinction between cookies and sessions, traced the login/session-ID flow, and covered session lifecycle, expiration, cookie security, session hijacking, and session fixation. Then moved into the systems perspective: process-local sessions do not naturally scale across horizontally scaled servers, sticky sessions provide one workaround, and shared session stores allow multiple servers to access common authentication state at the cost of introducing another distributed dependency. The key takeaway is that session management is fundamentally a state-management and scalability problem, not merely a cookie mechanism.
