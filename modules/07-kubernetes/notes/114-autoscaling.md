# Lesson 114 — Kubernetes Autoscaling

## Objectives

- Explain why autoscaling is needed.
- Distinguish horizontal and vertical scaling.
- Explain HPA and metrics-driven replica decisions.
- Understand CPU requests, metrics availability, and scheduling capacity.
- Distinguish HPA, VPA, and Cluster Autoscaler.
- Troubleshoot scaling that does not produce ready replicas.

## Prerequisites

Lessons 106–113: Pods, ReplicaSets, Deployments, Services, Ingress, ConfigMaps, Secrets, and Persistent Volumes.

## Theory

Autoscaling adjusts workload or infrastructure capacity in response to changing demand. It is not instantaneous and does not guarantee application throughput.

- **Horizontal scaling:** change the number of replicas.
- **Vertical scaling:** change the resources allocated to a workload.
- **HPA (Horizontal Pod Autoscaler):** adjusts a scalable workload's desired replica count based on configured metrics.
- **VPA (Vertical Pod Autoscaler):** recommends or adjusts per-Pod CPU/memory requests and, depending on configuration, limits. Applying updates may require Pod recreation.
- **Cluster Autoscaler:** adjusts node-group capacity when supported and configured, commonly to help schedule Pods that cannot fit on existing nodes.

### HPA mental model

Metrics are observed through Kubernetes metrics APIs. For CPU/memory resource metrics, Metrics Server commonly provides resource metrics. Other metric types may need additional adapters or integrations. HPA compares observed metrics with configured targets and updates the workload's desired replicas.

A simplified recommendation is:

`desired replicas = ceil(current replicas × current metric / target metric)`

For example, 3 replicas at 90% average CPU utilization against a 60% target gives `ceil(3 × 90/60) = 5`. This is illustrative; the real controller accounts for tolerance, unavailable metrics, stabilization, policies, and replica bounds.

For CPU utilization percentage, CPU requests are the baseline. If CPU requests are missing for affected containers, utilization may be undefined and CPU-based scaling may not work as expected. Requests also inform scheduling; limits cap resource usage.

### Capacity chain

1. Demand or metrics change.
2. HPA computes a desired replica count.
3. The workload controller creates Pods.
4. The scheduler places Pods on nodes.
5. Kubelets start containers; readiness checks determine when Pods can serve traffic.
6. If Pods cannot fit due to insufficient cluster capacity, a configured Cluster Autoscaler may add nodes through a supported provider/node group.

HPA does not add worker nodes. The scheduler places Pods but does not provision nodes by itself. Additional replicas may not improve throughput if a shared dependency such as a database is saturated.

## Real World Example

An API Deployment runs three replicas at normal load. A traffic spike increases CPU utilization above the HPA target, so HPA raises the desired replica count. If existing nodes have capacity, the scheduler places the new Pods. If not, Pods may remain Pending until capacity becomes available; a configured Cluster Autoscaler may add nodes. Pods still need time to start and become Ready.

## Deep Dive

- HPA scales workload replicas; Cluster Autoscaler scales node capacity; VPA changes resource sizing.
- HPA requires usable metrics. `kubectl top` and CPU/memory HPA targets depend on a functioning resource metrics pipeline.
- CPU utilization is measured relative to requests, not limits.
- Scaling is bounded by min/max replicas, policies, stabilization behavior, metric availability, scheduling constraints, and startup/readiness time.
- More replicas do not guarantee more throughput if the app is not horizontally scalable or a dependency is saturated.
- HPA may request more Pods while some remain Pending; inspect scheduling events and node capacity separately from HPA status.

## Hands-on Exercise

On a local or authorized cluster, use read-only inspection:

```bash
kubectl config current-context
kubectl get hpa
kubectl describe hpa <hpa-name>
kubectl get deployments
kubectl get pods -o wide
kubectl describe pod <pod-name>
kubectl top pods
kubectl top nodes
kubectl get events --sort-by=.metadata.creationTimestamp
```

Inspect HPA min/max replicas, current and target metrics, desired/current replicas, and events/conditions. If Pods remain Pending, inspect scheduler events, requests, node capacity, and placement constraints. `kubectl top` requires working resource metrics. Do not alter scaling policies in shared or production clusters without authorization.

## Common Misconceptions

- HPA adds worker nodes.
- More replicas always mean more throughput.
- CPU utilization percentage is calculated against CPU limits.
- Scaling is instantaneous.
- Every desired Pod will necessarily be scheduled and become Ready.
- Autoscaling always reduces cost.

## Summary

Kubernetes has separate mechanisms for scaling replicas, per-Pod resources, and cluster nodes. HPA responds to configured metrics by changing workload replicas; VPA focuses on resource sizing; Cluster Autoscaler can change node capacity. Effective scaling depends on metrics, resource requests, available capacity, application behavior, dependencies, and startup time.

## Key Takeaways

- Horizontal scaling changes replica count; vertical scaling changes per-workload resource sizing.
- HPA scales workloads, not worker nodes.
- CPU requests are the baseline for CPU utilization targets.
- Cluster Autoscaler may help when Pods cannot be scheduled due to insufficient capacity.
- Scaling only helps when the application and dependencies can use the added capacity.
- Inspect metric health, HPA conditions, Pod events, scheduling, and readiness as separate stages.

## Reflection Questions

1. What is the difference between HPA and Cluster Autoscaler?
2. HPA wants to scale a Deployment from 3 replicas to 8, but new Pods remain Pending because worker nodes have insufficient CPU. What is happening, and what mechanism could help?
3. Why do CPU resource requests matter when configuring CPU-based HPA?
4. Your application has 10 replicas, but database latency is very high. Why might scaling the application further fail to improve performance?
5. What are two reasons autoscaling may not respond quickly enough to a sudden traffic spike?

## What's Next

Lesson 115 — Kubernetes Scheduling: how the scheduler chooses a node for a Pod, how resource requests affect placement, and why Pods can remain Pending.