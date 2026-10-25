# Lesson 126 — Service Mesh

## Objectives

- Explain why a service mesh exists and which problems it solves.
- Distinguish its data plane and control plane.
- Compare a service mesh with service discovery, an API gateway, a sidecar, and Envoy.
- Understand traffic management, workload identity, security policy, and telemetry.
- Recognize mesh trade-offs and failure modes.

## Prerequisites

- Lesson 121 — Service Discovery
- Lesson 122 — Internal DNS
- Lesson 123 — API Gateway
- Lesson 124 — Sidecars
- Lesson 125 — Envoy

## Concept Summary

A service mesh is an infrastructure layer for managing service-to-service communication across workloads. It coordinates proxies and configuration to provide capabilities such as traffic management, workload identity, security policy, and telemetry. Exact capabilities and defaults depend on the implementation and configuration.

## Core Ideas

- **Data plane:** proxies that handle live service traffic and apply configured behavior.
- **Control plane:** manages or distributes proxy configuration, policies, and identity-related settings.
- **Traffic management:** may include routing, load balancing, timeouts, retries, and circuit-breaking behavior.
- **Workload identity and security:** can authenticate workloads, encrypt connections, and enforce communication policies. Encryption, authentication, and authorization are distinct concerns.
- **Observability:** proxies can emit communication metrics, access logs, and tracing data when configured.
- **Proxy placement:** sidecars are common, but node-level or ambient-style architectures also exist.

## Request Flow

```text
Checkout application
  -> Checkout outbound proxy
  -> Network connection
  -> Inventory inbound proxy
  -> Inventory application
  -> Response through the relevant path
```

The control plane configures proxies; it normally does not forward every live request. A mesh still depends on networking, endpoint discovery, correct proxy configuration, and healthy applications.

## Related Concepts

- Service discovery finds service instances or endpoints.
- Internal DNS resolves names to addresses or service records.
- An API gateway manages client-facing API traffic; a mesh commonly manages service-to-service traffic.
- A sidecar is a deployment pattern.
- Envoy is proxy software that can be a mesh data-plane component.
- A service mesh coordinates communication behavior across a fleet.

## Production Perspective

- Existing traffic may continue with the last accepted configuration during a control-plane outage, while updates or identity refreshes may be delayed; behavior depends on the implementation.
- A successful configuration submission does not guarantee every proxy has applied it.
- Retries can amplify overload or duplicate side effects; use appropriate deadlines, limits, and idempotency protections.
- Proxy telemetry complements application-level metrics and logs; it does not explain every business failure.
- Meshes add resource consumption, latency, configuration, security, and operational complexity.
- A mesh does not automatically fix DNS, network policy, endpoint, or application-health problems.

## Hands-on Exercise

Use the [Lesson 126 command reference](../commands/126-service-mesh.md) for safe, read-only inspection of authorized Kubernetes workloads. Identify application and proxy containers where applicable, then trace a hypothetical service-call failure through discovery, networking, proxy configuration, security policy, destination proxy, and application behavior.

## Common Misconceptions

- A service mesh is more than a collection of proxies.
- The control plane is not normally in the live request path.
- A mesh does not eliminate service discovery or application observability.
- mTLS does not replace authorization.
- Not every mesh uses a sidecar per workload.
- Installing a mesh does not guarantee reachability or application health.

## Key Takeaways

- The data plane handles traffic; the control plane manages configuration and coordination.
- A mesh can standardize communication behavior across services.
- Security, traffic management, and telemetry are distinct capabilities that require appropriate configuration.
- A mesh is an architectural trade-off, not a universal requirement.

## Reflection Questions

1. Why is a service mesh more than a collection of Envoy proxies?
2. Why might traffic continue during a control-plane outage while configuration updates stop?
3. How can an API gateway and service mesh complement each other?
4. Why are workload authentication, authorization, and encryption distinct?
5. How would you troubleshoot a timeout after a request reaches the destination proxy?

## What's Next

Lesson 127 — Istio.
