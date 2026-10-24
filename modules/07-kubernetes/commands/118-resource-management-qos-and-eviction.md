# Lesson 118 — Resource Management, QoS, and Eviction: Commands

## Inspect resource configuration and status

```bash
kubectl describe pod <pod-name>
kubectl get pod <pod-name> -o wide
kubectl get pod <pod-name> -o yaml
kubectl top pod <pod-name>
kubectl top node
kubectl describe node <node-name>
kubectl get events --sort-by=.metadata.creationTimestamp
```

`kubectl top` requires Metrics Server metrics. Pod YAML and descriptions may expose sensitive configuration; handle output accordingly.

## What to look for

- **CPU throttling or latency:** compare usage with CPU limits; use application or container metrics to confirm throttling.
- **OOMKilled:** inspect container termination state, previous logs, and memory limits.
- **Eviction:** check Pod events and node conditions for memory, ephemeral-storage, or inode pressure.
- **Pending:** compare Pod requests with node allocatable resources and review scheduling events.

## Safety

These commands are for inspection. Avoid changing production resource settings or deleting workloads before identifying the failure mechanism and checking ownership and impact.
