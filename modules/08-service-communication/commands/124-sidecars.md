# Lesson 124 — Sidecars Command Reference

Use these read-only commands only against a Kubernetes cluster you are authorized to inspect. Replace placeholders with existing workload names.

## Confirm Context and Workloads

```bash
kubectl config current-context
kubectl get pods -n <namespace>
kubectl get pod <pod-name> -n <namespace> -o yaml
```

Inspect `spec.containers`, `spec.initContainers`, `spec.volumes`, container `volumeMounts`, ports, probes, and resource requests/limits. A Pod with multiple containers is only a candidate for investigation; confirm each container's role from configuration and approved documentation.

## Inspect Runtime State

```bash
kubectl describe pod <pod-name> -n <namespace>
kubectl get pod <pod-name> -n <namespace> -o json
```

Review container states, restart counts, readiness, resource configuration, and events. Treat logs and command output as potentially sensitive. Do not infer a container's purpose from its name alone.

## Questions to Answer

1. Which container runs the primary application?
2. What purpose does each additional container serve?
3. Are volumes mounted into more than one container?
4. Are readiness probes and resource limits configured for each relevant container?
5. Is an entry under `initContainers` configured with `restartPolicy: Always`, indicating a native sidecar pattern?

## Interpretation Notes

- Containers in a Pod share the Pod network namespace and IP address, so port conflicts are possible and localhost can be used for local communication.
- Filesystem sharing requires an explicitly configured shared volume.
- Multiple containers do not by themselves prove a sidecar design.
- Resource configuration and status help with diagnosis but do not alone establish a container's architectural role.

## Safety

- These commands are intended for inspection only.
- Do not apply, delete, scale, restart, or modify workloads for this exercise.
- Do not create debug workloads in shared or production clusters without authorization.
- Follow your organization's access policies and handle output as potentially sensitive.

## Related Lessons

- [121 — Service Discovery](../notes/121-service-discovery.md)
- [122 — Internal DNS](../notes/122-internal-dns.md)
- [123 — API Gateway](../notes/123-api-gateway.md)
- [124 — Sidecars](../notes/124-sidecars.md)
