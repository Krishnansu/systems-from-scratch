# Lesson 115 — Kubernetes Scheduling

## Objectives

- Explain the scheduler's role in Pod placement.
- Understand filtering and scoring of candidate nodes.
- Explain how resource requests affect scheduling.
- Distinguish node selectors, affinity, taints, tolerations, and topology spread.
- Troubleshoot Pods that remain Pending.

## Prerequisites

Lessons 106–114: Pods, ReplicaSets, Deployments, Services, configuration, persistent volumes, and autoscaling.

## Theory

The `kube-scheduler` selects a suitable node for a Pod that has not yet been assigned to one. It does not start containers or provision worker nodes. After assignment, the kubelet on the selected node manages the Pod's containers.

A simplified scheduling flow is:

```text
Pod created
    |
    v
Scheduler filters unsuitable nodes
    |
    v
Scores eligible nodes
    |
    v
Selects a node and records the assignment
    |
    v
Kubelet and container runtime start the workload
```

### Filtering and scoring

- **Filtering:** removes nodes that violate resource, label, taint, affinity, volume, topology, or other scheduling requirements.
- **Scoring:** ranks eligible nodes according to configured scheduling plugins and policies.
- The scheduler does not simply select the node with the lowest instantaneous CPU usage.

### Requests and capacity

Scheduling uses resource requests and node allocatable capacity to evaluate fit. A node may have low observed CPU usage yet lack sufficient remaining requested capacity for a new Pod. Limits govern resource-use ceilings rather than serving as the baseline for ordinary scheduling fit.

```yaml
resources:
  requests:
    cpu: "2"
    memory: "1Gi"
  limits:
    cpu: "3"
    memory: "2Gi"
```

This example requests 2 CPU cores and 1 GiB of memory. Placement also depends on the other containers in the Pod, existing requests, node allocatable resources, and scheduling constraints.

### Placement constraints

- **`nodeSelector`:** requires node labels to match specified values.
- **Node affinity:** expresses required or preferred node-label rules.
- **Pod affinity / anti-affinity:** expresses required or preferred placement relative to other matching Pods.
- **Taints and tolerations:** a taint can repel Pods; a matching toleration permits the Pod to tolerate that taint but does not force placement there.
- **Topology spread constraints:** guide or constrain distribution across topology domains such as nodes or zones.
- **Volume constraints:** storage availability, attachment, and topology can affect placement.

Hard requirements can make a Pod unschedulable; preferences influence node scoring.

## Real World Example

HPA increases an API Deployment's desired replicas from three to six. The ReplicaSet creates additional Pods, but existing nodes cannot fit their resource requests. The scheduler leaves them unscheduled. A configured Cluster Autoscaler may add nodes if the provider and node-group configuration support it. The new nodes must still satisfy the Pods' constraints, and startup takes additional time.

## Deep Dive

- HPA changes desired workload replicas; the scheduler assigns Pods to nodes; Cluster Autoscaler may change node capacity.
- `Pending` does not always mean unscheduled. A Pod can have a node assignment but still wait for volume setup, image pulling, or container setup.
- If a Pod has no assigned node, inspect scheduling events, resource requests, allocatable capacity, labels, taints, affinity, topology, and volume constraints.
- If it is assigned but remains Pending, inspect Pod events, volume mounting, image pulling, and container setup.
- If it is Running but not Ready, investigate readiness probes, startup, configuration, and dependencies.
- Preemption can sometimes make room for a higher-priority Pod by evicting lower-priority Pods, but it cannot solve every placement constraint or create physical capacity.
- `kubectl top` shows observed resource usage; it is not a replacement for inspecting requests and allocatable capacity.

## Hands-on Exercise

Use a local or authorized cluster and begin with read-only inspection:

```bash
kubectl config current-context
kubectl get nodes --show-labels
kubectl get pods -A -o wide
kubectl describe pod <pod-name>
kubectl describe node <node-name>
kubectl get events --sort-by=.metadata.creationTimestamp
kubectl top nodes
kubectl top pods -A
```

Check whether the Pod has a node assignment, read its events, inspect its requests, compare them with node allocatable capacity, and review placement and storage constraints. `kubectl top` requires a functioning resource metrics pipeline. Do not change shared-cluster scheduling rules or evict workloads for an introductory exercise.

## Common Misconceptions

- The scheduler starts containers.
- The least busy node is always selected.
- Low actual CPU usage guarantees a Pod will fit.
- A toleration forces a Pod onto a tainted node.
- Adding nodes fixes every unschedulable Pod.
- Every Pending Pod is still waiting for scheduling.

## Summary

Kubernetes scheduling chooses a node by filtering unsuitable candidates and scoring eligible ones. Resource requests, allocatable capacity, placement rules, and storage constraints all affect whether a Pod can be assigned. Troubleshooting starts by determining whether the Pod has a node assignment and then inspecting the appropriate events and constraints.

## Key Takeaways

- The scheduler selects a node; the kubelet manages the Pod on that node.
- Requests and allocatable capacity are central to scheduling.
- Hard placement constraints can make a Pod unschedulable even when other nodes have spare resources.
- Tolerations permit matching taints; they do not force placement.
- Cluster Autoscaler can help with supported capacity shortages, not arbitrary placement constraints.
- Diagnose scheduling, volume setup, startup, and readiness as separate stages.

## Reflection Questions

1. What are the two high-level scheduling stages, and what happens in each?
2. How can a Pod fail to fit on a node with low actual CPU usage?
3. What is the difference between a node selector and a toleration?
4. HPA increases a Deployment from three to eight replicas, but the new Pods remain Pending. What would you investigate?
5. Why should you investigate different causes when a Pending Pod already has a node assignment?

## What's Next

Lesson 116 — Kubernetes Health Checks and Probes: how Kubernetes distinguishes container liveness, readiness to receive traffic, and startup.
