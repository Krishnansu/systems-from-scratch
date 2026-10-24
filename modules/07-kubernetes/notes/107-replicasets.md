# Lesson 107 — Kubernetes ReplicaSets

## Objectives

- Explain why ReplicaSets exist and what problem they solve.
- Understand desired replica count and reconciliation.
- Explain labels, selectors, and Pod templates.
- Distinguish Pod count from Pod readiness and application health.
- Explain the relationship between ReplicaSets and Deployments.

## Prerequisites

- Lesson 105 — Kubernetes Architecture
- Lesson 106 — Pods

## Theory

### 1. Why ReplicaSets?

A ReplicaSet maintains a desired number of matching Pod replicas. Without a controller, an operator would need to notice missing Pods and create replacements manually.

The ReplicaSet controller repeatedly compares desired state with observed state and creates or removes Pods as needed. Reconciliation is asynchronous and does not guarantee that every Pod will become healthy or run immediately.

### 2. ReplicaSet specification

A ReplicaSet primarily uses three things:

- **Replicas:** desired number of Pods.
- **Selector:** identifies Pods belonging to the ReplicaSet.
- **Pod template:** describes Pods to create when additional replicas are needed.

The selector and template labels must be compatible. Avoid overlapping selectors across independently managed ReplicaSets.

### 3. Reconciliation

If the desired count is three and only two matching Pods exist, the controller requests another Pod from the template. If more Pods exist than desired, it can reduce the set.

The ReplicaSet controller creates Pod objects; it does not schedule or run their containers itself. The scheduler assigns an eligible Node, and the Node's kubelet works with the container runtime to run the containers.

A replacement is a new Pod object. It may have a different name, IP address, and Node from the Pod it replaces.

### 4. Replica count versus readiness

The number of existing Pods is not the same as the number of ready Pods. A ReplicaSet may report three current Pods but only two ready Pods. The remaining Pod might still be starting, failing, or not passing readiness checks.

A correctly configured Service normally routes traffic to eligible endpoints rather than every Pod object indiscriminately. ReplicaSet replica management does not guarantee application health.

### 5. Labels and selectors

Labels are key-value metadata attached to Kubernetes objects. A selector matches Pods by labels, allowing controllers to identify the workload instances they manage.

For example, a Pod may have the label `app: orders-api`, and a ReplicaSet selector can match that label. The Pod template must supply matching labels so newly created Pods belong to the intended set.

### 6. ReplicaSet and Deployment

A ReplicaSet maintains the desired number of Pods for its template. A Deployment manages ReplicaSets and provides higher-level rollout behavior, including updating application versions, tracking rollout history, and supporting rollbacks.

For ordinary application deployments, create a Deployment rather than managing ReplicaSets directly. During a version change, a Deployment can create a new ReplicaSet for the new Pod template and scale old and new ReplicaSets according to its rollout strategy.

### 7. Capacity and failure limits

A ReplicaSet can request missing Pods, but it cannot create CPU, memory, or Node capacity by itself. If no suitable Node has enough resources or meets scheduling constraints, a Pod may remain Pending. Cluster autoscaling can add Nodes only when suitable infrastructure and configuration are available.

A ReplicaSet also cannot guarantee that an application starts successfully, passes readiness checks, or is distributed across different Nodes. Those outcomes depend on other cluster mechanisms and workload configuration.

## Real World Example

An `orders-api` ReplicaSet requests three Pods. One Pod is deleted, leaving two matching Pods. The controller observes the mismatch and creates another Pod from its template. The scheduler assigns the new Pod to a suitable Node, and the kubelet and runtime work to start its containers.

The replacement may have a different Pod IP. Clients should use a Service for stable access to eligible Orders Pods rather than depending on individual Pod IPs.

## Deep Dive

- **Pod:** one workload instance containing one or more containers.
- **ReplicaSet:** maintains the desired number of matching Pods.
- **Deployment:** manages ReplicaSets and versioned rollouts.
- **Service:** provides a stable network endpoint for selected eligible Pods.
- **Desired count versus readiness:** a requested replica count does not mean all replicas are ready to serve traffic.

## Hands-on Exercise

On a cluster you are authorized to inspect, run the read-only commands in [the Lesson 107 command reference](../commands/107-replicasets.md). Compare desired, current, and ready replica counts, inspect selectors and labels, and review ReplicaSet events. Do not modify or delete workloads in a shared or production cluster for this exercise.

## Common Misconceptions

- A ReplicaSet does not restart the same deleted Pod object; it creates a replacement Pod.
- A ReplicaSet does not directly schedule Pods or run containers.
- Three current Pods do not necessarily mean three ready Pods.
- A ReplicaSet does not provide stable client addressing; a Service does.
- A ReplicaSet is not the usual resource for managing versioned rollouts; a Deployment manages ReplicaSets.
- A ReplicaSet cannot guarantee capacity, application health, or distribution across Nodes.

## Summary

A ReplicaSet uses a selector and Pod template to maintain a desired number of matching Pods. Its controller reconciles the observed replica count with the desired count, creating replacement Pod objects when needed. Deployments manage ReplicaSets to provide application rollout and rollback capabilities.

## Key Takeaways

- ReplicaSets continuously reconcile desired and observed Pod counts.
- Selectors identify matching Pods; templates describe newly created Pods.
- Replacement Pods are new objects and may receive different IP addresses.
- Replica count and readiness are different measures.
- Deployments manage ReplicaSets for versioned application rollouts.
- Scheduling capacity and application health are not guaranteed by replica management alone.

## Reflection Questions

1. If a ReplicaSet requests four replicas and one Pod is deleted, how does Kubernetes work toward restoring four Pods?
2. Why does a ReplicaSet need both a selector and a Pod template?
3. What does `DESIRED=3`, `CURRENT=3`, and `READY=2` tell you?
4. Why is a Deployment more appropriate than directly managing a ReplicaSet for application version rollouts?
5. What happens when a ReplicaSet requests a Pod but no suitable Node has enough capacity?

## What's Next

Lesson 108 — Deployments: how Kubernetes manages application versions, rolling updates, rollout status, and rollback.
