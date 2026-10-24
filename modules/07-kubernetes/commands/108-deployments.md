# Lesson 108 — Deployments Command Reference

Use these commands only against a cluster and namespace you are authorized to inspect. Replace example names and revision numbers with values from your environment.

## Inspect Deployments and their resources

```bash
kubectl get deployments
kubectl describe deployment <deployment-name>
kubectl get deployments,replicasets,pods
```

Compare the Deployment, its ReplicaSets, and the Pods they manage. The Deployment's desired state does not guarantee all Pods are ready.

## Observe rollout progress

```bash
kubectl rollout status deployment/<deployment-name>
kubectl get deployment <deployment-name>
kubectl get replicasets
kubectl get pods
```

Rollout status helps determine whether a rollout is progressing or complete. If it stalls, inspect Deployment conditions and events, Pod readiness, image-pull failures, scheduling constraints, and resource availability.

## Inspect revision history

```bash
kubectl rollout history deployment/<deployment-name>
kubectl rollout history deployment/<deployment-name> --revision=<revision-number>
```

History availability depends on retained revisions and the Deployment's history-retention configuration.

## Understand rolling-update settings

Inspect the Deployment's strategy in its YAML:

```bash
kubectl get deployment <deployment-name> -o yaml
```

Look for `spec.strategy`, `maxSurge`, and `maxUnavailable`. A rolling update can temporarily have more Pods than desired or allow some replicas to be unavailable. Neither setting guarantees new Pods will become ready.

## Rollback — state-changing commands

```bash
kubectl rollout undo deployment/<deployment-name>
kubectl rollout undo deployment/<deployment-name> --to-revision=<revision-number>
```

These commands change cluster state. Run them only when explicitly authorized, after assessing impact and following your team's release procedures. Do not use them as part of a read-only exercise or on production/shared workloads without approval.

Rollback restores an earlier Pod template; it does not automatically undo database migrations, external API calls, messages, or other side effects.

## Troubleshooting checklist

1. Check rollout status and Deployment conditions.
2. Compare desired, current, updated, and available replicas.
3. Inspect ReplicaSets and Pod states.
4. Review events, readiness probes, image-pull errors, scheduling constraints, and resource requests.
5. Confirm whether dependencies and database schemas remain compatible with the target version.
6. Follow authorized release/rollback procedures before changing cluster state.

## Safety

- Check the current Kubernetes context and namespace before running commands.
- Treat YAML, events, logs, and configuration output as potentially sensitive.
- The inspection commands above are read-only; rollback commands are not.
- Avoid changing resources in shared or production clusters without explicit authorization.

## Related Lessons

- [106 — Pods](106-pods.md)
- [107 — ReplicaSets](107-replicasets.md)
- [108 — Deployments](../notes/108-deployments.md)
- [109 — Services](../notes/109-services.md) (upcoming)
