# Lesson 118 — Resource Management, QoS, and Eviction

## Objectives

- Distinguish resource requests from limits.
- Understand Kubernetes QoS classes.
- Diagnose CPU throttling, OOM kills, and node-pressure eviction.

## Core Concepts

- **Requests** influence scheduling and resource allocation under contention.
- **Limits** constrain container resource usage.
- CPU limits generally cause throttling when the quota is exhausted.
- Exceeding a container's memory limit can result in an `OOMKilled` termination.
- Node-pressure eviction is a kubelet action to reclaim resources such as memory or ephemeral storage. It differs from a container exceeding its own memory limit.

## Example

```yaml
resources:
  requests:
    cpu: "250m"
    memory: "128Mi"
  limits:
    cpu: "1"
    memory: "512Mi"
```

`250m` is one-quarter of a CPU core; `1` is one full core. Requests are used for scheduling decisions, while limits constrain usage. CPU requests are not hard caps, and memory requests are not hard reservations of physical memory.

## QoS Classes

| Class | General criteria |
|---|---|
| Guaranteed | Every container has CPU and memory requests equal to their limits, with valid nonzero settings |
| Burstable | Pod has resource requests or limits but does not meet Guaranteed criteria |
| BestEffort | No container specifies CPU or memory requests or limits |

QoS affects eviction preference but does not guarantee survival. Node-pressure eviction decisions also consider usage relative to requests and Pod priority.

## Troubleshooting Commands

```bash
kubectl describe pod <pod-name>
kubectl get pod <pod-name> -o wide
kubectl top pod <pod-name>
kubectl top node
kubectl describe node <node-name>
kubectl get events --sort-by=.metadata.creationTimestamp
```

`kubectl top` requires working Metrics Server metrics and provides a usage snapshot, not historical monitoring.

- High latency with CPU near its limit: inspect CPU throttling and limit sizing.
- `OOMKilled`: inspect memory usage, limits, and possible leaks.
- Evicted Pod: inspect Pod events and node pressure conditions.
- Pending Pod: inspect requests, node allocatable capacity, and scheduling events.

## Common Mistakes

- Setting requests too low can lead to overpacking nodes.
- Setting requests too high can waste schedulable capacity.
- CPU throttling and memory OOM kills are different failure modes.
- QoS class is not an absolute guarantee against eviction.

## Key Takeaways

Resource requests shape scheduling; limits constrain usage. CPU limits can throttle a workload, memory limits can lead to OOM kills, and node pressure can cause eviction. Diagnose the specific failure mechanism before changing resource settings.

## Related Lessons

- Lesson 114 — Autoscaling
- Lesson 115 — Scheduling
- Lesson 117 — Kubernetes Workload Types
- Lesson 120 — End-to-End Kubernetes Troubleshooting Lab
