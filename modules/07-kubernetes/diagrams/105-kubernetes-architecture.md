# Lesson 105 — Kubernetes Architecture Diagram

## Cluster Components

```mermaid
flowchart TB
    User[User / kubectl / deployment tool] --> API[kube-apiserver]

    subgraph CP[Control Plane]
        API <--> ETCD[(etcd: cluster state)]
        API <--> SCHED[kube-scheduler]
        API <--> CTRL[kube-controller-manager]
    end

    subgraph W1[Worker Node]
        K1[kubelet]
        R1[Container runtime via CRI]
        P1[Pod and its containers]
        K1 --> R1 --> P1
    end

    subgraph W2[Worker Node]
        K2[kubelet]
        R2[Container runtime via CRI]
        P2[Pod and its containers]
        K2 --> R2 --> P2
    end

    API <--> K1
    API <--> K2
    SCHED -->|assigns Pod to node| API
    CTRL -->|creates or updates API objects| API
```

This diagram is conceptual. Kubernetes components communicate through API interactions and watches; the flow is asynchronous rather than a single linear function call.

## Desired-State Reconciliation

```mermaid
flowchart TD
    A[Desired state: 3 replicas] --> B[Controllers observe cluster state]
    B --> C{Actual state matches desired state?}
    C -->|Yes| D[Continue observing]
    C -->|No| E[Create or update API objects]
    E --> F[Scheduler assigns unscheduled Pods]
    F --> G[Kubelet and runtime attempt execution]
    G --> H[Cluster reports observed state]
    H --> B
```

Reconciliation repeatedly attempts to reduce the difference between desired and actual state. It cannot guarantee convergence when constraints or failures prevent progress.

## When Capacity Is Insufficient

```mermaid
flowchart TD
    A[Pod needs scheduling] --> B[Scheduler evaluates nodes and constraints]
    B --> C{Suitable node available?}
    C -->|Yes| D[Pod assigned to a node]
    C -->|No| E[Pod remains unscheduled / Pending]
    E --> F[Investigate requests and constraints]
    F --> G[Free resources, adjust valid requests, or add capacity]
```

A Pending Pod caused by insufficient scheduling capacity is different from a container that starts and later exceeds its memory limit.
