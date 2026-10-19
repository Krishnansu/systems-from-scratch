# Lesson 86 — API Gateway Fundamentals

## Objectives
- Explain the role of an API Gateway in a distributed system.
- Distinguish gateway routing, load balancing, and application-level routing.
- Understand common gateway responsibilities and deployment patterns.
- Identify reliability and security concerns at the gateway boundary.

## Prerequisites
- Lesson 80 — API Rate Limiting, Quotas & Abuse Prevention
- Lesson 83 — Authentication Fundamentals
- Lesson 84 — Authorization Fundamentals
- Lesson 85 — OAuth Fundamentals

## Theory
An API Gateway provides a controlled entry point for API traffic. It routes requests to backend services and can centralize cross-cutting concerns such as TLS termination, authentication integration, rate limiting, request-size limits, API version routing, and observability.

### Common request path
Client → External Load Balancer → API Gateway → Backend Service → Application Handler

This is a common deployment pattern, not a mandatory topology. Managed gateways may hide their internal infrastructure, and a gateway may also perform reverse-proxy and load-balancing functions.

### Three distinct responsibilities
- **Gateway routing:** selects the logical backend service, often using host, path, method, or header rules.
- **Load balancing:** selects an eligible backend instance for traffic destined for a service.
- **Application routing:** the backend framework matches the HTTP request to a controller, handler, or route within the application.

In Kubernetes, gateway replicas may run in a Deployment. An external load balancer or platform entry point can distribute traffic to gateway pods. The gateway can forward to a stable Kubernetes Service name, which routes traffic to eligible backend pods. Some designs let the gateway select upstream instances directly.

## Real World Example
A store exposes `/api/users/*`, `/api/orders/*`, and `/api/payments/*`. The gateway routes these paths to the respective backend services. Each service's framework then routes requests to its own controllers. If the application is deployed as one service with multiple controllers, the gateway can route all those paths to that service without managing each controller separately.

## Deep Dive
- Gateways can route traffic across independently deployed services, while a backend framework routes requests to controllers within a service.
- One logical backend service can have many replicas. The gateway normally targets a stable service destination rather than configuring each pod separately.
- A gateway can validate access tokens and apply coarse edge policies, but the backend must still enforce resource-level authorization. A valid token does not imply permission to read a particular order.
- Identity headers must not be trusted if arbitrary clients can inject them. Strip untrusted values and accept trusted identity assertions only across controlled paths.
- Multiple gateway replicas improve availability, but the surrounding entry point and networking layers also need resilience.
- Timeouts do not prove that an upstream operation failed. Blind retries, particularly for payments, can duplicate side effects. Use correctly implemented idempotency controls and appropriate retry policies.
- Reverse proxies, load balancers, and API Gateways have overlapping capabilities. A dedicated gateway is useful when its API-specific policies justify the added complexity.

## Hands-on Exercise
For an online store exposing product, order, and payment endpoints:
1. Map each public route to a backend service.
2. Identify which controls belong at the gateway and which checks must remain in the backend.
3. Trace a request from the public entry point to a controller and database.
4. Explain what happens if a payment succeeds but the gateway times out before receiving the response.
5. Describe how networking and service authentication can prevent gateway bypass.

## Common Misconceptions
- The API Gateway does not normally replace the backend framework's controller routing.
- A gateway and a load balancer are related but not identical architectural roles.
- Every deployment does not require two separate load balancers.
- Gateway token validation does not replace resource-level authorization.
- A timeout does not prove that an operation failed.
- A gateway improves control and consistency only when its policies and deployment are configured correctly.

## Summary
An API Gateway provides a stable API-facing entry point and centralizes selected edge policies. Gateway routing selects a backend service, load balancing selects an instance, and application routing selects a handler. Production designs must account for availability, secure trust boundaries, and safe handling of timeouts and retries.

## Key Takeaways
- Separate gateway routing, instance selection, and controller routing mentally.
- Gateways commonly run as highly available tiers, often with multiple replicas.
- A Kubernetes Service can provide a stable destination for backend replicas.
- Backend services remain responsible for business rules and resource-level authorization.
- Retrying writes requires careful handling of idempotency and uncertain outcomes.

## Reflection Questions
1. Why use an API Gateway instead of exposing every backend service directly to clients?
2. Why is checking an access token at the gateway insufficient to authorize access to a specific order?
3. How can a gateway be both a reliability improvement and a potential single point of failure?
4. Why can automatically retrying a timed-out payment request be dangerous?
5. When might you use a reverse proxy or load balancer without introducing a dedicated API Gateway?

## What's Next
Lesson 87 — Forward Proxy Fundamentals: how forward proxies work, where they sit in a network, and how they differ from reverse proxies.
