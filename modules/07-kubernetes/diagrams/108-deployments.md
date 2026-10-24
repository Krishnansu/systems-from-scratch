# Lesson 108 — Deployments Diagrams

## Ownership hierarchy

```mermaid
flowchart TD
    D[Deployment controller] --> RS1[Old ReplicaSet: v1]
    D --> RS2[New ReplicaSet: v2]
    RS1 --> P1[Old Pods]
    RS2 --> P2[New Pods]
```

The Deployment coordinates ReplicaSets; each ReplicaSet maintains its own Pods.

## Rolling update concept

```mermaid
flowchart TD
    A[Deployment template uses v1] --> B[Change template to v2]
    B --> C[Create new ReplicaSet for v2]
    C --> D[Scale new and old ReplicaSets according to rollout strategy]
    D --> E{Are new replicas becoming available?}
    E -->|Yes| F[Continue shifting replicas]
    F --> G[Rollout completes with v2]
    E -->|No| H[Rollout may stall; inspect health and events]
```

## Rollback concept

```mermaid
flowchart TD
    A[Release v2] --> B{Problem detected?}
    B -->|No| C[Continue monitoring]
    B -->|Yes| D[Authorized operator requests rollback]
    D --> E[Deployment restores an earlier Pod template]
    E --> F[Controllers reconcile toward the earlier version]
    F --> G[Validate application and external dependencies]
```

Rollback restores a Pod template, not database state or external side effects.
