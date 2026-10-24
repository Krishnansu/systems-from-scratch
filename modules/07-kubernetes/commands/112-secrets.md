# Lesson 112 — Secrets Command Reference

Use these commands only against a local or authorized cluster. Confirm the current context and namespace first. Secret output may expose sensitive values; do not print or share credential material.

## Inspect Secret resources

```bash
kubectl config current-context
kubectl get secrets
kubectl get secret orders-db-secret
kubectl describe secret orders-db-secret
```

`describe` normally shows key names and data sizes rather than printing their values. Avoid `kubectl get secret orders-db-secret -o yaml` in shared terminals or logs because the output may contain Base64-encoded credentials.

## Inspect workload references

```bash
kubectl get pods
kubectl describe pod <pod-name>
kubectl get pod <pod-name> -o yaml
kubectl get events --sort-by=.metadata.creationTimestamp
kubectl get deployments
kubectl describe deployment <deployment-name>
```

Inspect the workload specification and events to verify the Secret name, namespace, key references, and volume mounts. Treat YAML output and diagnostic data as potentially sensitive.

## Troubleshooting checklist

1. Verify cluster context and namespace.
2. Confirm the Secret exists in the Pod's namespace.
3. Check the Secret key name and the Pod's reference.
4. Review Pod events and container startup errors for missing Secrets or keys.
5. Determine whether the value is delivered as an environment variable or mounted file.
6. For environment variables, determine whether the container restarted after the Secret changed.
7. For mounted files, allow for projection delay; check application reload behavior and whether `subPath` is used.
8. For credential rotation, verify the application loaded the new value and refreshed connections as required, without logging the credential itself.
9. Check RBAC and cluster encryption-at-rest configuration through authorized administrative procedures.

## Safe cleanup

Delete only test resources you created and confirmed are unused. Do not delete shared or production Secrets without explicit authorization.
