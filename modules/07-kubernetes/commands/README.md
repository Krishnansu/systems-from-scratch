# Kubernetes Command References

This directory contains practical command references that accompany the Kubernetes lessons. Use them as quick references; consult lesson notes for the concepts and trade-offs behind each command.

## Lessons

- [106 — Pods](106-pods.md)
- [107 — ReplicaSets](107-replicasets.md)
- [108 — Deployments](108-deployments.md)
- [109 — Services](109-services.md)
- [110 — Ingress](110-ingress.md)
- [111 — ConfigMaps](111-configmaps.md)
- [112 — Secrets](112-secrets.md)
- [113 — Persistent Volumes](113-persistent-volumes.md)
- [114 — Autoscaling](114-autoscaling.md)
- [115 — Scheduling](115-scheduling.md)
- [116 — Health Checks and Probes](116-health-checks-and-probes.md)
- [117 — Kubernetes Workload Types](117-workload-types.md)
- [118 — Resource Management, QoS, and Eviction](118-resource-management-qos-and-eviction.md)

## General Safety Notes

- Check your current context and namespace before running commands against a cluster.
- Use read-only inspection commands for introductory exercises.
- Treat rollout undo, apply, delete, scale, and exposure commands as state-changing operations requiring authorization.
- Treat Secret values, logs, YAML output, events, and configuration details as potentially sensitive.
- Inspect reclaim policies and confirm ownership before deleting storage resources.
- Avoid changing shared or production resources unless explicitly authorized.
- Begin autoscaling and scheduling troubleshooting with read-only inspection; do not change shared workload policies, labels, taints, or placement rules without authorization.
