# Lesson 109 — Kubernetes Services

## Objectives

- Explain why Services are needed when Pod identities and IP addresses change.
- Understand how selectors and EndpointSlices connect a Service to eligible Pods.
- Distinguish `port`, `targetPort`, and `nodePort`.
- Compare ClusterIP, NodePort, LoadBalancer, and headless Services.
- Explain Service DNS resolution and how traffic reaches a backend Pod.
- Troubleshoot Services with read-only Kubernetes commands.

## Prerequisites

- Lesson 106 — Pods
- Lesson 107 — ReplicaSets
- Lesson 108 — Deployments

## Theory

### 1. Why Services?

Pods are replaceable workload instances. A replacement Pod can have a different IP address, so clients should not depend on an individual Pod IP. A Service provides a stable network endpoint for a logical group of backend Pods.

### 2. Selectors and EndpointSlices

A typical Service selector matches labels on Pods. Kubernetes tracks backend endpoint information through EndpointSlices, including endpoint addresses and conditions. A Service normally selects Pods, not Deployments or ReplicaSets directly.

During a Deployment rollout, old and new ReplicaSets can have Pods with the same labels. Both versions may therefore be selected by the same Service while the rollout progresses. Traffic eligibility depends on endpoint conditions and the cluster's networking behavior; a Pod merely existing does not prove it is Ready or serving traffic.

### 3. Service ports

- `port`: the port exposed by the Service.
- `targetPort`: the backend Pod port to which traffic is directed; the application must listen on that port.
- `nodePort`: the port exposed on cluster nodes by a NodePort Service.

Example:

```yaml
apiVersion: v1
kind: Service
metadata:
  name: orders-api
spec:
  selector:
    app: orders-api
  ports:
    - port: 80
      targetPort: 8080
  type: ClusterIP
```

Clients use Service port 80; traffic is directed to eligible backend Pods on port 8080.

### 4. Service types

- **ClusterIP:** default type; provides a stable virtual IP for access through cluster networking.
- **NodePort:** exposes the Service on a port on each eligible node, subject to cluster networking and firewall rules.
- **LoadBalancer:** requests integration with an external load-balancing implementation, where supported.
- **Headless Service:** uses `clusterIP: None`; DNS can return backend Pod addresses rather than a single ClusterIP.

ClusterIP is not restricted to clients in the same namespace. For a Service named `orders-api` in namespace `sales`, a client can typically use `orders-api.sales` or the fully qualified name `orders-api.sales.svc.cluster.local`. The cluster DNS domain can vary, and network policies or other restrictions may limit reachability.

### 5. DNS and traffic routing

Cluster DNS resolves a normal Service name to its Service IP. DNS resolution does not choose a backend for each HTTP request. The cluster's Service networking data plane directs traffic to eligible endpoints. Depending on the implementation, this may be programmed by kube-proxy using iptables or IPVS, or handled by another networking implementation.

Backend selection commonly operates at the network-flow or connection level, not independently for every HTTP request. Multiple HTTP requests that reuse one TCP connection normally continue to use the same backend connection. New connections may reach different endpoints, but even distribution is not guaranteed.

## Real World Example

An Orders API has several Pods managed by a Deployment. The Pods can be replaced during failures or rollouts, changing their IP addresses. A ClusterIP Service named `orders-api` selects Pods labeled `app: orders-api`. Other applications connect to the Service rather than tracking individual Pod addresses. As eligible endpoints change, Kubernetes networking directs new connections toward the available backends according to the cluster's implementation.

## Deep Dive

- **Stable Service endpoint:** clients use a logical Service address instead of tracking ephemeral Pod IPs.
- **Selector:** matches Pod labels; a mismatch can leave the Service without matching backends.
- **EndpointSlice:** represents backend endpoint addresses and conditions.
- **Readiness:** affects whether a Pod is considered eligible to receive normal Service traffic.
- **DNS:** resolves the Service name; it is distinct from backend traffic forwarding.
- **Connection reuse:** one persistent TCP connection does not generally switch backend Pods for every HTTP request.
- **Implementation differences:** Service routing details depend on the cluster networking implementation.

## Hands-on Exercise

On a cluster you are authorized to inspect, follow the read-only commands in [the Lesson 109 command reference](../commands/109-services.md). Inspect a Service, compare its selector with Pod labels, examine EndpointSlices, and identify the Service port and backend target port. If no cluster is available, trace a request to `orders-api:80` and explain how it can reach an eligible Pod on port 8080.

Do not create, delete, or modify workloads in a shared or production cluster for this introductory exercise.

## Common Misconceptions

- Pod IP addresses are not stable identities for clients to depend on.
- A Service typically selects Pods through labels; it does not directly select a Deployment.
- `port` and `targetPort` describe different sides of the Service connection.
- ClusterIP Services are not limited to clients in the same namespace.
- DNS resolution and backend traffic forwarding are separate operations.
- A Service does not guarantee a different backend for every HTTP request or perfectly even distribution.
- A Service object existing does not guarantee it has healthy, eligible endpoints.

## Summary

A Service provides a stable network endpoint for a logical set of Pods. Selectors match Pod labels, EndpointSlices describe backend endpoints, and the Service type determines how clients access the endpoint. DNS resolves Service names, while the cluster networking data plane forwards traffic to eligible backends.

## Key Takeaways

- Use Services instead of hard-coding replaceable Pod IP addresses.
- Check selectors, labels, EndpointSlices, and readiness when a Service has no working backends.
- `port` is the Service-facing port; `targetPort` is the backend Pod port.
- ClusterIP, NodePort, LoadBalancer, and headless Services provide different access models.
- DNS resolution does not itself select a Pod for each HTTP request.
- Backend selection and load distribution depend on networking behavior and connection reuse.

## Reflection Questions

1. Why is a Service useful when a Pod is replaced and receives a new IP address?
2. If a Service has `port: 80` and `targetPort: 8080`, where must the backend application listen?
3. What would you inspect if a Service has no eligible endpoints?
4. How do ClusterIP, NodePort, and LoadBalancer differ, and can a ClusterIP Service be accessed across namespaces?
5. What is the difference between resolving a Service name through DNS and routing traffic to a backend Pod?

## What's Next

Lesson 110 — Kubernetes Ingress: routing external HTTP and HTTPS traffic to Services.
