# Lesson 112 — Kubernetes Secrets

## Objectives

- Explain why Kubernetes Secrets exist.
- Create and inspect Secrets safely.
- Consume Secret values through environment variables and mounted files.
- Distinguish Base64 encoding from encryption.
- Understand RBAC, encryption at rest, runtime access, and credential rotation.

## Prerequisites

- Lessons 106–111: Pods, ReplicaSets, Deployments, Services, Ingress, and ConfigMaps.
- Basic Kubernetes YAML and `kubectl`.

## Theory

A Kubernetes Secret is a namespaced API object intended to hold sensitive data such as passwords, tokens, and credentials. It separates sensitive configuration from application code and ordinary configuration, but does not automatically make the data secure.

```yaml
apiVersion: v1
kind: Secret
metadata:
  name: orders-db-secret
type: Opaque
stringData:
  DB_USERNAME: orders_service
  DB_PASSWORD: replace-with-a-real-secret
```

`stringData` accepts strings and Kubernetes converts them into the Secret's stored data representation. The `data` field uses Base64 encoding. Base64 is not encryption. Never commit real credentials to source control or embed them in images.

### Consuming a Secret

Environment variable:

```yaml
env:
  - name: DB_PASSWORD
    valueFrom:
      secretKeyRef:
        name: orders-db-secret
        key: DB_PASSWORD
```

A Secret can also be mounted as files:

```yaml
volumeMounts:
  - name: db-credentials
    mountPath: /etc/orders/credentials
    readOnly: true
volumes:
  - name: db-credentials
    secret:
      secretName: orders-db-secret
```

Secret keys become files in the mounted directory. Environment variables in existing containers do not update when the Secret changes. Mounted files update eventually, but the application must reread or reload them. A `subPath` mount does not receive automatic updates.

## Real World Example

An orders service obtains its database username and password from a Secret. When the database password rotates, the team updates the Secret and coordinates application reload or Pod rollout with database connection refresh. Updating the Secret alone does not guarantee that existing connections or application configuration use the new credential.

## Deep Dive

- Secrets are namespaced; normal Pod references target a Secret in the same namespace.
- `Opaque` is a common Secret type for arbitrary application key-value data.
- Base64 encoding is reversible and provides no confidentiality.
- RBAC controls who can read or modify Secret objects through the Kubernetes API.
- Encryption at rest protects stored Secret data when configured appropriately for the cluster.
- Runtime processes that need a credential can still read it; restrict access and avoid logging or exposing values.
- Secret updates do not generally trigger a Deployment rollout.
- A mounted file update is useful only if the application reloads it; connection pools may also need refreshing after credential rotation.
- For production, consider protected secret-management systems and deployment pipelines instead of committing plaintext credential manifests.

## Hands-on Exercise

Use a local or authorized test cluster and a dummy credential. Create a Secret, inspect its metadata, and consume a key through an environment variable or mounted file.

```bash
kubectl config current-context
kubectl get secrets
kubectl describe secret orders-db-secret
kubectl get pod <pod-name> -o yaml
kubectl describe pod <pod-name>
kubectl get events --sort-by=.metadata.creationTimestamp
```

Avoid printing Secret values or using `kubectl get secret ... -o yaml` casually, because output may expose credential material. Verify behavior using a dummy value and a test workload. Delete only resources created for the exercise and no longer in use.

## Common Misconceptions

- Base64 encoding is encryption.
- Creating a Secret automatically secures every copy of the credential.
- Only cluster administrators can read Secrets.
- Updating a Secret automatically restarts Pods or refreshes environment variables.
- A read-only Secret mount prevents processes from reading the mounted values.
- Updating a credential automatically refreshes existing application connections.

## Summary

Kubernetes Secrets provide a standard mechanism for sensitive configuration, but their protection depends on permissions, storage configuration, runtime access, and careful handling. Environment-variable and mounted-file consumption have different update behavior, and credential rotation must be coordinated with the application.

## Key Takeaways

- Use ConfigMaps for non-sensitive settings and Secrets for credentials.
- Base64 is encoding, not encryption.
- Use least-privilege RBAC and appropriate encryption at rest.
- Secret changes do not automatically refresh environment variables or trigger a rollout.
- Credential rotation must account for application reloads and existing connections.

## Reflection Questions

1. What distinguishes a ConfigMap from a Secret, and does a Secret automatically encrypt its values?
2. What happens when a Secret changes if a Pod consumes it as an environment variable versus a mounted file?
3. Why are RBAC and encryption at rest separate controls?
4. If one Pod can read a Secret, can every Pod in the namespace necessarily read it?
5. What would you investigate if database authentication fails after a password rotation?

## What's Next

Lesson 113 — Kubernetes Persistent Volumes: durable storage, PersistentVolumes, PersistentVolumeClaims, and StorageClasses.
