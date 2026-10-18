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

## Lesson 54 — JWT

Studied JWT as an alternative authentication model to server-side sessions. Learned the header/payload/signature structure, the distinction between Base64URL encoding and encryption, and how signature verification establishes token integrity and authenticity. Clarified that JWTs can be self-contained or intentionally minimal, with application data still coming from databases or caches when needed. Compared JWTs with sessions from a distributed-systems perspective, including horizontal scaling, revocation, short-lived access tokens, refresh tokens, symmetric versus asymmetric signing, and key rotation. Also clarified practical credential storage: browser applications commonly use secure cookies or carefully managed client-side storage, while native clients should use OS-provided secure credential stores. The central takeaway is that JWTs change where authentication state is represented and trade centralized server-side control for locally verifiable credentials.

## Lesson 55 — Caching

Studied caching as a systems performance mechanism rather than simply as Redis. Covered why caches reduce latency and backend load, cache hits and misses, browser/CDN/application/distributed-cache hierarchy, TTL and expiration, eviction policies, cache-aside, invalidation, cache stampedes, and hot keys. Clarified the distinction between a cache and a database, including the fact that Redis is primarily in-memory while still supporting persistence. Established the physical mental model of distributed Redis as multiple machines whose Redis processes keep working datasets in RAM, with sharding distributing keys and replication creating additional copies.

## Lesson 56 — Compression

Studied HTTP compression as a CPU-versus-network trade-off. Covered why redundancy makes data compressible, why text-based formats such as JSON, HTML, CSS, and JavaScript benefit from compression, and why already-compressed formats usually do not. Clarified that both request and response bodies can be compressed, with `Accept-Encoding` representing client capabilities and `Content-Encoding` identifying the encoding applied to a body. Covered gzip and Brotli, compression levels, static versus dynamic content, compression before encryption, and caching different encoded representations with `Vary: Accept-Encoding`. Distinguished HTTP body compression from HTTP/2 HPACK and HTTP/3 QPACK header compression. The central takeaway is that compression is an engineering trade-off: spend CPU to reduce bytes on the network when the resulting savings justify the cost.

## Lesson 57 — WebSockets

Studied WebSockets as a solution for applications that require persistent, bidirectional communication rather than repeated HTTP request/response exchanges. Covered polling and long polling as earlier approaches, the HTTP Upgrade handshake and `101 Switching Protocols`, WebSocket frames, text and binary messages, ping/pong heartbeats, and the close handshake. Then examined production concerns including long-lived connections, load balancers, backend failures, reconnection, state resynchronization, and cross-server message delivery through shared messaging infrastructure. The central takeaway is that WebSockets change the communication model from request/response to a persistent bidirectional channel, but introduce their own distributed-systems challenges around connection lifecycle and scaling.

## Lesson 58 — WebSocket Protocol Deep Dive

Studied the WebSocket wire protocol after the HTTP Upgrade handshake. Covered frame structure, FIN, opcodes, text and binary frames, client-to-server masking, payload length encoding, fragmentation, control frames, Ping/Pong, the close handshake, and the distinction between WebSocket framing and TCP's byte stream. Clarified that masking is not encryption and that TLS provides confidentiality for `wss://` connections.

## Lesson 59 — WebSocket Lifecycle & Reliability

Studied the production lifecycle of WebSocket connections and the failure modes that occur after the initial connection succeeds. Covered heartbeats, liveness detection, reconnect storms, exponential backoff, jitter, sequence numbers, missed messages, event replay, and state synchronization. The central takeaway is that connection-level reliability does not automatically provide application-level message recovery after a disconnect.

## Lesson 60 — WebSockets at Scale

Studied how WebSockets scale horizontally when a single connection server is no longer sufficient. Covered load balancers, long-lived connection ownership, sticky sessions, distributed connection registries, cross-server messaging, message brokers, broadcasting/fan-out, presence, and backend failure. Clarified that an established WebSocket connection cannot simply be migrated between servers; clients reconnect after failure and may resume or resynchronize state. The central takeaway is that production WebSockets become a distributed-systems problem involving connection state, event routing, failure recovery, and coordination between multiple connection-owning servers.

## Lesson 61 — HTTP vs WebSocket vs WebRTC

Compared HTTP, WebSocket, and WebRTC as different communication models. Established HTTP as request/response, WebSocket as persistent bidirectional client/server communication, and WebRTC as real-time peer-to-peer communication. Explored why WebRTC is better suited to video/audio because it is designed around real-time media, while WebSocket is often better for server-backed chat because the server can provide persistence, routing, authentication, moderation, presence, and offline delivery. Covered WebRTC signaling and the roles of SDP, ICE, STUN, TURN, and DataChannels. The central takeaway is that WebSocket and WebRTC are complementary: WebSocket can handle signaling, chat, and application coordination while WebRTC carries real-time media or peer-to-peer data.

## Lesson 62 — HTTP Module Consolidation

Consolidated the complete HTTP module into a single systems mental model. Reviewed the evolution from HTTP/1.1 to HTTP/2, QUIC, and HTTP/3, then connected sessions and JWT to authentication state, caching and compression to performance, WebSockets to persistent server-backed real-time communication, and WebRTC to peer-to-peer real-time media and data. Reinforced that these technologies form a toolbox rather than a simple replacement chain, and that systems design should begin with the communication problem and required properties before selecting a technology. This lesson completes the HTTP module.

## Lesson 63 — Linux Architecture

Started the Linux module by examining why operating systems are needed and how hardware, the Linux kernel, and user space fit together. Covered kernel responsibilities, system calls, user mode versus kernel mode, the distinction between root and kernel mode, and the role of shells and distributions. Traced conceptual file-read and network-send paths and explored basic Linux inspection commands. Connected these architectural boundaries to production debugging and prepared the foundation for processes, scheduling, memory, filesystems, and networking.


## 2026-10-10 — Lesson 64: Processes

Studied the difference between a program and a process, process creation with `fork()` and program replacement with `execve()`, scheduling and context switching, common process states, parent-child relationships, virtual memory, file descriptors, and practical Linux process inspection for production debugging.


## 2026-10-10 — Lesson 65: Threads

Studied why threads provide multiple execution paths within a process, which resources are shared versus thread-local, how Linux represents and schedules threads, and the distinction between concurrency and parallelism. Explored race conditions, mutexes, contention, deadlocks, event-loop alternatives, and commands for inspecting Linux threads.


## 2026-10-10 — Lesson 66: CPU Scheduling

Studied how the OS chooses runnable threads for CPU time and balances fairness, responsiveness, throughput, and policy requirements. Distinguished running, runnable, and waiting states; covered preemption, time slices, and context-switch overhead. Compared FCFS, SJF, SRTF, Round Robin, priority scheduling, MLFQ, and EDF, including their trade-offs. Connected classic scheduling concepts to Linux's fair-scheduling class and real-time policies such as `SCHED_FIFO` and `SCHED_RR`, and reviewed how to investigate CPU contention and interpret load average in production. Next: Lesson 67 — Memory Management.


## 2026-10-10 — Lesson 67: Memory Management

Studied virtual memory and physical RAM, process address spaces, paging, page frames, page tables, the MMU and TLB, and memory protection. Distinguished normal page faults from invalid memory accesses, and covered demand paging, minor versus major faults, copy-on-write, memory reclamation, swap, and OOM behavior. Practiced inspecting Linux memory with `free` and `/proc` interfaces, and connected memory pressure and page-fault activity to production latency. Next: Lesson 68 — File Systems.


## 2026-10-10 — Lesson 68: File Systems

Studied why file systems are needed to organize storage, and how paths, directories, inodes, hard links, symbolic links, and file descriptors relate. Traced the Linux file-open path through system calls, path lookup, VFS, filesystem implementations, and the page cache or storage I/O. Connected mount points and inode capacity to production debugging, and practiced inspecting filesystems, free space, and open descriptors. Next: Lesson 69 — Linux Permissions.


## 2026-10-10 — Lesson 69: Linux Permissions

Studied Linux users, groups, UIDs/GIDs, ownership, and the traditional owner/group/other permission model. Learned to interpret symbolic permissions and numeric modes, and clarified how read, write, and execute differ for files versus directories. Traced simplified kernel access checks, including the importance of parent-directory traversal permissions, and reviewed `chmod`, `chown`, `chgrp`, ACLs, special permission bits, and least privilege. Connected permission failures to production debugging and why backend services should not run as root by default. Next: Lesson 70 — Linux Signals.


## 2026-10-10 — Lesson 70: Linux Signals

Studied Linux signals as kernel-managed notifications for processes and threads. Compared `SIGTERM`, `SIGKILL`, `SIGINT`, `SIGSTOP`, `SIGCONT`, and `SIGCHLD`; examined signal delivery, default actions, handlers, blocked and pending signals, standard-signal coalescing, and process-directed versus thread-directed signals. Connected signals to graceful backend shutdown, process supervision, and safe Linux process inspection. Next: Lesson 71 — Linux Services.


## 2026-10-10 — Lesson 71: Linux Services

Studied Linux services as managed operational units and distinguished them from individual processes. Examined `systemd` as a common Linux service manager, unit configuration, lifecycle states, dependencies, restart policies, and the difference between starting and enabling a service. Practiced inspecting service status and logs with `systemctl` and `journalctl`, and connected service shutdown to `SIGTERM`, bounded cleanup, and production reliability. Next: Lesson 72 — Linux Networking Tools.

## Lesson 72 — Linux Networking Tools

Learned to inspect Linux network interfaces and assigned IP addresses with `ip link` and `ip addr`, examine routing tables and destination-specific route choices with `ip route`, and inspect listening sockets and established TCP connections with `ss`. Distinguished ICMP reachability checks using `ping` from actual HTTP requests using `curl`. Practiced diagnosing a service that works locally but is unreachable remotely, including checking whether it listens only on loopback, and reinforced that interface state, routing, sockets, firewalls, network namespaces, and application health are separate pieces of evidence.


## 2026-10-10 — Lesson 73: Linux Module Consolidation

Consolidated Linux architecture, processes, threads, scheduling, memory, filesystems, permissions, signals, services, and networking into a production troubleshooting mental model. Connected service state, process health, listening sockets, resource pressure, access control, and downstream dependencies. Practiced choosing targeted diagnostics from symptoms, separating evidence from assumptions, and verifying fixes rather than repeatedly restarting services or making broad changes. Next: Lesson 74 — API Fundamentals.


## 2026-10-13 — Lesson 74: API Fundamentals

Started Module 04 by defining APIs as interfaces that let software components interact through agreed contracts. Distinguished APIs from HTTP, backend services, clients, and databases. Walked through a GET request for an order and connected endpoint methods, resources, requests, responses, and JSON representations. Examined why stable contracts enable independent client and server development, how incompatible response changes can break consumers, and why API boundaries still require explicit authentication, authorization, and input validation. Next: Lesson 75 — REST Fundamentals.


## 2026-10-13 — Lesson 75: REST Fundamentals

Studied REST as an architectural style for distributed systems and distinguished it from HTTP and from the broader category of HTTP + JSON APIs. Covered resources, resource identifiers, representations, the six REST constraints, and resource-oriented endpoint design. Compared GET, POST, PUT, PATCH, and DELETE, including safe and idempotent semantics and why retries require care after timeouts. Connected these principles to filtering, pagination, gateways, backend services, and production API contracts. Next: Lesson 76 — REST API Design in Practice.


## 2026-10-15 — Lesson 76: REST API Design in Practice

Applied REST principles to production API contracts. Covered resource-oriented URLs, relationship modeling and nested-route trade-offs, HTTP status codes, consistent error responses using Problem Details, filtering and pagination with offset and cursor approaches, deterministic ordering, and API versioning and backward compatibility. Connected endpoint design to authorization, validation, database performance, observability, and safe error handling. Next: Lesson 77 — GraphQL Fundamentals.


## 2026-10-15 — Lesson 77: GraphQL Fundamentals

Introduced GraphQL as a typed API query language and execution runtime. Covered why client-selected fields can reduce over-fetching and under-fetching, schema types and nullability, queries, mutations, variables, and resolver execution. Examined the N+1 problem and batching, and connected GraphQL to production concerns including authorization, query complexity, caching, and observability. Compared GraphQL and REST as complementary API design choices with different operational trade-offs. Next: Lesson 78 — GraphQL Execution, Resolvers & DataLoader.


## 2026-10-17 — Lesson 78: GraphQL Execution, Resolvers & DataLoader

Traced GraphQL operations from parsing and validation through field execution and response assembly. Examined resolver arguments, parent values, context, and data-source boundaries. Explained the N+1 query problem and how DataLoader batches keys and caches repeated loads within a request, including the requirement to preserve key order. Covered query versus mutation execution ordering, null propagation for non-null fields, request-scoped cache safety, and production concerns around authorization and observability. Next: Lesson 79 — GraphQL Performance, Security & Production Design.


## 2026-10-18 — Lesson 79: GraphQL Performance, Security & Production Design

Studied production GraphQL guardrails, including query depth and complexity, pagination caps, aliases and fan-out, authorization boundaries, cache scope and invalidation, persisted queries, introspection policy, timeout and cancellation limitations, and observability across resolvers, databases, DataLoader, and downstream dependencies. Reinforced that schema validation does not authorize access and that reducing HTTP request count does not necessarily reduce backend work. Next: Lesson 80 — API Rate Limiting, Quotas & Abuse Prevention.


## 2026-10-18 — Lesson 80: API Rate Limiting, Quotas & Abuse Prevention

Studied why APIs need rate limits and how they differ from quotas, concurrency limits, and query-cost limits. Compared fixed windows, sliding windows, token buckets, and leaky buckets, including their burst and resource trade-offs. Covered tenant-aware limit keys, shared enforcement across multiple API servers, atomic limiter state, Redis failure policies, HTTP 429 and Retry-After, exponential backoff with jitter, and production observability. The exercise reinforced that a shared limiter prevents per-server limits from multiplying, burst acceptance depends on the algorithm and policy, and concurrency limits protect expensive long-running work. Next: Lesson 81 — Circuit Breakers & Resilience (proposed continuation).


## 2026-10-18 — Lesson 81: Circuit Breakers & Resilience

Studied circuit breakers as a defense against cascading failures in distributed services. Covered Closed, Open, and Half-Open states; thresholds and recovery probes; and how breakers complement timeouts, bounded retries, rate limits, bulkheads, and fallbacks. Examined per-pod breaker state versus shared coordination, failure classification, synchronized recovery traffic, and safe degraded responses. The exercise reinforced that local breakers can react independently and that fallbacks must preserve product correctness. Next: Lesson 82 — gRPC Fundamentals (proposed continuation).


## 2026-10-18 — Lesson 82: gRPC Fundamentals

Studied RPC and gRPC as a service-to-service communication model. Covered Protobuf service/message contracts, generated client stubs, field-number compatibility, and the request lifecycle over HTTP/2 streams and DATA frames. Compared unary, server-streaming, client-streaming, and bidirectional-streaming RPCs, and contrasted gRPC with REST. Reinforced that deadlines do not prove a remote side effect failed, so retries require care and idempotency for operations such as payments. Next: Lesson 83 — Authentication Fundamentals (proposed continuation).


## 2026-10-18 — Lesson 83: Authentication Fundamentals

Studied authentication as the process of establishing a user's, service's, or workload's identity, and distinguished it from authorization. Covered identities, credentials, principals, server-side sessions, access tokens, JWT validation, and opaque-token introspection. Examined production trust boundaries across identity providers, API gateways, and backend services, including the risks of spoofable identity headers and gateway bypasses. Distinguished user identity from workload identity and discussed how service-to-service authentication can use mechanisms such as mTLS. Next: Lesson 84 — Authorization Fundamentals.


## 2026-10-18 — Lesson 84: Authorization Fundamentals

Studied authorization as the decision about which actions an authenticated identity may perform on specific resources. Compared RBAC, ABAC, and ReBAC; examined gateway versus backend authorization boundaries; and covered object-level access checks, IDOR/BOLA vulnerabilities, least privilege, and deny-by-default policies. Reinforced that valid authentication does not imply permission to access every resource, and that hiding frontend controls or using unpredictable identifiers cannot replace server-side authorization. Next: Lesson 85 — OAuth Fundamentals.


## 2026-10-18 — Lesson 85: OAuth Fundamentals

Studied OAuth as a delegated-authorization framework and distinguished it from authentication and OpenID Connect. Covered the resource owner, client, authorization server, and resource server; traced Authorization Code with PKCE; and differentiated authorization codes, access tokens, refresh tokens, and OIDC ID tokens. Examined scopes, audience validation, token protection, redirect URI validation, and Client Credentials for application-level access without user delegation. Reinforced that token validity does not replace resource-level authorization. Next: Lesson 86 — API Gateway Fundamentals.
