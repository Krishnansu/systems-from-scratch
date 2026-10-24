# Lesson 109 — Services Command Reference

Use these read-only commands only against a Kubernetes cluster and namespace you are authorized to inspect. Replace example names and labels with values from your environment.

## List Services

```bash
kubectl get services
kubectl get services -A
kubectl get service orders-api
kubectl describe service orders-api
```

The default commands use the current namespace. `-A` lists across namespaces, subject to permissions.

## Inspect Pod Labels and Service Selectors

```bash
kubectl get pods --show-labels
kubectl get pods -l app=orders-api
kubectl get service orders-api -o yaml
```

Compare `spec.selector` in the Service with the labels on intended backend Pods. A selector mismatch can prevent the Service from discovering the expected Pods.

## Inspect EndpointSlices

```bash
kubectl get endpointslices
kubectl get endpointslices -o wide
kubectl describe endpointslice <endpointslice-name>
```

EndpointSlices show backend addresses and endpoint conditions. Identify the EndpointSlice associated with the Service before interpreting its entries. An absence of eligible endpoints can result from selector mismatch, missing matching Pods, readiness, or endpoint conditions.

## Understand Service Ports and Types

```bash
kubectl get service orders-api -o yaml
kubectl describe service orders-api
```

Inspect `spec.type`, `spec.ports`, `port`, `targetPort`, `nodePort` (if applicable), and `spec.selector`. The application must listen on the backend target port. A Service configuration alone does not prove that the application is healthy or reachable.

## Troubleshooting Checklist

1. Confirm the Service exists in the expected namespace.
2. Check its selector and compare it with actual Pod labels.
3. Inspect EndpointSlices and their endpoint conditions.
4. Check Pod status, readiness, events, and scheduling issues; inspect container logs when appropriate.
5. Confirm the application listens on the expected target port.
6. If endpoints exist but connections fail, investigate Service networking, DNS, NetworkPolicies, firewalls, and application health as appropriate.
7. For DNS problems, test from a suitable client Pod and confirm the correct Service name and namespace.

## Safety

- Check the current Kubernetes context and namespace before inspecting a cluster.
- These examples are read-only; do not apply, delete, expose, or modify workloads for this exercise.
- Treat YAML, events, and logs as potentially sensitive.
- Avoid changing resources in shared or production clusters without explicit authorization.

## Related Lessons

- [106 — Pods](../notes/106-pods.md)
- [107 — ReplicaSets](../notes/107-replicasets.md)
- [108 — Deployments](../notes/108-deployments.md)
- [109 — Services](../notes/109-services.md)
- [110 — Ingress](../notes/110-ingress.md) (upcoming)
