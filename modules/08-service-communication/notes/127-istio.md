# Lesson 127 — Istio

## Objectives

- Explain Istio's control plane and data plane.
- Understand Istiod, Envoy, and xDS configuration delivery.
- Distinguish key Istio traffic and security resources.
- Trace a request through a sidecar-based mesh.
- Identify safe, read-only troubleshooting commands.

## Prerequisites

- Lessons 121–126: Service Discovery, Internal DNS, API Gateway, Sidecars, Envoy, Service Mesh.

## Concept Summary

Istio implements service-mesh capabilities. Istiod processes mesh configuration and distributes proxy resources; Envoy commonly processes live traffic in the data plane. Istio also supports architectures that do not require a sidecar in every workload.

## Core Ideas

- **Istiod:** control-plane component that processes service and policy configuration and distributes proxy configuration.
- **Envoy:** data-plane proxy that applies active configuration to traffic.
- **xDS:** family of APIs used to deliver dynamic configuration resources to Envoy, including listeners, routes, clusters, and endpoints.
- **Traffic capture:** implementation-dependent mechanisms direct selected traffic through mesh proxies.
- **Gateway:** configures an Istio gateway proxy's incoming traffic behavior.
- **VirtualService:** defines request-routing rules and destination selection.
- **DestinationRule:** defines destination policies, including subsets and supported load-balancing or connection-pool behavior.
- **PeerAuthentication:** configures peer authentication behavior, including workload mTLS mode.
- **AuthorizationPolicy:** defines which requests are allowed or denied.
- **ServiceEntry:** adds services to Istio's registry that are not represented by ordinary Kubernetes service discovery.

## Request Flow

```text
Application A
  → outbound Envoy
  → mesh network
  → inbound Envoy
  → Application B
```

Istiod normally distributes configuration rather than forwarding each live request. Exact traffic capture and routing depend on deployment mode and configuration.

## Resource Distinctions

- Kubernetes Service: stable access to a set of workloads.
- Istio Gateway: configures a proxy that accepts incoming traffic.
- VirtualService: matches requests and selects destinations.
- DestinationRule: configures behavior for a destination and its subsets.
- PeerAuthentication: peer authentication and mTLS mode.
- AuthorizationPolicy: access decisions.

## Production Perspective

- Desired configuration does not prove that every proxy has synchronized or that a request will succeed.
- A valid route does not prove that the destination exists, is reachable, or is healthy.
- Inspect the first failing hop: caller proxy, route/cluster, network, destination proxy, application, or downstream dependency.
- mTLS and authorization are separate concerns; encryption and identity do not automatically grant access.
- Prefer read-only inspection and follow incident procedures before changing shared infrastructure.

## Common Misconceptions

- Istio and Envoy are not the same thing.
- Istiod is not normally in the live request path.
- A VirtualService does not create its Kubernetes Service or application workloads.
- Proxy health does not guarantee application health.
- Configuration acceptance does not prove fleet-wide synchronization.

## Key Takeaways

- Istiod translates mesh intent into proxy configuration distributed through xDS.
- Envoy proxies apply active configuration to traffic.
- Gateway, VirtualService, and DestinationRule have distinct responsibilities.
- PeerAuthentication and AuthorizationPolicy address different security decisions.
- Troubleshooting must distinguish configuration, synchronization, reachability, and application health.

## Reflection Questions

1. Why does Istio need Istiod if Envoy can proxy traffic?
2. A VirtualService routes to subset `v2`, but requests fail. What would you inspect?
3. How do a Kubernetes Service, Istio Gateway, and VirtualService differ?
4. How do PeerAuthentication and AuthorizationPolicy differ?
5. How would you diagnose timeouts affecting only some proxies after a policy change?

## What's Next

Lesson 128 — mTLS.
