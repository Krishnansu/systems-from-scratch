# Kubernetes Command References

This directory contains practical command references that accompany the Kubernetes lessons. Use them as quick references; consult lesson notes for the concepts and trade-offs behind each command.

## Lessons

- [106 — Pods](106-pods.md)
- [107 — ReplicaSets](107-replicasets.md)

## General Safety Notes

- Check your current context and namespace before running commands against a cluster.
- Use read-only inspection commands for introductory exercises.
- Avoid deleting or changing resources in shared or production clusters unless explicitly authorized.
- Treat logs, YAML output, and configuration details as potentially sensitive.
