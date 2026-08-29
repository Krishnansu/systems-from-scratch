# Systems From Scratch Roadmap

## Module 00 — Foundation

- [x] Repository setup
- [ ] Repository documentation
- [ ] Learning workflow

---

## Module 01 — Networking

- [x] What is the Internet?
- [x] What is a Network?
- [x] How Does Data Travel Across a Network?
- [x] Bits, Frames and Packets
- [x] OSI Model
- [x] TCP/IP Model
- [x] Encapsulation & Decapsulation
- [x] IP Addressing
- [x] Subnets & CIDR
- [x] ARP
- [x] Routing
- [x] Network Address Translation (NAT)
- [x] DNS
- [x] TCP
- [x] UDP
- [x] How the Web Works
  - [x] DNS → TCP → TLS → HTTP
  - [x] Browser Request Journey
  - [x] HTTP/3 → QUIC → UDP overview

---

## Module 02 — HTTP

### HTTP Fundamentals

- [x] Why HTTP?
- [x] HTTP Request / Response Model
- [x] HTTP Request Lifecycle
- [x] HTTP Methods
- [x] HTTP Headers
- [x] HTTP Status Codes
- [x] HTTP Request / Response Structure
- [x] Cookies & Statelessness
- [x] Content Negotiation
- [x] Idempotency

### HTTP Across the Network

- [x] HTTP Request Journey Across All Layers
- [x] HTTP → TCP → IP → Network
- [x] TCP Stream vs HTTP Messages
- [x] HTTP Message Boundaries
- [x] HTTP Request Framing

### Building HTTP from Scratch

- [x] Build a TCP Server in Python
- [x] Build a Raw HTTP Server
- [x] HTTP Request Parsing
- [x] Request Buffering
- [x] Partial TCP Reads
- [x] Multiple HTTP Requests in One TCP Read
- [x] HTTP/1.1 Persistent Connections
- [x] Persistent Connection Server Loop
- [x] HTTP/1.1 Pipelining & Ordering

### TLS / HTTPS

- [x] TLS Fundamentals
- [x] TLS Handshake
- [x] TLS Certificate Chain
- [x] ECDHE Key Exchange
- [x] TLS Key Schedule
- [x] TLS Digital Signatures
- [x] HTTP Through TLS
- [x] Complete HTTPS / TLS 1.3 Flow
- [x] Inspecting HTTPS with Python

### HTTP Evolution

- [ ] HTTP/1.1 Internals
- [ ] HTTP/1.1 Limitations
- [ ] HTTP/2 Fundamentals
- [ ] HTTP/2 Frames
- [ ] HTTP/2 Streams
- [ ] HTTP/2 Multiplexing
- [ ] HTTP/2 Head-of-Line Blocking
- [ ] QUIC Fundamentals
- [ ] QUIC Streams
- [ ] QUIC Reliability
- [ ] QUIC vs TCP
- [ ] HTTP/3 Fundamentals
- [ ] HTTP/1.1 vs HTTP/2 vs HTTP/3

### Higher-Level HTTP

- [ ] Sessions
- [ ] JWT
- [ ] Caching
- [ ] Compression
- [ ] WebSockets

---

## Module 03 — Linux

- [ ] Linux Architecture
- [ ] Processes
- [ ] Threads
- [ ] Scheduling
- [ ] Memory
- [ ] File Systems
- [ ] Permissions
- [ ] Signals
- [ ] Services
- [ ] Networking Tools

---

## Module 04 — APIs

- [ ] REST
- [ ] GraphQL
- [ ] gRPC
- [ ] Authentication
- [ ] Authorization
- [ ] OAuth
- [ ] API Gateway
- [ ] Rate Limiting
- [ ] Circuit Breakers

---

## Module 05 — Reverse Proxy

- [ ] Forward Proxy
- [ ] Reverse Proxy
- [ ] NGINX
- [ ] Load Balancing
- [ ] SSL Termination
- [ ] Routing
- [ ] Health Checks

---

## Module 06 — Docker

- [ ] Why Containers?
- [ ] Images
- [ ] Layers
- [ ] Dockerfile
- [ ] Namespaces
- [ ] cgroups
- [ ] Volumes
- [ ] Networks
- [ ] Docker Compose

---

## Module 07 — Kubernetes

- [ ] Kubernetes Architecture
- [ ] Pods
- [ ] ReplicaSets
- [ ] Deployments
- [ ] Services
- [ ] Ingress
- [ ] ConfigMaps
- [ ] Secrets
- [ ] Persistent Volumes
- [ ] Autoscaling
- [ ] Scheduling

---

## Module 08 — Service Communication

- [ ] Service Discovery
- [ ] Internal DNS
- [ ] API Gateway
- [ ] Sidecars
- [ ] Envoy
- [ ] Service Mesh
- [ ] Istio
- [ ] mTLS

---

## Module 09 — Databases

- [ ] Database Fundamentals
- [ ] Indexing
- [ ] Transactions
- [ ] Isolation Levels
- [ ] Replication
- [ ] Sharding
- [ ] Connection Pooling
- [ ] Redis

---

## Module 10 — Messaging

- [ ] Why Messaging?
- [ ] RabbitMQ
- [ ] Kafka
- [ ] Event-Driven Architecture
- [ ] Dead Letter Queues
- [ ] Saga Pattern

---

## Module 11 — Observability

- [ ] Logging
- [ ] Metrics
- [ ] Tracing
- [ ] Health Checks
- [ ] Prometheus
- [ ] Grafana
- [ ] OpenTelemetry
- [ ] Jaeger

---

## Module 12 — Production Systems

- [ ] CI/CD
- [ ] Blue-Green Deployment
- [ ] Canary Deployment
- [ ] Feature Flags
- [ ] CDN
- [ ] Infrastructure as Code
- [ ] Cloud Architecture
- [ ] Disaster Recovery
- [ ] Security Fundamentals
- [ ] Cost Optimization