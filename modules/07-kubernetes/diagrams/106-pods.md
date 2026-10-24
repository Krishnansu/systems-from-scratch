# Lesson 106 — Kubernetes Pods Diagrams

## Node, Pod, and Containers

```mermaid
flowchart TB
    subgraph NODE[Worker Node]
        subgraph POD[Pod: orders-api]
            APP[Application container]
            SIDE[Optional sidecar container]
            NET[Shared Pod network namespace and IP]
            VOL[Shared volume when configured]
            APP --- NET
            SIDE --- NET
            APP --- VOL
            SIDE --- VOL
        end
    end
```

A Pod is scheduled as one unit on a Node. Containers share its network namespace; they share files only through configured volumes.

## Pod IPs and Service

```mermaid
flowchart TD
    CLIENT[Client] --> SVC[Stable Kubernetes Service]
    SVC --> P1[Orders Pod 1\nPod IP A]
    SVC --> P2[Orders Pod 2\nPod IP B]
    SVC --> P3[Orders Pod 3\nPod IP C]
```

The Service selects eligible Pods and provides a stable access point while individual Pod IPs may change.

## Simplified Pod Lifecycle

```mermaid
flowchart TD
    A[Pod object created] --> B[Scheduler assigns Node]
    B --> C[Kubelet and runtime set up containers]
    C --> D[Pod runs; readiness is assessed separately]
    D --> E[Pod terminates or is deleted]
    E --> F{Controller maintains replicas?}
    F -->|Yes| G[Controller creates replacement Pod]
    F -->|No| H[No automatic replacement guaranteed]
```

A replacement is a new Pod object and may have a different IP address or Node.
