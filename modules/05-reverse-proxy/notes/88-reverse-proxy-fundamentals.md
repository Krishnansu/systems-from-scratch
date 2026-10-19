# Lesson 88 — Reverse Proxy Fundamentals

## Objectives
- Explain why reverse proxies exist and where they sit in a system.
- Trace requests between clients, proxies, and backend services.
- Distinguish reverse proxies, forward proxies, load balancers, and API gateways.
- Understand TLS termination, forwarded headers, and backend protection.

## Prerequisites
- DNS, TCP, HTTP, and TLS/HTTPS
- Lesson 86 — API Gateway Fundamentals
- Lesson 87 — Forward Proxy Fundamentals

## Theory
A reverse proxy accepts requests on behalf of backend servers and forwards them to the appropriate destination. Clients normally connect to the proxy's public endpoint rather than directly to individual backends.

```text
Client → Reverse Proxy → Backend Service → Response
```

Common capabilities include host/path routing, TLS termination, load balancing, connection management, caching, and reducing direct backend exposure.

## Real World Example
An online store exposes `shop.example.com`. Requests under `/products` go to the product service, while `/orders` goes to the order service. Clients use one public endpoint without needing to know the internal service addresses.

## Deep Dive
- Reverse proxies represent the server side; forward proxies represent clients.
- Routing selects a service. Load balancing can select an instance of that service.
- An API gateway is commonly a reverse-proxy-based entry point with additional API-oriented policies.
- TLS termination decrypts client HTTPS at the proxy. The proxy-to-backend connection may still need HTTPS.
- Private backend addresses and firewall rules reduce direct exposure, but do not replace application authorization.
- Forwarding headers such as `X-Forwarded-For` and `X-Forwarded-Proto` must be sanitized and trusted only from known proxies.
- Production concerns include redundancy, timeouts, health checks, connection limits, observability, and safe retry behavior.

## Hands-on Exercise
1. Design routing rules for `/api/*` and `/images/*`.
2. Explain what happens if one backend fails while another remains healthy.
3. Identify where traffic is encrypted when TLS terminates at the proxy.
4. Explain why a backend must not blindly trust client-supplied forwarding headers.
5. Describe the impact of the reverse-proxy tier becoming unavailable.

## Common Misconceptions
- A reverse proxy does not have to load-balance; it can forward to one backend.
- An API gateway and a reverse proxy have overlapping capabilities but are not identical concepts.
- A reverse proxy is not a replacement for firewalls or backend authorization.
- HTTPS from the browser does not guarantee encryption on the internal network hop.
- The backend does not automatically know the original client IP address.

## Summary
A reverse proxy provides a controlled entry point for incoming traffic and forwards requests to backend services. It can route requests, terminate TLS, distribute traffic, and reduce direct backend exposure. Secure and reliable deployments also require appropriate network controls, authorization, trusted-header handling, monitoring, and redundancy.

## Key Takeaways
- A reverse proxy fronts servers; a forward proxy represents clients.
- Service routing and instance-level load balancing are distinct decisions.
- TLS termination defines where the client-facing encrypted connection ends.
- Reverse proxies complement, rather than replace, firewall and application security.
- Proxy availability and failure behavior are production design concerns.

## Reflection Questions
1. Why put a reverse proxy in front of backend services?
2. How is routing different from load balancing?
3. What changes when TLS terminates at the proxy?
4. Why is backend authorization still necessary?
5. How should a system respond to a backend failure versus a proxy-tier failure?

## What's Next
Lesson 89 — NGINX Fundamentals: apply reverse-proxy concepts using a widely used server and its configuration model.
