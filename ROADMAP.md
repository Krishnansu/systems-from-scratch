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

- [x] HTTP/1.1 Internals
- [x] HTTP/1.1 Limitations
- [x] HTTP/2 Fundamentals
- [x] HTTP/2 Frames
- [x] HTTP/2 Streams
- [x] HTTP/2 Multiplexing
- [x] HTTP/2 Head-of-Line Blocking
- [x] QUIC Fundamentals
- [x] QUIC Streams
- [x] QUIC Reliability
- [x] QUIC vs TCP
- [x] HTTP/3 Fundamentals
- [x] HTTP/1.1 vs HTTP/2 vs HTTP/3

### Higher-Level HTTP

- [x] Sessions
- [x] JWT
- [x] Caching
- [x] Compression
- [x] WebSockets

---

## Module 03 — Linux

- [x] Linux Architecture
- [x] Processes
- [x] Threads
- [x] Scheduling
- [x] Memory
- [x] File Systems
- [x] Permissions
- [x] Signals
- [x] Services
- [x] Networking Tools

---

## Module 04 — APIs

- [x] REST
- [x] GraphQL
- [x] gRPC
- [x] Authentication
- [x] Authorization
- [x] OAuth
- [x] API Gateway
- [x] Rate Limiting
- [x] Circuit Breakers

---

## Module 05 — Reverse Proxy

- [x] Forward Proxy
- [x] Reverse Proxy
- [x] NGINX
- [x] Load Balancing
- [x] SSL Termination
- [x] Routing
- [x] Health 
- [x] Firewall 
- [x] VPN

---

## Module 06 — Docker

- [x] Why Containers?
- [x] Images
- [x] Layers
- [x] Dockerfile
- [x] Namespaces
- [x] cgroups
- [x] Volumes
- [x] Networks
- [x] Docker Compose

---

## Module 07 — Kubernetes

- [x] Kubernetes Architecture
- [x] Pods
- [x] ReplicaSets
- [x] Deployments
- [x] Services
- [x] Ingress
- [x] ConfigMaps
- [x] Secrets
- [x] Persistent Volumes
- [x] Autoscaling
- [x] Scheduling
- [x] Health Checks and Probes
- [x] Kubernetes Workload Types
- [x] Resource Management, QoS, and Eviction
- [x] Kubernetes Security: RBAC, Workload Identity, and Network Policies
- [x] End-to-End Kubernetes Troubleshooting Lab

---

## Module 08 — Service Communication

- [x] Service Discovery
- [x] Internal DNS
- [x] API Gateway
- [x] Sidecars
- [x] Envoy
- [x] Service Mesh
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
- [ ] Production DNS and Global Traffic Management (CNAMEs, Endpoint management, GSLB, Regional Failover)
- [ ] Infrastructure as Code
- [ ] Cloud Architecture
- [ ] Disaster Recovery
- [ ] Security Fundamentals
- [ ] Cost Optimization