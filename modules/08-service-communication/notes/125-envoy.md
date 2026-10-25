# Lesson 125 — Envoy

## Objectives

- Explain Envoy's role as a configurable L4/L7 proxy.
- Trace traffic through listeners, filters, routes, clusters, and endpoints.
- Distinguish static from dynamic configuration.
- Understand upstream selection, health checks, load balancing, and retry trade-offs.
- Distinguish Envoy from a sidecar pattern and a service mesh.

## Prerequisites

- Reverse proxies and load balancing
- Service discovery and internal DNS
- Lesson 124 — Sidecars

## Concept Summary

Envoy is a high-performance proxy that accepts connections, processes traffic through configured filters, and forwards traffic to upstream destinations. It can run at the edge or alongside an application as a sidecar.

## Core Ideas

- **Listener:** address and port where Envoy accepts connections.
- **Filter chain:** selects the connection-processing path using configured match criteria.
- **Filters:** process traffic; examples include TCP proxy, HTTP connection manager, and HTTP router filters.
- **Route:** matches HTTP request attributes and selects a logical upstream.
- **Cluster:** describes an upstream group and connection/load-balancing behavior.
- **Endpoint:** concrete upstream host and port.
- **Static configuration:** resources supplied in configuration.
- **Dynamic configuration:** resources delivered by a management server through xDS APIs.

## Request Flow

```text
Incoming connection
  → Listener
  → Filter chain and filters
  → HTTP route selection (when using HTTP routing)
  → Upstream cluster
  → Selected endpoint
  → Response through proxy
```

L4 TCP proxying does not inherently understand HTTP paths. Exact processing depends on configured filters and protocols.

## Production Perspective

- Load balancing, health checking, timeouts, and retries are distinct behaviors; inspect active configuration rather than assuming they are enabled.
- A route match does not guarantee that the upstream is reachable or that the application succeeds.
- Retries can duplicate state-changing operations or amplify overload; consider idempotency, deadlines, and retry budgets.
- Envoy's control plane can distribute configuration, while Envoy proxies process data-plane traffic.
- Envoy may be a service-mesh data-plane component, but Envoy alone is not a complete service mesh.

## Common Misconceptions

- A cluster is not necessarily one server.
- Routes and service discovery are not the same thing.
- Envoy does not automatically intercept all traffic or enable every feature.
- A sidecar is a deployment pattern; Envoy is proxy software.

## Hands-on Exercise

Trace the illustrative configuration in [the Lesson 125 command reference](../commands/125-envoy.md). Identify the listener, HTTP connection manager, route, cluster, and endpoint. If Envoy is installed locally, validate a local configuration without restarting or modifying shared infrastructure.

## Key Takeaways

- Remember the HTTP proxy model: listener → filters → route → cluster → endpoint.
- Routes select logical destinations; clusters describe upstream behavior and endpoints identify concrete destinations.
- Static and dynamic configuration are different ways to provide proxy resources.
- Proxy capabilities depend on configuration and deployment architecture.

## Reflection Questions

1. What is the difference between a route, a cluster, and an endpoint?
2. Why might a TCP proxy not route by HTTP path?
3. What belongs to the data plane versus the control plane?
4. Why doesn't a successful route match guarantee upstream success?
5. What risks arise from automatic retries on state-changing requests?

## What's Next

Lesson 126 — Service Mesh.
