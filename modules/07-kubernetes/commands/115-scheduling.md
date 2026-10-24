# Lesson 115 — Kubernetes Scheduling Command Reference

Use these commands on a local or authorized cluster. Begin with read-only inspection and confirm the context before inspecting workloads.

## Inspect Pods and nodes

```bash
kubectl config current-context
kubectl get nodes --show-labels
kubectl get pods -A -o wide
kubectl describe pod <pod-name>
kubectl describe node <node-name>
```

Check the Pod's node assignment, scheduling conditions, node labels, allocatable capacity, taints, and events.

## Inspect events and resource usage

```bash
kubectl get events --sort-by=.metadata.creationTimestamp
kubectl top nodes
kubectl top pods -A
```

`kubectl top` requires a working resource metrics pipeline and reports observed usage. Compare node allocatable resources and existing Pod requests when investigating scheduling fit.

## Troubleshooting sequence

1. Confirm the current cluster context and namespace.
2. Run `kubectl get pod <pod-name> -o wide` to see whether a node is assigned.
3. Run `kubectl describe pod <pod-name>` and read scheduling events and conditions.
4. If unassigned, inspect Pod requests, node allocatable capacity, node selectors, affinity, taints/tolerations, topology rules, and volume constraints.
5. If assigned but still Pending, inspect volume setup, image pulling, and container setup events.
6. If Running but not Ready, investigate readiness probes, startup, configuration, and dependencies.
7. Consider Cluster Autoscaler only when the evidence points to insufficient node capacity and autoscaling is configured and supported.

## Safety

- Start with read-only commands.
- Avoid changing labels, taints, affinity, priorities, or workload resources in shared or production clusters without authorization.
- Do not evict workloads to test preemption on a shared cluster.
- Use a disposable local cluster for state-changing experiments.
