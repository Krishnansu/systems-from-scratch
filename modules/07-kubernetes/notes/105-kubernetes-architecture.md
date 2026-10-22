# Lesson 105 — Kubernetes Architecture

## Learning Objectives

By the end of this lesson, you should be able to:

- Explain why Kubernetes orchestration is useful beyond running containers with Docker Compose.
- Describe the roles of the control plane and worker nodes.
- Explain how the API server, etcd, scheduler, controllers, kubelet, and container runtime interact.
- Trace how Kubernetes attempts to run a requested workload.
- Explain desired state, actual state, and reconciliation.
- Recognize why a Pod can remain Pending when cluster capacity is insufficient.

## Prerequisites

- Lesson 96 — Why Containers?
- Lesson 99 — Dockerfile
- Lesson 103 — Docker Networks
- Lesson 104 — Docker Compose

## 1. Why Kubernetes?

Docker runs containers. Docker Compose describes and coordinates related containers, commonly on a single host. Kubernetes orchestrates workloads across a cluster of machines.

Kubernetes helps manage workload placement, replacement of failed Pods, scaling toward a requested replica count, and reconciliation between declared and observed state.

Orchestration does not guarantee that an application is correct, that capacity is unlimited, or that application data is durable.

## 2. Cluster Mental Model

A Kubernetes cluster has two major parts:

- **Control plane:** maintains cluster state and coordinates decisions about workloads.
- **Worker nodes:** provide the environment where Pods run.

See [the Kubernetes architecture diagram](../diagrams/105-kubernetes-architecture.md).

## 3. Control Plane Components

- **kube-apiserver:** the primary interface to the Kubernetes API. It validates and exposes API operations and coordinates persisted cluster state.
- **etcd:** the consistent key-value store that persists Kubernetes cluster state. It is not a replacement for an application's business database.
- **kube-scheduler:** selects a suitable node for each unscheduled Pod, considering scheduling requirements and available resources.
- **kube-controller-manager:** runs controllers that observe cluster state and take actions to move actual state toward desired state.
- **cloud-controller-manager (when used):** integrates Kubernetes with cloud-provider functionality such as certain node and load-balancer operations.

These components have distinct responsibilities. For example, the scheduler chooses a node; it does not start the container on that node.

## 4. Worker Node Components

- **kubelet:** the node agent that ensures assigned Pods are run according to their specifications and reports relevant status to the control plane.
- **Container runtime:** runs containers. Kubernetes interacts with supported runtimes through the Container Runtime Interface (CRI).
- **Networking components:** provide Pod connectivity and service networking. kube-proxy is a common implementation component, but some cluster networking implementations replace its role.

A Pod is the Kubernetes workload unit scheduled onto a node. A Pod can contain one or more closely related containers.

## 5. What Happens When You Request a Workload?

A simplified flow for a workload that requests replicas is:

1. A user or deployment tool submits the desired configuration to the API server.
2. The API server validates the request and cluster state is persisted through etcd.
3. Controllers observe that the requested workload needs Pods and create the corresponding Pod objects.
4. The scheduler selects suitable nodes for Pods that do not yet have a node assignment.
5. The kubelet on each selected node observes its assigned Pods and works with the container runtime to run their containers.
6. Node and control-plane components report state; controllers continue reconciling differences.

This is a conceptual flow, not a single synchronous transaction. Components watch state and act asynchronously, so the requested state may take time to become reality.

## 6. Desired State and Reconciliation

Kubernetes is designed around a desired-state model:

- **Desired state:** what the configuration requests, such as three replicas.
- **Actual state:** what the cluster currently observes, such as two running Pods.
- **Reconciliation:** controllers repeatedly compare observed state with desired state and take actions to reduce the difference.

If a managed Pod disappears, a controller may create a replacement Pod. The replacement is a new Pod object; Kubernetes does not necessarily restart the same Pod object.

Reconciliation is an ongoing process, not a guarantee that the desired state can always be achieved immediately.

## 7. Scheduling and Capacity Constraints

The scheduler evaluates whether a node is suitable for a Pod, including resource requests and other scheduling constraints. If no node is suitable, the Pod can remain unscheduled in a Pending state.

Kubernetes cannot conjure additional memory or CPU capacity. Possible responses include freeing resources, adding worker capacity, or correcting an unnecessarily high resource request. Cluster autoscaling may add nodes when configured and supported, but it is not an unconditional guarantee.

Do not confuse two situations:

- **Insufficient scheduling capacity:** a Pod cannot be placed on a suitable node.
- **Runtime memory-limit failure:** a container starts but later exceeds its configured memory limit.

These occur at different stages and require different diagnosis.

## 8. State and Data Boundaries

etcd stores Kubernetes cluster state, such as Kubernetes API objects. Application business data belongs in the application's database or other appropriate data store.

Kubernetes can manage workloads that use persistent storage, but orchestration by itself does not guarantee that application data is backed up, replicated, or recoverable.

## Common Misconceptions

- **Kubernetes is just a container runtime:** No. It orchestrates workloads across a cluster and relies on a container runtime to run containers.
- **The scheduler starts containers:** No. It assigns Pods to nodes; the node's kubelet coordinates with the runtime to run them.
- **A controller runs containers directly:** No. Controllers reconcile API objects; scheduling and node execution involve other components.
- **etcd stores all application data:** No. It stores Kubernetes cluster state, not an application's general business records.
- **Kubernetes always makes every requested replica run:** No. Scheduling constraints, insufficient capacity, image failures, and other problems can prevent the desired state from being reached.
- **Kubernetes automatically adds machines whenever needed:** No. Additional capacity requires suitable infrastructure and autoscaling configuration, if available.
- **A replacement Pod is the same Pod restarted:** Typically not. A controller creates a replacement Pod object when required.

## Key Takeaways

- A Kubernetes cluster consists of a control plane and worker nodes.
- The API server is the main API entry point; etcd persists cluster state.
- Controllers reconcile desired and actual state.
- The scheduler selects a node; kubelet and the container runtime handle execution on that node.
- Kubernetes continuously works toward desired state, but resource constraints and failures can prevent immediate convergence.
- Cluster state and application business data are separate concerns.

## Reflection Questions

1. What does Kubernetes add beyond running containers with Docker Compose?
2. What is the difference between the scheduler and kubelet, and how does the container runtime fit into their responsibilities?
3. If a managed Pod disappears, which component notices the replica mismatch and what happens next?
4. What kind of state does etcd persist, and why is it not the application's business database?
5. What can happen when no worker node has enough suitable capacity to schedule a Pod?

## Next Lesson

Lesson 106 — Pods: the smallest deployable unit in Kubernetes, and why Kubernetes schedules Pods rather than individual containers.
