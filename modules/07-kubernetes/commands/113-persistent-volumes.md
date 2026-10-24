# Lesson 113 — Persistent Volumes Command Reference

Use these commands against a local or authorized cluster. Confirm the current context and namespace before investigating resources. Storage deletion can cause data loss.

## Discover storage configuration

```bash
kubectl config current-context
kubectl get storageclass
kubectl describe storageclass <storage-class-name>
kubectl get pv
kubectl get pvc
kubectl get pvc -A
```

PVs are cluster-scoped. PVCs are namespaced. Use `-n <namespace>` for a specific namespace and `-A` to list claims across namespaces.

## Inspect a claim and its backing volume

```bash
kubectl describe pvc <claim-name>
kubectl get pvc <claim-name> -o yaml
kubectl describe pv <pv-name>
kubectl get pv <pv-name> -o yaml
```

Inspect claim status, requested capacity, access modes, StorageClass, binding, events, and reclaim policy. YAML may expose operational details; handle output appropriately.

## Inspect Pod mounting

```bash
kubectl get pods
kubectl describe pod <pod-name>
kubectl get pod <pod-name> -o yaml
kubectl get events --sort-by=.metadata.creationTimestamp
```

Check the Pod's PVC reference, volume mounts, namespace, Pod events, and storage-driver messages. A PVC can be `Bound` even when a Pod cannot mount it successfully.

## Troubleshooting a Pending PVC

1. Verify cluster context and namespace.
2. Confirm the requested StorageClass exists.
3. Check requested capacity and access modes.
4. Determine whether a compatible PV is available or dynamic provisioning is configured.
5. Review PVC events and provisioner/CSI-driver health.
6. Check capacity, topology, and scheduling constraints.
7. If the claim is bound but mounting fails, inspect Pod events and storage attachment/mount errors.

## Safety

- Begin with read-only inspection.
- Use a disposable local cluster for creation/deletion exercises.
- Inspect reclaim policy and confirm ownership before deleting a PVC or PV.
- Never delete shared or production claims or volumes without explicit authorization and an approved recovery plan.
- Persistent storage is not a substitute for backups or restore testing.
