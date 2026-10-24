# Lesson 107 — ReplicaSets Diagrams

## Desired State and Reconciliation

```mermaid
flowchart TD
    A[ReplicaSet specification: replicas = 3] --> B[ReplicaSet controller observes matching Pods]
    B --> C{Actual count equals desired count?}
    C -->|Too few| D[Create Pods from template]
    C -->|Too many| E[Reduce Pods in the set]
    C -->|Equal| F[No replica-count correction needed]
    D --> G[Scheduler assigns suitable Nodes]
    G --> H[Kubelet and runtime run containers]
    E --> B
    H --> B
    F --> B
```

Reconciliation repeats over time. Creating a Pod object does not guarantee that it will be scheduled or become Ready.

## Deployment, ReplicaSet, and Pods

```mermaid
flowchart TD
    DEP[Deployment] --> RS[ReplicaSet for a Pod template]
    RS --> P1[Pod A]
    RS --> P2[Pod B]
    RS --> P3[Pod C]
    DEP -. manages rollout and revisions .-> RS
```

A Deployment manages ReplicaSets to provide rollout and rollback behavior. A ReplicaSet maintains the desired count of Pods for its template.

## Pod Replacement

```mermaid
flowchart LR
    A[Three matching Pods] --> B[One Pod disappears]
    B --> C[ReplicaSet observes two]
    C --> D[New Pod object created]
    D --> E[Scheduler selects Node]
    E --> F[Kubelet and runtime start containers]
    F --> G[Readiness assessed separately]
```

The replacement is a new Pod object and may have a different IP address or Node.
