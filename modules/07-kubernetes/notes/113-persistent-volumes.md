# Lesson 113 — Kubernetes Persistent Volumes

## Objectives

- Explain why Pod-local storage is not sufficient for durable application data.
- Distinguish PersistentVolumes (PVs), PersistentVolumeClaims (PVCs), and StorageClasses.
- Explain static and dynamic provisioning.
- Understand access modes, claim binding, and reclaim policies.
- Troubleshoot PVC provisioning and volume mounting.

## Prerequisites

- Lessons 106–112: Pods, ReplicaSets, Deployments, Services, Ingress, ConfigMaps, and Secrets.
- Docker volumes and basic Kubernetes YAML.

## Theory

Pods are replaceable compute units. Data written only to a container's writable layer should not be expected to survive container or Pod replacement. Kubernetes storage resources separate workload lifecycle from storage lifecycle.

- **PersistentVolume (PV):** A cluster storage resource representing provisioned storage, created statically or dynamically.
- **PersistentVolumeClaim (PVC):** A namespaced request for storage. Pods normally reference a PVC rather than naming a PV directly.
- **StorageClass:** Describes a class of storage and its provisioner and parameters. It enables dynamic provisioning when supported and configured.

A PVC binds to a compatible PV. If no suitable PV is available and provisioning cannot succeed, the claim may remain `Pending`.

### PVC example

```yaml
apiVersion: v1
kind: PersistentVolumeClaim
metadata:
  name: orders-data
spec:
  accessModes:
    - ReadWriteOnce
  storageClassName: standard
  resources:
    requests:
      storage: 1Gi
```

The StorageClass name is cluster-specific. Inspect available classes before applying this example. A claim is a request, not proof that storage has been successfully provisioned and mounted.

### Pod volume reference

```yaml
spec:
  containers:
    - name: app
      image: busybox:1.36
      command: ["sh", "-c", "echo durable-data > /data/message.txt; sleep 3600"]
      volumeMounts:
        - name: orders-storage
          mountPath: /data
  volumes:
    - name: orders-storage
      persistentVolumeClaim:
        claimName: orders-data
```

When a Pod is replaced, another Pod can access existing data by referencing the same PVC, provided the backing storage remains available and can be mounted.

### Provisioning

- **Static:** An administrator provisions PVs ahead of time.
- **Dynamic:** A PVC requests a StorageClass and a configured provisioner creates suitable storage.

### Access modes

- `ReadWriteOnce` (RWO): read-write mounting from a single node; multiple Pods on that node may still use it, depending on the volume and setup.
- `ReadOnlyMany` (ROX): read-only mounting from multiple nodes, if supported.
- `ReadWriteMany` (RWX): read-write mounting from multiple nodes, if supported.
- `ReadWriteOncePod` (RWOP): read-write use by a single Pod, when supported.

Access modes describe supported mounting patterns and are not a complete security mechanism. Backend capabilities vary.

### Reclaim policies

- `Retain`: preserve the PV and underlying data for manual recovery or cleanup.
- `Delete`: the PV and backing storage may be deleted, depending on the provisioner and storage type.

Dynamically provisioned PVs often inherit a reclaim policy from their StorageClass. Inspect policies before deleting claims containing valuable data.

## Real World Example

An orders service writes uploaded documents to a PVC-backed mount. When a Pod is replaced, a replacement Pod references the same claim and can access the existing files if the storage is healthy and mountable. The team still needs backups, recovery tests, capacity monitoring, and appropriate access controls.

## Deep Dive

- PVs are cluster-scoped; PVCs are namespaced.
- A Pod normally references a PVC in its own namespace.
- Pod deletion does not normally delete a separate PVC.
- Persistence does not guarantee backup, replication, or disaster recovery.
- `ReadWriteOnce` is node-oriented, not a guarantee of one Pod only.
- A `Pending` PVC may indicate a missing StorageClass, unavailable compatible PV, provisioner failure, capacity constraints, or topology issues.
- A `Bound` PVC does not guarantee that a Pod can successfully mount the volume.
- StatefulSet policies and automation can influence PVC lifecycle; inspect the actual configuration before deleting resources.

## Hands-on Exercise

Inspect storage using a local or authorized cluster. Start with read-only commands:

```bash
kubectl config current-context
kubectl get storageclass
kubectl get pvc -A
kubectl get pv
kubectl get pvc
kubectl describe pvc <claim-name>
kubectl get events --sort-by=.metadata.creationTimestamp
```

For a `Pending` claim, check the requested StorageClass, access mode, capacity, compatible PVs, provisioning configuration, events, provisioner health, and topology constraints. For a Pod that cannot mount a bound claim, inspect Pod events and storage-driver status as well.

Only create or delete test resources in a disposable or authorized environment. Never delete shared or production storage as part of this exercise.

## Common Misconceptions

- A PVC is the physical disk rather than a request for storage.
- Persistent storage automatically means backed up or replicated.
- `ReadWriteOnce` means exactly one Pod.
- Every PVC provisions storage immediately.
- A bound claim guarantees a successful volume mount.
- Deleting a Pod normally deletes its separate PVC.

## Summary

Kubernetes separates replaceable compute from storage through PVs, PVCs, and StorageClasses. Claims request storage, PVs represent provisioned resources, and StorageClasses can enable dynamic provisioning. Durability and access behavior depend on the underlying storage system and its configuration.

## Key Takeaways

- Pods normally consume persistent storage through PVCs.
- PVCs can outlive Pod replacement and allow a new Pod to reuse data.
- Access modes describe supported mounting patterns, not complete security controls.
- Reclaim policies affect storage lifecycle after a claim is released.
- Persistence is not backup or disaster recovery.
- Troubleshoot provisioning and mounting as separate stages.

## Reflection Questions

1. What is the difference between a PV, PVC, and StorageClass?
2. Why is a PVC useful when Pods are replaceable?
3. What is the difference between static and dynamic provisioning?
4. Does `ReadWriteOnce` mean only one Pod can mount a volume? Explain.
5. A PVC is `Pending`. What would you investigate, and why might a claim that is `Bound` still fail to mount in a Pod?

## What's Next

Lesson 114 — Kubernetes Autoscaling: responding to changing workload demand and distinguishing workload scaling from cluster capacity scaling.
