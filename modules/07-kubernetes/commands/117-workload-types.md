# Lesson 117 — Kubernetes Workload Types Command Reference

Use read-only commands against a local or authorized cluster.

## Inspect workload controllers

```bash
kubectl get deployments,statefulsets,daemonsets,jobs,cronjobs
kubectl get pods -o wide
kubectl describe deployment <name>
kubectl describe statefulset <name>
kubectl describe daemonset <name>
kubectl describe job <name>
kubectl describe cronjob <name>
```

Use the appropriate namespace when needed. `kubectl get` supports these resource types, though combining resources may produce different columns for each type.

## Inspect Jobs and scheduled runs

```bash
kubectl get jobs
kubectl get cronjobs
kubectl get pods --selector=job-name=<job-name>
kubectl describe job <job-name>
kubectl get events --sort-by=.metadata.creationTimestamp
```

Inspect Job status, retry behavior, Pod logs, CronJob schedule, and recent events when a task fails or does not run as expected.

## Safety

- Begin with read-only inspection.
- Creating, deleting, or manually triggering Jobs can run real workload code. Do this only in a disposable or authorized environment.
- Avoid deleting Jobs or their Pods in shared or production clusters without understanding the consequences.
