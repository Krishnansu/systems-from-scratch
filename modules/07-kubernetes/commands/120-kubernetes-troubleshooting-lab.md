# Lesson 120 — Kubernetes Troubleshooting Commands

Use read-only inspection first. Confirm cluster context, namespace, permissions, and operational impact before taking action.

## Cluster and workload overview

```bash
kubectl config current-context
kubectl get nodes
kubectl get pods -A -o wide
kubectl get deployments,replicasets -A
kubectl get events -A --sort-by=.metadata.creationTimestamp
```

## Pod and rollout health

```bash
kubectl describe pod <pod-name> -n <namespace>
kubectl logs <pod-name> -n <namespace> --all-containers
kubectl logs <pod-name> -n <namespace> --all-containers --previous
kubectl describe deployment <deployment> -n <namespace>
kubectl rollout status deployment/<deployment> -n <namespace>
kubectl rollout history deployment/<deployment> -n <namespace>
```

Previous logs may be available when a container has restarted. Rollout history and status are inspection commands; undoing a rollout changes state.

## Service routing

```bash
kubectl get services,endpointslices -n <namespace>
kubectl describe service <service> -n <namespace>
kubectl get pods -n <namespace> --show-labels
```

Compare selectors, Pod labels, readiness, EndpointSlices, Service ports, and target ports. Continue with DNS, routing, and NetworkPolicy checks when appropriate.

## Resources and node health

```bash
kubectl top pods -n <namespace>
kubectl top nodes
kubectl describe node <node-name>
```

Metrics require a functioning metrics pipeline. `kubectl top` is a point-in-time view and does not replace historical monitoring.

## Safety

- Avoid exposing credentials or sensitive application output in shared logs.
- Do not delete, restart, scale, apply, or roll back production workloads without authorization and an incident plan.
- Preserve evidence before mitigation when practical.
- Verify recovery using workload health and service-level signals, not only Pod status.
