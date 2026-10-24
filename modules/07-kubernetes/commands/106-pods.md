# Lesson 106 — Pods Command Reference

Run these commands only against a Kubernetes cluster and namespace you are authorized to inspect. The commands below are read-only.

## List Pods

```bash
kubectl get pods
kubectl get pods -o wide
kubectl get pods -A
```

- The default command lists Pods in the current namespace.
- `-o wide` includes details such as Node and Pod IP.
- `-A` lists Pods across namespaces; access depends on your permissions.

## Inspect a Pod

```bash
kubectl describe pod <pod-name>
kubectl get pod <pod-name> -o yaml
```

Use `describe` to inspect status, container states, scheduling details, and events. YAML shows the Pod specification and observed status; review output for sensitive environment details before sharing it.

## View Container Logs

```bash
kubectl logs <pod-name>
kubectl logs <pod-name> -c <container-name>
kubectl logs <pod-name> --all-containers=true
```

Specify `-c` when the Pod has multiple containers. Logs may contain sensitive application data, so handle them appropriately.

## Inspect Labels and Placement

```bash
kubectl get pods --show-labels
kubectl get pods -o wide
```

Labels help identify workload groups and are commonly used by Services and controllers to select Pods.

## Troubleshooting Checklist

1. Check phase and container status with `kubectl get pods -o wide`.
2. Inspect events and scheduling details with `kubectl describe pod <pod-name>`.
3. Review logs with `kubectl logs` and specify the container when needed.
4. Check whether the Pod is Running and whether its readiness checks pass; these are not equivalent.
5. Confirm the Pod's Node, IP, labels, and relevant Service selectors when investigating routing.
6. Check resource requests, image-pull errors, and volume-mount events when a Pod cannot start.

## Safety

- Avoid deleting Pods or changing workloads in shared or production clusters during this introductory exercise.
- Treat logs and YAML output as potentially sensitive.
- Do not assume a Pod IP is permanent or use it as a long-term service address.

## Related Lessons

- [105 — Kubernetes Architecture](../notes/105-kubernetes-architecture.md)
- [106 — Pods](../notes/106-pods.md)
- [107 — ReplicaSets](../notes/107-replicasets.md) (upcoming)
