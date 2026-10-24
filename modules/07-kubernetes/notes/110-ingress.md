# Lesson 110 — Kubernetes Ingress

## Objectives

- Explain why Ingress is useful for external HTTP/HTTPS routing.
- Distinguish an Ingress resource from an Ingress controller.
- Understand host-based and path-based routing.
- Trace traffic from an external entry point to a backend Service and Pod.
- Understand IngressClass, TLS configuration, and common failure modes.

## Prerequisites

- Lesson 106 — Pods
- Lesson 107 — ReplicaSets
- Lesson 108 — Deployments
- Lesson 109 — Services
- Reverse proxies and DNS fundamentals

## Theory

### Why Ingress?

Services provide stable access to backend Pods. Ingress adds declarative HTTP/HTTPS routing rules, commonly using hostnames and URL paths, so multiple web applications can share an external entry point.

An Ingress resource describes routing configuration. An Ingress controller implements the rules and processes traffic. Creating an Ingress without a compatible controller does not make the routes work by itself.

### Request flow

A typical flow is:

`DNS → external entry point → Ingress controller → Service → eligible backend Pod`

DNS resolves the hostname to an address associated with the entry point. The controller evaluates the HTTP host and path, then forwards traffic to the configured backend. Depending on the implementation, a controller may route through Service networking or directly to discovered endpoints.

### Routing rules

- **Host-based:** different hostnames route to different backends, such as `shop.example.com` and `api.example.com`.
- **Path-based:** different paths route to different backends, such as `/` and `/api` on one hostname.
- `Exact` matches the exact path.
- `Prefix` matches slash-separated path elements.
- `ImplementationSpecific` leaves matching behavior to the controller.

Path matching does not automatically rewrite or strip the matched prefix. Rewriting behavior depends on controller configuration.

### Example

```yaml
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: orders-ingress
spec:
  ingressClassName: nginx
  rules:
    - host: api.example.com
      http:
        paths:
          - path: /orders
            pathType: Prefix
            backend:
              service:
                name: orders-api
                port:
                  number: 80
```

The cluster must have a compatible controller and matching IngressClass. The `orders-api` Service must exist in the same namespace as the Ingress. Port `80` here is the Service port, not necessarily the backend container port.

### TLS

Ingress can reference TLS certificate material through a Secret:

```yaml
spec:
  tls:
    - hosts:
        - api.example.com
      secretName: api-example-tls
```

The controller must support the configuration and be able to access the Secret. Certificate provisioning and renewal may require separate tooling. TLS often terminates at the controller; traffic to the backend may still use HTTP unless upstream encryption is configured.

### Ingress and LoadBalancer Services

A Service of type `LoadBalancer` exposes a Service through a supported load-balancing implementation. Ingress configures HTTP/HTTPS routing rules. They can work together: the Ingress controller may itself be exposed by a LoadBalancer Service.

Standard Ingress focuses on HTTP/HTTPS. Advanced routing capabilities and annotations vary by controller. Gateway API offers a richer Kubernetes networking API model.

## Real World Example

A cluster hosts a storefront, an orders API, and an admin interface. An external entry point forwards web traffic to an Ingress controller. Rules route `shop.example.com` to the storefront Service, `api.example.com/orders` to the orders Service, and `/admin` to the admin Service. Each Service then provides access to eligible backend Pods.

## Deep Dive

- Ingress resource: desired routing configuration.
- Ingress controller: software or infrastructure implementing that configuration.
- IngressClass: identifies the intended controller class.
- DNS, external exposure, and certificate provisioning are related but separate concerns.
- Backend rules target a Service and Service port, not a Deployment or Pod directly.
- TLS termination at the edge does not guarantee encryption on internal hops.
- A 404 may indicate a rule mismatch or an application response; a 502/503 may indicate an upstream problem, depending on the controller.

## Hands-on Exercise

On a cluster you are authorized to inspect, use the [Lesson 110 command reference](../commands/110-ingress.md). Inspect Ingress resources, classes, Services, Pods, and events. Trace one hostname/path rule to its backend Service and explain how traffic can reach an eligible Pod. If no cluster is available, trace the example configuration on paper.

Use read-only commands for this introductory exercise. Do not install controllers or modify shared or production clusters without authorization.

## Common Misconceptions

- Creating an Ingress resource alone does not expose an application.
- An Ingress resource and an Ingress controller are not the same thing.
- Ingress typically routes to Services, not directly to Deployments.
- Ingress does not automatically provision DNS records or certificates in every setup.
- HTTPS at the edge does not automatically encrypt backend traffic.
- Path matching does not necessarily rewrite the path.
- Ingress is not a universal replacement for Service exposure, especially for non-HTTP protocols.

## Summary

Ingress declares HTTP/HTTPS routing rules into a Kubernetes cluster. A compatible controller implements those rules, commonly routing by hostname and path to Services. External addressing, TLS provisioning, and advanced routing depend on the controller and surrounding infrastructure.

## Key Takeaways

- Ingress resource = routing configuration; controller = implementation.
- Typical flow: DNS → external entry point → controller → Service → Pod.
- Host and path rules determine which backend Service receives a request.
- The configured backend port is a Service port.
- Verify controller availability, routing rules, Service endpoints, DNS, and TLS when troubleshooting.

## Reflection Questions

1. What is the difference between an Ingress resource and an Ingress controller?
2. Trace a request to `https://api.example.com/orders/123` from DNS to a backend Pod.
3. How do host-based and path-based routing differ?
4. Why might an Ingress resource exist while the application remains unreachable?
5. If TLS terminates at the controller and the backend hop uses HTTP, which segment is encrypted?

## What's Next

Lesson 111 — Kubernetes ConfigMaps: separating non-sensitive application configuration from container images and injecting configuration into Pods.
