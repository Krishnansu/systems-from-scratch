# Lesson 126 — Service Mesh Command Reference

Use only Kubernetes contexts and namespaces you are authorized to inspect. These commands are read-only; do not install a mesh, apply policies, restart proxies, or modify shared workloads for this lesson.

## Confirm Context and Inspect Workloads

```bash
kubectl config current-context
kubectl get pods -n <namespace> -o wide
kubectl get services -n <namespace>
kubectl get endpointslices -n <namespace>
```

Use these outputs to separate workload state, Service definitions, and endpoint information. Successful DNS or Service discovery does not guarantee network reachability or application health.

## Inspect a Specific Pod

```bash
kubectl get pod <pod-name> -n <namespace> -o yaml
kubectl describe pod <pod-name> -n <namespace>
```

Look at container names and images, ports, readiness probes, resource requests, labels, configuration references, and events. A second container does not prove that it is a mesh proxy, and a Pod without a sidecar may still use another mesh architecture.

## Troubleshooting Checklist

1. Confirm the intended namespace and workload identity.
2. Check service discovery and endpoint information.
3. Verify network reachability and listening ports.
4. Inspect proxy configuration and relevant policy where authorized tools are available.
5. Check workload identity and authorization failures.
6. Inspect destination application readiness, logs, and downstream dependencies.
7. Correlate the symptom with configuration changes, rollouts, or resource pressure.

## Safety and Interpretation

- Do not assume a mesh implementation or proxy from container count alone.
- Do not print secrets or expose proxy admin interfaces.
- Treat YAML, logs, and telemetry as potentially sensitive.
- Prefer read-only inspection; do not apply configuration or change production resources for this exercise.
- The exact mesh-specific inspection commands depend on the implementation. This reference intentionally avoids assuming that Istio or another mesh is installed.

## Related Lessons

- [123 — API Gateway](../notes/123-api-gateway.md)
- [124 — Sidecars](../notes/124-sidecars.md)
- [125 — Envoy](../notes/125-envoy.md)
- [126 — Service Mesh](../notes/126-service-mesh.md)
