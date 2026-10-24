# Lesson 108 — Kubernetes Deployments

## Objectives

- Explain why Deployments manage ReplicaSets rather than individual Pods directly.
- Understand how Pod-template changes trigger new ReplicaSets and rollout revisions.
- Explain rolling updates, `maxSurge`, and `maxUnavailable`.
- Inspect rollout status and revision history.
- Explain rollback limitations, especially for external state such as databases.

## Prerequisites

- Lesson 106 — Pods
- Lesson 107 — ReplicaSets

## Theory

### 1. Why Deployments?

A ReplicaSet maintains the desired number of Pods for a particular Pod template. Application releases need more: versioned rollout coordination, rollout status, revision history, and rollback. A Deployment provides this higher-level management.

The ownership model is:

`Deployment → ReplicaSets → Pods`

The Deployment controller coordinates ReplicaSets. Each ReplicaSet controller maintains its own matching Pods. The scheduler assigns Pods to Nodes, and the kubelet works with the container runtime to run their containers.

### 2. Pod-template changes and revisions

A Deployment specifies a replica count, selector, and Pod template. Changing the Pod template—for example, changing a container image from `v1` to `v2`—normally creates a new ReplicaSet and Deployment revision. The Deployment coordinates the transition between the old and new ReplicaSets.

Changes outside the Pod template do not necessarily trigger a new rollout. Revision history is retained according to the Deployment's history-retention configuration; old ReplicaSets are not guaranteed to run old Pods indefinitely.

### 3. Rolling updates

With the default rolling-update strategy, Kubernetes gradually scales the new ReplicaSet up and the old ReplicaSet down. Old and new ReplicaSets may coexist during the rollout. The actual sequence is asynchronous and depends on readiness, capacity, rollout settings, and failures.

Two settings govern the availability/capacity trade-off:

- `maxSurge`: maximum additional replicas allowed above the desired count during the rollout.
- `maxUnavailable`: maximum replicas allowed to be unavailable during the rollout.

These values may be integers or percentages. For the default RollingUpdate strategy, both default to `25%`; surge percentages round up and unavailable percentages round down. These controls do not guarantee that new Pods will become ready or that downtime is impossible.

### 4. Readiness and stalled rollouts

A rollout can stall if new Pods cannot become ready—for example, because of failing readiness probes, image-pull errors, resource shortages, or scheduling constraints. The Deployment may retain old replicas while it cannot safely progress. Inspect the Deployment, ReplicaSets, Pods, and events to diagnose the cause.

Replica count alone does not prove that an application is available. Readiness and application behavior matter.

### 5. Rollout status and history

Useful commands include:

- `kubectl rollout status deployment/<name>` — observe rollout progress.
- `kubectl rollout history deployment/<name>` — inspect recorded revisions.
- `kubectl rollout history deployment/<name> --revision=<n>` — inspect a specific revision when available.

A rollout being initiated is not the same as a successful rollout. Revision history is subject to retention settings.

### 6. Rollback

`kubectl rollout undo deployment/<name>` requests a rollback to the previous revision. `--to-revision=<n>` targets a specific retained revision. The Deployment then reconciles toward the restored Pod template using its rollout strategy.

Rollback is a state-changing operational action. Use it only when authorized and after assessing the impact. Do not practice it on a shared or production cluster without explicit approval.

Rollback does not automatically undo database migrations, external API calls, published messages, or side effects already performed. Restoring an old application image cannot restore a dropped database column or recover deleted data.

## Real World Example

An Orders API has three `v1` replicas. A Deployment template is updated to use `v2`. Kubernetes creates a new ReplicaSet and gradually shifts replicas to it. If new Pods pass readiness checks, the rollout can complete with three `v2` replicas. If they fail readiness checks, progress may stall while old replicas remain available, subject to the rollout strategy and actual health of the application.

## Deep Dive

- **Deployment:** coordinates versioned rollout and rollback.
- **ReplicaSet:** maintains Pods for one Pod template.
- **Rolling update:** shifts replicas gradually between versions.
- **Readiness:** influences whether Pods count as available for rollout progress and traffic eligibility.
- **Rollback boundary:** restores a prior Pod template, not all external system state.
- **Production safety:** compatible database migrations, sufficient capacity, reliable readiness probes, and observable rollout health are essential to safe releases.

## Hands-on Exercise

On a cluster you are authorized to inspect, use the Lesson 108 command reference to list Deployments, observe rollout status, inspect revision history, and compare Deployments, ReplicaSets, and Pods. Do not initiate a rollout or rollback on a shared or production cluster for this exercise. If no cluster is available, explain the expected state transitions for a three-replica `v1` to `v2` update and a failed-readiness scenario.

## Common Misconceptions

- A Deployment manages ReplicaSets; it does not directly manage individual containers.
- Existing Pods are not normally mutated in place to change their container image during a Deployment rollout.
- A rolling update does not guarantee zero downtime.
- Creating a new ReplicaSet does not mean the rollout has completed.
- Old ReplicaSets and revision history are subject to retention behavior.
- Rollback does not reverse database changes or external side effects.

## Summary

A Deployment manages application versions through ReplicaSets. Pod-template changes normally create a new ReplicaSet and revision, and the Deployment coordinates a gradual transition between versions. Rollout status and history aid observation; rollback restores an earlier Pod template but cannot automatically reverse external changes.

## Key Takeaways

- Deployment → ReplicaSets → Pods.
- Pod-template changes normally trigger a new rollout revision.
- `maxSurge` controls extra rollout replicas; `maxUnavailable` controls permitted unavailability.
- Readiness failures or insufficient capacity can stall rollout progress.
- Rollback restores a previous Pod template, not the entire external system state.

## Reflection Questions

1. Why does a Pod-template change normally create a new ReplicaSet?
2. What do `maxSurge` and `maxUnavailable` control for a three-replica Deployment?
3. What can happen to old replicas when new Pods fail readiness checks?
4. What do rollout status and history show, and how is rollback different from manually deleting new Pods?
5. Why might an application still fail after rolling back if the new version dropped a database column?

## What's Next

Lesson 109 — Kubernetes Services: stable network access to changing Pod replicas.
