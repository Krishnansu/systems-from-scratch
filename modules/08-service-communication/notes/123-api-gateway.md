# Lesson 123 — API Gateway

## Objectives

- Explain the API Gateway's role as a client-facing entry point.
- Trace requests through routing and gateway policies.
- Understand authentication, rate limiting, TLS termination, transformation, and aggregation.
- Compare gateways with load balancers, reverse proxies, Ingress, and service meshes.
- Reason about timeouts, retries, availability, and security boundaries.

## Prerequisites

- HTTP fundamentals and authentication/authorization
- Reverse proxies and load balancing
- Lessons 121–122: Service Discovery and Internal DNS

## Concept Summary

An API Gateway accepts client API requests and applies configured routing and policies before forwarding requests to backend services. It provides a stable API-facing boundary while backend services can evolve independently.

## Core Ideas

- **Routing:** map paths, hosts, methods, headers, or versions to backend services.
- **Authentication and authorization:** validate identity and apply access policies. Backend services may still need resource-level authorization.
- **Rate limiting:** control request volume; distributed counters trade consistency against latency and dependency cost.
- **TLS termination:** handle client-facing TLS. Backend traffic may also require encryption.
- **Transformation:** rewrite paths or headers and enforce request policies.
- **Aggregation:** optionally combine multiple backend responses; this adds latency and dependency coupling.
- **Discovery:** the gateway still needs a way to locate upstream services. DNS and service discovery are separate from API routing policy.

## Request Flow

```text
Client
  → API Gateway
      → configured policies
      → route selection
      → upstream service
      → response processing
  ← Client
```

Exact policy order and supported features depend on the implementation.

## Production Perspective

- A gateway timeout does not prove a state-changing operation failed; the backend may have committed the operation before the response was lost.
- Retries should be bounded and account for idempotency, deadlines, and ambiguous outcomes.
- Gateways need redundancy, capacity planning, monitoring, secure configuration, and resilient upstream handling.
- Useful signals include request rate, error rate, latency percentiles, upstream timeouts, rejected requests, and trace identifiers.

## Related Components

- **Load balancer:** distributes traffic across targets.
- **Reverse proxy:** forwards requests on behalf of upstream servers; gateway products often use this architecture.
- **Kubernetes Ingress:** API resource for HTTP(S) routing, implemented by an Ingress controller; not automatically a complete API Gateway.
- **Service mesh:** primarily manages service-to-service communication, often called east-west traffic. Gateways commonly handle north-south traffic.

## Common Misconceptions

- An API Gateway is not merely DNS or a load balancer.
- A valid token does not prove ownership of a particular resource.
- A 504 does not prove the backend did not execute the request.
- A gateway does not eliminate service discovery or backend health checks.
- Retrying every failure can duplicate side effects or amplify overload.

## Key Takeaways

- The gateway is a client-facing API boundary with configured routing and policy enforcement.
- Gateway features vary by product and configuration.
- Keep business authorization and correctness in the appropriate backend layer.
- Treat timeouts and retries as distributed-systems problems.
- Operate the gateway as a critical production dependency.

## Reflection Questions

1. What problem does an API Gateway solve that internal DNS alone cannot solve?
2. Why might a valid token be insufficient to authorize access to a particular order?
3. What can go wrong if a gateway automatically retries every failed POST?
4. How does a gateway differ from a load balancer?
5. Why does a 504 during order creation not prove the order was not created?

## What's Next

Lesson 124 — Sidecars.
