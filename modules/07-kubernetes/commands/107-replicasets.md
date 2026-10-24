# Lesson 107 — ReplicaSets Command Reference

Run these read-only commands only against a Kubernetes cluster and namespace you are authorized to inspect.

## List ReplicaSets

```bash
kubectl get replicasets
kubectl get rs
kubectl get rs -A
```

The default commands show ReplicaSets in the current namespace. `-A` lists across namespaces, subject to permissions.

## Inspect Replica Counts and Details

```bash
kubectl get rs <replicaset-name>
kubectl describe rs <replicaset-name>
kubectl get rs <replicaset-name> -o yaml
```

The table typically includes desired, current, and ready counts. `describe` shows selector information and events that may explain why Pods are not being created or becoming ready.

## Inspect Pod Labels and Ownership

```bash
kubectl get pods --show-labels
kubectl get pods -o wide
kubectl get pods -l app=orders-api
kubectl describe pod <pod-name>
```

Replace the example label with the label used by the workload. Confirm the selector matches the intended Pods. Do not assume that every Pod with a similar name belongs to a particular ReplicaSet; inspect ownership and labels.

## Inspect Deployments and ReplicaSets Together

```bash
kubectl get deployments
kubectl get deployments,replicasets,pods
kubectl describe deployment <deployment-name>
```

This helps show how a Deployment manages ReplicaSets and how ReplicaSets relate to their Pods.

## Troubleshooting Checklist

1. Compare desired, current, and ready replica counts.
2. Inspect ReplicaSet events with `kubectl describe rs <replicaset-name>`.
3. Verify selector labels match the intended Pod labels.
4. Inspect Pod status, events, and container logs when Pods do not become ready.
5. Check scheduling constraints, resource requests, image-pull errors, and volume-mount events.
6. Remember that a ReplicaSet can request Pods but cannot guarantee capacity or application health.

## Safety

- These examples are read-only; do not apply, delete, or scale workloads as part of this exercise.
- Check your current context and namespace before inspecting a cluster.
- Treat YAML, events, and logs as potentially sensitive.
- Avoid changing resources in shared or production clusters without explicit authorization.

## Related Lessons

- [105 — Kubernetes Architecture](../notes/105-kubernetes-architecture.md)
- [106 — Pods](../notes/106-pods.md)
- [107 — ReplicaSets](../notes/107-replicasets.md)
- [108 — Deployments](../notes/108-deployments.md) (upcoming)
