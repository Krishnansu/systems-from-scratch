# Lesson 114 — Kubernetes Autoscaling Command Reference

Use these commands on a local or authorized cluster. Start with read-only inspection; do not change scaling policies in shared or production clusters without authorization.

## Inspect autoscalers and workloads

```bash
kubectl config current-context
kubectl get hpa
kubectl describe hpa <hpa-name>
kubectl get deployments
kubectl get pods -o wide
```

Review HPA minimum/maximum replicas, current and target metrics, desired/current replica counts, conditions, and events.

## Inspect metrics and resources

```bash
kubectl top pods
kubectl top nodes
kubectl describe pod <pod-name>
kubectl get events --sort-by=.metadata.creationTimestamp
```

`kubectl top` requires the resource metrics pipeline. For CPU-based HPA, check CPU requests as well as usage; utilization is relative to requests.

## Troubleshooting sequence

1. Confirm cluster context and namespace.
2. Inspect HPA status, targets, min/max replicas, conditions, and events.
3. Verify metrics are available and current.
4. Inspect Deployment desired/current/ready replicas.
5. If Pods are Pending, inspect Pod events, resource requests, node capacity, and placement constraints.
6. If Pods are Running but not Ready, investigate startup, readiness probes, and application dependencies.
7. Check whether a saturated dependency, such as a database, is limiting throughput.

## Safety

- Begin with read-only inspection.
- Use a disposable local cluster for scaling experiments.
- Treat `kubectl scale`, `kubectl apply`, and changes to HPA resources as state-changing actions.
- Do not change shared or production scaling policies without authorization.