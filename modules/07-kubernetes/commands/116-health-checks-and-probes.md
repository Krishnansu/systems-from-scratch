# Lesson 116 — Health Checks and Probes Command Reference

Use read-only inspection commands on a local or authorized cluster.

## Inspect probe status and events

```bash
kubectl get pods
kubectl describe pod <pod-name>
kubectl get events --sort-by=.metadata.creationTimestamp
kubectl get endpointslices
```

Check Pod conditions, restart counts, probe events, and whether the Pod is represented among ready Service endpoints. Use the appropriate namespace when needed.

## Inspect container logs

```bash
kubectl logs <pod-name>
kubectl logs <pod-name> --previous
```

`--previous` retrieves logs from the previous container instance when available, which is useful after probe-triggered restarts.

## Troubleshooting

1. Confirm the Pod and namespace.
2. Inspect `kubectl describe pod` for probe failures and events.
3. Check current and previous logs.
4. Verify the probe path, port, protocol, thresholds, and expected response.
5. For readiness issues, inspect Pod readiness and Service EndpointSlices.
6. Avoid changing probe thresholds before identifying the underlying failure.

## Safety

- These commands are read-only inspections.
- Avoid editing or restarting shared or production workloads without authorization.
- Do not expose sensitive application details from logs or events.
