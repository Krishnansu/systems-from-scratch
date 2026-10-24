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


## 2026-10-19 — Lesson 86: API Gateway Fundamentals

Studied the API Gateway as an API-facing entry point for routing and cross-cutting policies such as TLS termination, authentication integration, rate limiting, and observability. Distinguished gateway routing to a logical service from load balancing across service instances and application routing to controllers. Examined common Kubernetes deployment patterns with gateway replicas, external entry points, Services, and backend pods. Reinforced that backend services retain resource-level authorization responsibilities and that timeouts do not prove a write operation failed, making safe retry and idempotency design essential. Next: Lesson 87 — Forward Proxy Fundamentals.


## 2026-10-19 — Lesson 87: Forward Proxy Fundamentals

Studied forward proxies as client-side intermediaries for outbound access policy, authentication, auditing, and caching. Traced HTTP forwarding and HTTPS CONNECT tunneling, distinguishing ordinary tunneling from TLS interception. Compared forward proxies with reverse proxies, NAT, and VPNs, and examined proxy bypass, open-proxy risks, and fail-open versus fail-closed behavior. Next: Lesson 88 — Reverse Proxy Fundamentals.


## 2026-10-19 — Lesson 88: Reverse Proxy Fundamentals

Studied reverse proxies as controlled entry points for incoming requests. Traced request forwarding, host/path routing, TLS termination, and backend responses. Distinguished reverse proxies from forward proxies, load balancers, and API gateways, and covered trusted forwarding headers, backend authorization, and production failure concerns. Next: Lesson 89 — NGINX Fundamentals.


## 2026-10-19 — Lesson 89: NGINX Fundamentals

Studied NGINX as a web server, reverse proxy, and load balancer. Read a basic configuration using `listen`, `server_name`, `location`, and `proxy_pass`; traced request routing; compared upstream groups; and covered URI rewriting, forwarding headers, and 502/504 troubleshooting. Next: Lesson 90 — Load Balancing Fundamentals.


## 2026-10-19 — Lesson 90: Load Balancing Fundamentals

Studied why load balancing distributes work across backend instances and compared round robin, weighted round robin, least connections, latency-aware selection, and sticky sessions. Covered active and passive health checks, backend removal and recovery, retry safety and idempotency, shared-dependency bottlenecks, and load-balancer redundancy. The exercises reinforced that connection counts approximate rather than measure workload, and that scaling application instances can increase pressure on shared dependencies. Next: Lesson 91 — SSL/TLS Termination.


## 2026-10-19 — Lesson 91: SSL/TLS Termination

Studied TLS termination at a reverse proxy and compared plaintext upstream forwarding, TLS re-encryption, and TLS passthrough. Covered certificate and private-key roles, SNI versus HTTP Host, trusted forwarding headers, upstream certificate verification, mTLS, and certificate lifecycle management. The exercises reinforced that HTTPS at the edge does not automatically encrypt internal hops and that upstream TLS requires identity verification. Next: Lesson 92 — Routing Fundamentals.


## 2026-10-19 — Lesson 92: Routing Fundamentals

Studied host-based and path-based routing, NGINX virtual server selection, location matching precedence, the meaning of `^~`, upstream selection, and `proxy_pass` URI rewriting. Reinforced that routing and load balancing are separate decisions and that a correct backend selection does not guarantee a successful response. Next: Lesson 93 — Health Checks and Backend Availability.


## 2026-10-19 — Lesson 93: Health Checks and Backend Availability

Studied how reverse proxies and load balancers assess backend availability. Distinguished liveness from readiness and active probes from passive failure observation. Examined health-check intervals, thresholds, timeouts, recovery safeguards, and flapping. Discussed why overly broad dependency checks can remove otherwise useful instances during a shared database incident, and why health checks must be complemented by metrics, logs, traces, and latency investigation. Next: Lesson 94 — Firewall Fundamentals.


## 2026-10-19 — Lesson 94: Firewall Fundamentals

Studied firewalls as network access controls and compared stateful connection tracking with stateless packet filtering. Covered inbound and outbound rules, default-deny policies, network segmentation, and least-privilege access between reverse proxies, application servers, and databases. Distinguished firewall filtering from reverse-proxy routing, WAF inspection, and application authorization. Practiced a layer-by-layer approach to diagnosing connectivity timeouts without assuming the firewall is always responsible. Next: Lesson 95 — VPN Fundamentals.


## 2026-10-19 — Lesson 95: VPN Fundamentals

Studied VPNs as protected logical connections over existing networks. Covered tunneling and encapsulation, endpoint authentication, remote-access versus site-to-site VPNs, and full-tunnel versus split-tunnel routing. Distinguished VPNs from proxies and firewalls, examined where tunnel encryption ends, and connected routing, DNS, return paths, firewall rules, and application health to VPN troubleshooting. Next: Lesson 96 — Why Containers?


## 2026-10-19 — Lesson 96: Why Containers?

Started Module 06 — Docker. Learned how application environments cause deployment drift, why containers package application files and user-space dependencies, and how Linux namespaces, cgroups, filesystem isolation, and security controls support container execution. Compared containers with virtual machines and covered limits around security, configuration, networking, and persistent data. Next: Lesson 97 — Images.


## 2026-10-19 — Lesson 97: Images

Studied container images as packaged filesystem layers and metadata, and containers as runtime instances with configuration and a writable layer. Covered registries and the build → push → pull → run lifecycle; distinguished mutable tags such as `latest` from content-based digests; and connected artifact identity to reproducible production deployments. Reinforced that runtime configuration and secrets should generally remain outside the image, and that successful image retrieval does not prove successful application startup. Next: Lesson 98 — Layers.


## 2026-10-21 — Lesson 98: Layers

Studied how container images combine filesystem layers and how build caching reuses prior results when relevant instructions and inputs remain unchanged. Examined cache invalidation, why copying stable dependency manifests before frequently changing source improves build efficiency, and the distinction between read-only image layers and a container's writable layer. Connected layer design to build performance, storage reuse, persistent volumes, and the security risk of secrets remaining in earlier layers. Next: Lesson 99 — Dockerfile.


## 2026-10-21 — Lesson 99: Dockerfile

Studied Dockerfiles as image-build recipes and distinguished the build context, resulting image, and runtime container. Covered `FROM`, `WORKDIR`, `COPY`, `RUN`, `CMD`, `ENTRYPOINT`, and `ENV`; clarified build-time execution versus container startup and how `CMD` supplies defaults or a complete command. Examined build-context boundaries, `.dockerignore`, cache-friendly instruction ordering, and multi-stage builds. Reinforced that environment-specific configuration and secrets should be supplied separately from image contents, and that production images should be minimal, maintained, and run with least privilege where practical. Next: Lesson 100 — Namespaces.


## 2026-10-21 — Lesson 101: cgroups

Studied Linux control groups as the mechanism for accounting for and controlling process resource consumption. Distinguished cgroups from namespaces, explored CPU quota versus CPU weight, and reviewed cgroup v2 memory controls including `memory.current`, `memory.max`, and `memory.events`. Clarified why a container can hit its memory limit while the host still has free RAM, and why reaching the limit does not necessarily terminate every process immediately. Next: Lesson 102 — Volumes.


## 2026-10-21 — Lesson 102: Volumes

Studied the difference between a container's writable layer and persistent storage. Compared Docker-managed named volumes with host-path bind mounts and introduced tmpfs. Practiced creating, inspecting, mounting, reusing, and removing a named volume, and examined how mounts can obscure files already present in an image. Connected storage persistence to production requirements for backups, restore testing, permissions, capacity monitoring, replication, and recovery. Next: Lesson 103 — Docker Networks.


## 2026-10-21 — Lesson 103: Docker Networks

Studied how Docker connects isolated container network namespaces using network drivers and, on typical Linux bridge networks, veth pairs and a Linux bridge. Compared the default bridge with user-defined bridges and practiced container-name resolution, container-to-container HTTP connectivity, and host port publishing. Distinguished container ports from published host ports and reinforced that `localhost` inside a container refers to that container itself. Covered bridge, host, none, and overlay networking at a high level, plus a layered troubleshooting process for DNS, reachability, listening ports, and application health. Reinforced least-exposure principles by keeping internal service ports unpublished when host access is unnecessary. Next: Lesson 104 — Docker Compose.


## 2026-10-22 — Lesson 104: Docker Compose

Completed Module 06 by learning how Docker Compose declaratively defines and manages related services in a YAML file. Connected Compose to Docker's underlying containers, networks, and volumes; practiced service-name communication, host port publishing, environment configuration, health checks, dependency startup conditions, logs, inspection, and safe cleanup. Reinforced that startup order is not the same as readiness, that named volumes normally survive `docker compose down`, and that `down -v` can delete persisted data. Reviewed troubleshooting from service status and logs through network, health, and configuration checks. Next: Lesson 105 — Kubernetes Architecture.


## 2026-10-22 — Lesson 105: Kubernetes Architecture

Started Module 07 by examining Kubernetes as a cluster orchestrator beyond single-host container management. Distinguished the control plane from worker nodes and covered the responsibilities of kube-apiserver, etcd, kube-scheduler, kube-controller-manager, kubelet, the container runtime through CRI, and cluster networking components. Traced a simplified workload flow from desired configuration through controller reconciliation, node assignment, and runtime execution. Reinforced that controllers work toward desired state rather than guaranteeing immediate convergence, that etcd stores Kubernetes cluster state rather than application business data, and that insufficient scheduling capacity can leave a Pod Pending. Distinguished scheduling constraints from runtime memory-limit failures. Next: Lesson 106 — Pods.


## 2026-10-24 — Lesson 106: Kubernetes Pods

Studied Pods as Kubernetes' smallest deployable and schedulable unit. Distinguished Nodes, Pods, and containers; covered shared Pod networking, localhost communication, port conflicts, and explicitly configured shared volumes. Reviewed single-container and sidecar patterns, Pod phases, readiness versus Running status, and the ephemeral nature of Pod IPs. Connected Services to stable access across Pod replacement and controllers to maintaining desired replica counts. Practiced the purpose of read-only `kubectl` inspection and log commands, with attention to cluster permissions and sensitive output. Next: Lesson 107 — ReplicaSets.


## 2026-10-24 — Lesson 107: Kubernetes ReplicaSets

Studied ReplicaSets as controllers that reconcile the desired number of matching Pods with the observed count. Covered selectors, Pod templates, replacement Pod objects, and the distinction between current and ready replicas. Connected ReplicaSets to the scheduler, kubelet, container runtime, and Services, and clarified why Deployments manage ReplicaSets for versioned rollouts and rollback. Also covered capacity constraints and why replica management cannot guarantee that Pods become healthy or Ready. Next: Lesson 108 — Deployments.


## 2026-10-24 — Lesson 108: Kubernetes Deployments

Studied why Deployments manage ReplicaSets to coordinate versioned application rollouts. Covered Pod-template changes and revision history, rolling updates, `maxSurge` and `maxUnavailable`, readiness failures and stalled rollouts, rollout status/history inspection, and rollback. Reinforced that rollback restores an earlier Pod template but does not reverse database migrations or external side effects. Next: Lesson 109 — Kubernetes Services.


## 2026-10-24 — Lesson 109: Kubernetes Services

Studied why Services provide stable network access to replaceable Pods. Covered selectors, Pod labels, EndpointSlices, readiness and endpoint eligibility, `port` versus `targetPort` and `nodePort`, and the ClusterIP, NodePort, LoadBalancer, and headless Service models. Clarified cross-namespace Service access, DNS resolution versus data-plane traffic forwarding, and why backend selection usually follows connection or flow behavior rather than choosing a different Pod for each HTTP request. Practiced a read-only troubleshooting sequence covering Service configuration, selectors, Pod labels and readiness, EndpointSlices, application ports, DNS, and networking restrictions. Next: Lesson 110 — Kubernetes Ingress.


## 2026-10-24 — Lesson 110: Kubernetes Ingress

Studied Ingress as declarative HTTP/HTTPS routing into a Kubernetes cluster. Distinguished Ingress resources from controllers, traced traffic from DNS and an external entry point through host/path matching to backend Services and eligible Pods, and reviewed path types, IngressClass, TLS Secrets, and TLS termination. Compared Ingress with LoadBalancer Services and covered controller-dependent behavior, common failure symptoms, and read-only inspection commands. Next: Lesson 111 — Kubernetes ConfigMaps.


## 2026-10-24 — Lesson 111: Kubernetes ConfigMaps

Studied ConfigMaps as namespaced Kubernetes objects for non-confidential configuration, separating environment-specific settings from application images. Covered key-value and file-like data, environment-variable references, `envFrom`, and mounted configuration files. Clarified that environment variables in existing containers do not change after a ConfigMap update, projected files update eventually, `subPath` mounts do not receive automatic updates, and applications may need a reload or rollout. Distinguished ConfigMaps from Secrets and reviewed safe inspection and troubleshooting. Next: Lesson 112 — Kubernetes Secrets.


## 2026-10-24 — Lesson 112: Kubernetes Secrets

Studied Kubernetes Secrets as namespaced objects for sensitive configuration and compared them with ConfigMaps. Covered `stringData`, Base64-encoded `data`, environment-variable references, mounted Secret files, and update behavior. Clarified that Base64 is not encryption, RBAC and encryption at rest serve different purposes, and runtime access still needs careful control. Reviewed safe inspection and troubleshooting practices, plus credential rotation across application reloads and database connections. Next: Lesson 113 — Kubernetes Persistent Volumes.


## 2026-10-24 — Lesson 113: Kubernetes Persistent Volumes

Studied how Kubernetes separates replaceable Pods from durable storage. Distinguished PersistentVolumes, PersistentVolumeClaims, and StorageClasses; traced claim binding and Pod volume mounting; and compared static with dynamic provisioning. Reviewed access modes, reclaim policies, and the difference between persistence and backup. Practiced a read-only storage inspection and troubleshooting sequence, emphasizing that a Pending claim and a Bound claim with a mount failure represent different stages. Next: Lesson 114 — Kubernetes Autoscaling.


## 2026-10-24 — Lesson 114: Kubernetes Autoscaling

Studied Kubernetes autoscaling as three related but distinct concerns: HPA changes workload replica counts based on metrics, VPA recommends or adjusts per-Pod resource sizing, and Cluster Autoscaler adjusts node capacity when supported and configured. Covered CPU utilization targets relative to resource requests, the role of the metrics pipeline, the simplified HPA replica formula, scaling limits and delays, and the chain from metric observation to scheduling and Pod readiness. Emphasized that HPA does not add worker nodes, desired Pods may remain Pending without capacity, and extra replicas may not help when a shared dependency is saturated. Next: Lesson 115 — Kubernetes Scheduling.


## 2026-10-24 — Lesson 115: Kubernetes Scheduling

Studied how kube-scheduler selects a node for a Pod through filtering and scoring. Covered resource requests and node allocatable capacity, node selectors, node and Pod affinity, taints and tolerations, topology spread, and storage constraints. Connected autoscaling to scheduling by tracing how HPA-created replicas can remain Pending when no eligible node has capacity, and clarified that Cluster Autoscaler can help with supported capacity shortages but cannot resolve arbitrary placement constraints. Practiced a read-only troubleshooting sequence that distinguishes unscheduled Pods from Pods assigned to a node but still waiting for setup. Next: Lesson 116 — Kubernetes Health Checks and Probes.


## Lesson 116 — Kubernetes Health Checks and Probes

Consolidated startup, liveness, and readiness probes and their distinct effects. A configured startup probe gates the other probes until startup succeeds; liveness failures can restart containers, while readiness failures remove Pods from normal ready Service traffic without restarting them. Reviewed HTTP, TCP, exec, and gRPC probe mechanisms, plus practical inspection using Pod events, logs, and EndpointSlices. Next: Lesson 117 — Kubernetes Workload Types.


## Lesson 117 — Kubernetes Workload Types

Compared Deployments, StatefulSets, DaemonSets, Jobs, and CronJobs by workload lifecycle and guarantees. Distinguished interchangeable replicas from stable identity and storage association, node-level agents, finite tasks, and scheduled tasks. Noted that StatefulSets do not automatically provide data replication or high availability and that Job/CronJob execution is not an exactly-once guarantee. Next: Lesson 118 — Resource Management, QoS, and Eviction.


## Lesson 118 — Resource Management, QoS, and Eviction

Covered requests versus limits, CPU throttling versus memory OOM kills, Kubernetes Guaranteed/Burstable/BestEffort QoS classes, and node-pressure eviction. Reviewed how requests affect scheduling and how usage relative to requests and Pod priority can influence eviction decisions. Practiced read-only diagnostics for resource usage, node pressure, events, and Pending Pods. Next: Lesson 119 — Kubernetes Security: RBAC, Workload Identity, and Network Policies.


## Lesson 119 — Kubernetes Security: RBAC, Workload Identity, and Network Policies

Studied three complementary Kubernetes security boundaries: RBAC authorization for Kubernetes API actions, ServiceAccounts and workload identity for identifying workloads, and NetworkPolicies for restricting Pod traffic. Distinguished identities from permissions, Roles from bindings, and API authorization from network access control. Reviewed least privilege, provider-specific external workload identity, CNI-dependent NetworkPolicy enforcement, and read-only diagnostics for permissions and connectivity. Next: Lesson 120 — End-to-End Kubernetes Troubleshooting Lab.
