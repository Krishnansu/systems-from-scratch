# Lesson 127 — Istio Command Reference

Use only clusters and namespaces you are authorized to inspect. These exercises are read-only; do not change shared resources.

## Confirm Context

```bash
kubectl config current-context
kubectl get namespaces
```

## Check for Istio Custom Resource Definitions

```bash
kubectl get crd gateways.networking.istio.io
kubectl get crd virtualservices.networking.istio.io
kubectl get crd destinationrules.networking.istio.io
kubectl get crd peerauthentications.security.istio.io
kubectl get crd authorizationpolicies.security.istio.io
kubectl get crd serviceentries.networking.istio.io
```

A missing CRD may indicate that the resource type is not installed under that name; it does not prove the whole cluster is unhealthy.

## Inspect Existing Resources

```bash
kubectl get gateways,virtualservices,destinationrules -n <namespace>
kubectl get peerauthentications,authorizationpolicies -n <namespace>
kubectl get serviceentries -n <namespace>
kubectl get virtualservice <name> -n <namespace> -o yaml
kubectl describe virtualservice <name> -n <namespace>
```

Review hosts, route matches, destinations, subsets, and policy scope. Resource output may contain sensitive information.

## Optional Istio CLI Diagnostics

```bash
istioctl version
istioctl analyze -n <namespace>
istioctl proxy-status
```

Availability and permissions depend on the environment. `analyze` can detect some configuration issues; `proxy-status` helps inspect proxy synchronization. Neither proves end-to-end application health.

## Troubleshooting Sequence

1. Confirm cluster context and namespace.
2. Inspect the Kubernetes Service, selectors, workload labels, readiness, and endpoints.
3. Inspect VirtualService destination and matching rules.
4. If subsets are used, inspect the corresponding DestinationRule and workload labels.
5. Check proxy synchronization and active configuration when authorized.
6. Trace the first failing hop through caller proxy, network, destination proxy, and application.
7. Check security policies and application/downstream latency as indicated by evidence.

## Safety Notes

- Do not apply, delete, restart, or modify shared resources for this exercise.
- Do not expose proxy administration interfaces or sensitive diagnostic output.
- A valid resource or synchronized proxy does not guarantee reachability or application success.

## Related Lessons

- [125 — Envoy](../notes/125-envoy.md)
- [126 — Service Mesh](../notes/126-service-mesh.md)
- [127 — Istio](../notes/127-istio.md)
