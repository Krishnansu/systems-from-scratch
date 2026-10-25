# Lesson 124 — Sidecars

## Objectives

- Explain the sidecar pattern and why it exists.
- Compare sidecars with libraries, node agents, gateways, and init containers.
- Understand sidecars in Kubernetes Pods.
- Evaluate sidecar benefits, costs, and failure modes.
- Connect sidecars to proxies and service meshes.

## Prerequisites

- Linux processes and networking
- Docker containers and network namespaces
- Kubernetes Pods and Services
- Lessons 121–123: Service Discovery, Internal DNS, API Gateway

## Concept Summary

A sidecar is a helper process deployed alongside a primary application workload. It can provide cross-cutting capabilities such as traffic proxying, telemetry, logging, or security without embedding all such functionality in application code.

## Core Ideas

- Sidecars are separate processes, not libraries loaded into the application.
- Communication can use localhost, traffic interception, local APIs, or explicitly shared volumes; implementations differ.
- In Kubernetes, application and sidecar containers commonly run in one Pod.
- Containers in a Pod share the Pod network namespace and IP; they can communicate over localhost. They do not automatically share filesystems or process memory.
- Volumes are shared only when configured and mounted into the relevant containers.
- Native Kubernetes sidecars can be declared as init containers with `restartPolicy: Always`; they continue running alongside the application.
- Sidecars can standardize infrastructure capabilities, but add CPU/memory use, latency, configuration, lifecycle complexity, and failure modes.

## Comparisons

- **Library:** in-process calls; usually tied to the app's language/runtime.
- **Sidecar:** separate helper process associated with a workload.
- **Node agent:** often runs once per node and serves multiple workloads.
- **Init container:** ordinarily completes before application containers start; native sidecars use different lifecycle semantics.
- **Service mesh:** a fleet-level communication system; sidecars may be one component, not the whole mesh.

## Production Perspective

- A sidecar failure can interrupt requests if the application depends on it.
- Extra processes require resource sizing, probes, observability, upgrades, and shutdown planning.
- Multiple containers do not automatically imply a sidecar architecture; determine each container's role.
- Sidecars do not replace service discovery, DNS, or application-level correctness.

## Hands-on Exercise

Use the [Lesson 124 command reference](../commands/124-sidecars.md) to inspect an existing authorized Pod. Identify containers, init containers, volumes, resource limits, probes, and restart counts. Do not modify shared workloads.

## Common Misconceptions

- A sidecar is always a proxy.
- Containers in one Pod have completely separate networking.
- Every sidecar intercepts all traffic automatically.
- Process separation guarantees failure isolation.
- A sidecar alone is a service mesh.

## Key Takeaways

- Sidecars separate selected supporting capabilities from application code.
- Kubernetes Pods provide shared networking and coordinated placement, not automatic shared filesystems or memory.
- Sidecars are useful but add operational and resource costs.
- Envoy is a proxy commonly used in sidecar-based architectures.

## Reflection Questions

1. Why might a platform team choose a sidecar for telemetry or traffic policies?
2. What do containers in the same Pod share, and what do they not automatically share?
3. Why can a sidecar failure affect application availability?
4. How does a sidecar differ from a node agent and an init container?
5. Why is a sidecar not, by itself, a service mesh?

## What's Next

Lesson 125 — Envoy.
