# Kubernetes Command References

This directory contains practical command references that accompany the Kubernetes lessons. Use them as quick references; consult lesson notes for the concepts and trade-offs behind each command.

## Lessons

- [106 — Pods](106-pods.md)
- [107 — ReplicaSets](107-replicasets.md)
- [108 — Deployments](108-deployments.md)
- [109 — Services](109-services.md)

## General Safety Notes

- Check your current context and namespace before running commands against a cluster.
- Use read-only inspection commands for introductory exercises.
- Treat rollout undo, apply, delete, scale, and exposure commands as state-changing operations requiring authorization.
- Avoid changing resources in shared or production clusters unless explicitly authorized.
- Treat logs, YAML output, events, and configuration details as potentially sensitive.
