# Lesson 121 — Service Discovery

## Objectives

- Explain why distributed services need discovery.
- Compare client-side and server-side discovery.
- Distinguish registration, discovery, health assessment, and load balancing.
- Explain how Kubernetes Services and DNS provide service discovery.
- Diagnose common discovery-related failures.

## Prerequisites

- Lesson 109 — Kubernetes Services
- Lesson 120 — End-to-End Kubernetes Troubleshooting Lab

## Theory

### Why discovery?

Service instances are replaceable: scaling, restarts, deployments, and infrastructure changes can alter their addresses. Hardcoding instance IPs couples callers to ephemeral destinations. Service discovery maps a logical service identity to endpoint information that callers or routing infrastructure can use.

### Discovery architectures

- **Client-side discovery:** the client obtains endpoint information and chooses an instance. This permits application-specific selection but distributes selection, caching, and failure-handling logic across clients.
- **Server-side discovery:** the client calls a stable endpoint; a router or load balancer selects a backend. Clients are simpler, but routing infrastructure becomes an important dependency.
- Systems can combine both patterns.

### Service registry and related responsibilities

A service registry stores or exposes information about service instances. Registration makes an instance known; discovery retrieves endpoint information; health assessment determines whether an endpoint appears eligible; load balancing chooses or distributes traffic among candidates. These are related but distinct responsibilities.

Registries can become stale after unexpected failures. Leases, heartbeats, health checks, expiration, and reconciliation help maintain endpoint freshness. Cached information improves efficiency but creates freshness trade-offs.

### Kubernetes example

A client in namespace `store` can typically call `inventory` by its short Service name, or use `inventory.store.svc.cluster.local` when the cluster domain is `cluster.local` (the domain can vary).

For a normal ClusterIP Service:

1. The client resolves the logical Service name through cluster DNS.
2. DNS typically returns the Service virtual IP.
3. Cluster networking forwards traffic to an eligible backend endpoint.
4. The backend Pod handles the connection and request.

A headless Service (`clusterIP: None`) can publish endpoint addresses through DNS. DNS resolution and traffic forwarding remain separate operations.

### Production considerations

- Discovery data may be stale or propagate with delay.
- Successful name resolution does not guarantee connectivity or application health.
- Clients still need timeouts and appropriate error handling.
- Retries must account for idempotency and ambiguous outcomes.
- A registry, DNS system, or routing layer can itself become a dependency that needs monitoring and reliable operation.

## Real World Example

Checkout calls the logical `inventory-service` rather than storing each inventory Pod's IP. The discovery mechanism exposes current endpoints; client-side logic or a routing layer directs traffic to a suitable instance. When instances change, endpoint information is updated without requiring every caller to hardcode new addresses.

## Deep Dive

- **Discovery:** find destinations for a logical service.
- **Registration:** publish an instance to the discovery mechanism.
- **Health assessment:** estimate whether an instance should receive traffic.
- **Load balancing:** select or distribute traffic among candidates.
- **Client-side:** client selects from discovered endpoints.
- **Server-side:** router or load balancer selects the backend.
- **Kubernetes:** Service state, DNS, endpoint data, and networking cooperate; none alone guarantees successful requests.

## Hands-on Exercise

On a cluster you are authorized to inspect, use the read-only commands in [the Lesson 121 command reference](../commands/121-service-discovery.md). Pick a Service, identify its namespace and DNS name, inspect its EndpointSlices, and distinguish name resolution from backend forwarding. Do not modify shared or production resources for this exercise.

## Common Misconceptions

- Service discovery is not synonymous with DNS.
- A service registry is not necessarily queried for every request.
- Discovery does not guarantee a destination is healthy or reachable.
- Discovery and load balancing are different responsibilities.
- A resolved Kubernetes Service name does not prove that its backends are reachable.

## Summary

Service discovery decouples callers from changing instance addresses. Clients may select from discovered endpoints, or a stable routing layer may select backends. In Kubernetes, Service names, DNS, endpoint information, and cluster networking cooperate to provide stable service communication.

## Key Takeaways

- Prefer logical service identities over hardcoded instance addresses.
- Separate registration, discovery, health assessment, and load balancing.
- Understand who selects the backend in client-side and server-side designs.
- In Kubernetes, DNS resolution and traffic forwarding are distinct stages.
- Debug discovery failures by checking names, endpoint state, ports, routing, policies, and application health in order.

## Reflection Questions

1. Why is hardcoding an instance IP fragile?
2. How do client-side and server-side discovery differ?
3. Why can registry data become stale?
4. How do Kubernetes Service DNS resolution and backend forwarding differ?
5. What would you investigate if DNS resolves but requests time out?

## What's Next

Lesson 122 — Internal DNS.
