# Lesson 87 — Forward Proxy Fundamentals

## Objectives
- Explain why forward proxies exist and where they sit in a network.
- Trace HTTP and HTTPS requests through a forward proxy.
- Distinguish forward proxies from reverse proxies, NAT, and VPNs.
- Understand proxy access policies, security boundaries, and failure behavior.

## Prerequisites
- Networking fundamentals: IP addressing, routing, and NAT
- DNS, HTTP, and TLS/HTTPS
- Lesson 86 — API Gateway Fundamentals

## Theory
A forward proxy acts on behalf of clients when they access external destinations. It provides a controlled point for outbound access policies, authentication, auditing, and sometimes caching.

Common uses include corporate web access control, egress restrictions, centralized auditing, and reuse of eligible cached responses. Clients typically use an explicitly configured proxy or managed proxy settings. Network policy may be needed to prevent direct-connect bypasses.

### Request paths
- HTTP: Client → Forward Proxy → Destination Server
- HTTPS: Client → Proxy using CONNECT → TLS session through tunnel → Destination Server

An HTTP proxy can inspect application-level request details available to it. A normal HTTPS CONNECT tunnel exposes the requested host and port plus connection metadata, but does not automatically reveal the encrypted HTTP path or body.

## Real World Example
A company routes employee browser traffic through a managed forward proxy. The proxy authenticates users, applies destination policies, logs approved activity, and forwards allowed requests. The destination generally sees the proxy's outbound network address rather than the employee laptop's address.

## Deep Dive
- A forward proxy represents clients; a reverse proxy fronts servers.
- HTTP proxies can understand HTTP methods, destinations, and headers available to them.
- HTTPS commonly uses CONNECT to establish a tunnel; TLS normally remains between client and destination unless managed TLS interception is configured.
- NAT translates network addresses; it does not inherently parse HTTP URLs or methods.
- A VPN typically tunnels IP traffic more broadly, while an HTTP proxy handles configured application traffic.
- Explicit proxy configuration alone does not guarantee all traffic uses the proxy. Egress firewall rules can enforce the boundary.
- Proxy authentication and destination policy are distinct from authorization inside the destination application.
- An exposed open proxy can be abused. Production deployments need access controls, careful logging, monitoring, capacity planning, and redundancy.
- Fail-open behavior may preserve connectivity but bypass policy; fail-closed behavior preserves the boundary but can interrupt access.

## Hands-on Exercise
1. Trace an HTTP request from a browser through a forward proxy to a destination.
2. Explain the purpose of CONNECT when the destination uses HTTPS.
3. If you have an authorized test proxy, compare direct and proxied requests using `curl -v` and `curl -v -x http://proxy.example:8080 https://example.com/`.
4. Identify which controls belong at the proxy and which belong inside the destination application.
5. Compare fail-open and fail-closed behavior during a proxy outage.

## Common Misconceptions
- Forward and reverse proxies serve different architectural roles.
- A forward proxy is not the same as NAT or a VPN.
- HTTPS tunneling does not automatically decrypt application traffic.
- Configuring a browser proxy does not prevent every other application from bypassing it.
- Proxy access approval does not grant permission to every resource at the destination.
- Centralizing outbound traffic does not remove the need for availability and security design.

## Summary
A forward proxy acts on behalf of clients for outbound requests and provides a centralized point for access policy, auditing, and caching. HTTP proxies can inspect request details, while HTTPS commonly uses CONNECT to tunnel a client-to-destination TLS session. Proxies differ from reverse proxies, NAT, and VPNs by purpose and behavior. Production use requires secure configuration, resilient deployment, and deliberate bypass policies.

## Key Takeaways
- Forward proxies represent clients; reverse proxies represent server-side services.
- CONNECT commonly establishes a tunnel for HTTPS traffic.
- NAT, VPNs, and forward proxies solve related but different problems.
- Firewall and egress controls may be needed to prevent proxy bypass.
- Authentication, destination policy, and application authorization are separate concerns.
- Failure behavior should reflect the security and availability requirements.

## Reflection Questions
1. Why might an organization require employee web traffic to pass through a forward proxy?
2. What does CONNECT accomplish for an HTTPS destination?
3. How does a forward proxy differ from NAT if both can share an outbound IP address?
4. Why combine proxy configuration with firewall rules?
5. What are the trade-offs between fail-open and fail-closed proxy behavior?

## What's Next
Lesson 88 — Reverse Proxy Fundamentals: how reverse proxies front backend services, route incoming requests, and protect server-side infrastructure.
