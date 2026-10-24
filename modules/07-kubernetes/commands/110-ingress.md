# Lesson 110 — Ingress Command Reference

Use these commands to inspect Ingress configuration. Commands are read-only; output may contain sensitive hostnames, annotations, or configuration details.

## Inspect the cluster

```bash
kubectl config current-context
kubectl get ingress -A
kubectl get ingressclass
kubectl get services -A
kubectl get pods -A
```

- `current-context`: confirms which cluster context is active.
- `get ingress -A`: lists Ingress resources across namespaces.
- `get ingressclass`: lists declared controller classes.
- Services and Pods help identify possible backends and controller workloads.

## Inspect a resource

```bash
kubectl describe ingress <ingress-name> -n <namespace>
kubectl get ingress <ingress-name> -n <namespace> -o yaml
kubectl get events -n <namespace> --sort-by=.metadata.creationTimestamp
```

Replace placeholders with the actual resource name and namespace. Review hosts, paths, path types, backend Service names and ports, TLS references, events, and the intended IngressClass.

## Troubleshooting checklist

1. Confirm the current cluster context and namespace.
2. Check DNS and the address of the external entry point.
3. Confirm a compatible Ingress controller is running and the IngressClass matches.
4. Check host and path rules, backend Service name, and Service port.
5. Inspect the Service selector, EndpointSlices, and Pod readiness using the Lesson 109 reference.
6. Check controller logs and events if permitted; logs may contain sensitive information.
7. For HTTPS failures, verify the hostname, certificate validity, TLS settings, and referenced Secret access.

A 404 may come from a rule mismatch or from the application. A 502/503 may indicate an upstream issue, but exact meanings vary by controller. Correlate the response with controller logs and backend state.

## Safety

These commands are for inspection. Do not install controllers, edit Ingress resources, expose Services, or change DNS in a shared or production environment without authorization.
