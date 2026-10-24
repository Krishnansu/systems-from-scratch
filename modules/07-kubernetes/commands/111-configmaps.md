# Lesson 111 — ConfigMaps Command Reference

Use these commands only against a local or authorized cluster. Inspect the current context and namespace first. YAML and configuration output may reveal sensitive operational details.

## Inspect ConfigMaps

```bash
kubectl config current-context
kubectl get configmaps
kubectl get configmap orders-config
kubectl describe configmap orders-config
kubectl get configmap orders-config -o yaml
kubectl get configmap orders-config -o json
```

ConfigMaps are namespaced. Use `-n <namespace>` to inspect a specific namespace and `-A` to list resources across namespaces.

## Inspect workloads and events

```bash
kubectl get pods
kubectl get deployments
kubectl describe pod <pod-name>
kubectl describe deployment <deployment-name>
kubectl get events --sort-by=.metadata.creationTimestamp
```

Check Pod events, container state, and the workload's configuration references. If authorized, inspect the Pod specification to verify the referenced ConfigMap name, key, environment-variable mapping, or volume mount.

## Troubleshooting checklist

1. Verify the active cluster context and namespace.
2. Confirm the ConfigMap exists in the Pod's namespace.
3. Check that the required key exists and is spelled correctly.
4. Check Pod events and container startup status for missing references.
5. Determine whether configuration is consumed as environment variables or mounted files.
6. For environment variables, confirm whether the container restarted after the value changed.
7. For mounted files, allow for projection delay; check whether the application reloads the file and whether `subPath` is used.
8. Check application logs and configuration validation errors, treating output as potentially sensitive.

## Safe cleanup

Only if the ConfigMap was created for your own exercise and no workload depends on it:

```bash
kubectl delete configmap orders-config
```

Do not delete shared or production configuration without explicit authorization.
