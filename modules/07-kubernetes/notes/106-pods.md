# Lesson 106 — Kubernetes Pods

## Objectives

- Explain why a Pod is Kubernetes' smallest deployable unit.
- Distinguish Pods from containers and Nodes.
- Describe shared networking, volumes, and scheduling for containers in a Pod.
- Understand Pod phases, replacement, and ephemeral identity.
- Explain how Pods relate to Services and workload controllers.

## Prerequisites

- Lesson 104 — Docker Compose
- Lesson 105 — Kubernetes Architecture

## Theory

### 1. Why Pods?

A Pod is the smallest deployable and schedulable unit in Kubernetes. It contains one or more containers that are placed and managed together on the same Node. Most Pods contain one application container; multiple containers are useful for tightly coupled helpers such as sidecars.

Kubernetes schedules Pods, not individual containers within a Pod.

### 2. What a Pod provides

- **Shared network namespace:** containers in a Pod normally share the Pod IP and can communicate through `localhost`. Processes must avoid conflicting bindings to the same address and port.
- **Shared storage when configured:** containers can mount the same volume. Their container filesystems are not automatically shared.
- **Co-scheduling:** containers in a Pod run on the same Node and are managed within the Pod's lifecycle.

A shared volume such as `emptyDir` can share files for the Pod's lifetime. Persistent storage is needed when data must survive beyond that lifecycle, subject to storage configuration.

### 3. One or multiple containers

Use one container per Pod as the normal default. Multiple containers in one Pod are appropriate when they are tightly coupled and need shared networking, shared volumes, or coordinated placement. Independently scalable application components usually belong in separate Pods.

### 4. Pod lifecycle

1. A Pod object is submitted through the Kubernetes API, directly or by a controller.
2. The scheduler assigns an unscheduled Pod to a suitable Node.
3. The Node's kubelet works with the container runtime to set up and run its containers.
4. Kubernetes reports and observes state; health and readiness are separate from the Pod phase.
5. A Pod can terminate or be deleted. A workload controller may create a replacement Pod.

A Pod does not recreate itself as a new Pod object merely because it was deleted. Container restarts within an existing Pod are a different mechanism.

### 5. Common Pod phases

- `Pending`: accepted, but setup or container startup is not yet complete; scheduling or image pulling may still be in progress.
- `Running`: bound to a Node and containers have been created; at least one container is running or starting/restarting.
- `Succeeded`: all containers completed successfully and will not be restarted.
- `Failed`: all containers have terminated and at least one failed.
- `Unknown`: Kubernetes cannot determine the Pod state, often because of a communication issue with the Node.

`Running` does not necessarily mean the application is ready to receive traffic. Readiness probes and endpoint management help determine whether a Pod should receive traffic.

### 6. Pod networking and identity

Each Pod normally has its own cluster IP. Containers inside that Pod share the Pod's network namespace. Separate Pods can normally listen on the same port because they have different network identities.

Pod IPs are not stable identities: when a Pod is replaced, the new Pod may have a different IP or run on a different Node. A Kubernetes Service provides a stable way to reach a selected group of Pods.

### 7. Storage and replacement

Data written only to a container's writable filesystem should not be assumed to survive Pod replacement. Use an appropriate volume or external data service according to the durability requirements. Persistent storage and backups are separate concerns; a volume alone does not guarantee recoverability.

## Real World Example

An `orders-api` workload runs three Pod replicas across worker Nodes. Each Pod contains one application container listening on port `8080`. A Service selects the Orders Pods and provides a stable address. If a controller replaces one Pod, clients continue using the Service instead of depending on the old Pod IP.

A tightly coupled sidecar could share a Pod with an application container and mount the same volume to process files. If the helper needs independent scaling, it would usually be deployed separately.

## Deep Dive

- **Pod vs. container:** the container runs a process; the Pod is the Kubernetes unit that groups containers and provides shared context.
- **Pod vs. Node:** a Node is a machine; a Pod is scheduled onto one Node.
- **Pod vs. Service:** a Pod is a workload instance; a Service is a stable network abstraction for a set of eligible backends.
- **Pod vs. ReplicaSet:** a Pod is an instance; a ReplicaSet maintains the desired number of matching Pods.
- **Running vs. Ready:** Running describes the Pod phase; readiness determines whether it should receive traffic.

## Hands-on Exercise

Use a cluster you are authorized to access. Inspect Pods, their Nodes, IPs, container status, and events using the commands in [the Lesson 106 command reference](../commands/106-pods.md). Do not delete or modify workloads in a shared or production cluster as part of this exercise.

## Common Misconceptions

- A Pod is not the same thing as a container.
- Containers in a Pod share networking, but do not automatically share their filesystems.
- Two containers in one Pod generally cannot bind to the same address and port simultaneously.
- A Pod IP is not a permanent service address.
- A Running Pod is not necessarily ready to serve requests.
- Deleting a Pod does not itself guarantee a replacement; a controller usually maintains replicas for managed workloads.
- A shared volume does not automatically mean data is persistent or backed up.

## Summary

A Pod groups one or more containers into a single Kubernetes scheduling unit. Its containers share the Pod network namespace and can share explicitly configured volumes. Pods are replaceable, so Services and workload controllers provide stable access and desired replica management.

## Key Takeaways

- Kubernetes schedules Pods onto Nodes.
- Containers within a Pod run together on the same Node and share its Pod-level network identity.
- Volumes must be configured to share files.
- Pod IPs can change when Pods are replaced; Services provide stable access to selected Pods.
- Pod phase, container health, and readiness are distinct concepts.
- Controllers such as ReplicaSets maintain desired Pod counts.

## Reflection Questions

1. Why does Kubernetes schedule Pods rather than scheduling every container independently?
2. Why can two separate Pods normally use port `8080`, while two containers in the same Pod can encounter a port conflict?
3. What must be configured for an application container and a sidecar to share files?
4. How should other applications reach a workload after a Pod's IP changes?
5. Which component maintains three replicas when one Pod managed by a Deployment-based workload is deleted?

## What's Next

Lesson 107 — ReplicaSets: how Kubernetes maintains the desired number of Pod replicas.
