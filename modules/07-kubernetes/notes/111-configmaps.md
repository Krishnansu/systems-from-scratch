# Lesson 111 — Kubernetes ConfigMaps

## Objectives

- Explain why configuration should be separated from application images.
- Understand ConfigMaps and their key-value data.
- Inject configuration through environment variables and mounted files.
- Explain ConfigMap update behavior.
- Distinguish ConfigMaps from Secrets.

## Prerequisites

- Lessons 106–110: Pods, ReplicaSets, Deployments, Services, and Ingress.
- Docker images and environment variables.
- Basic Kubernetes YAML.

## Theory

A ConfigMap is a namespaced Kubernetes API object for non-confidential configuration data. It separates environment-specific settings from application images, allowing the same image to be deployed with different configuration.

```yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: orders-config
data:
  APP_ENV: "production"
  LOG_LEVEL: "info"
  API_BASE_URL: "https://api.example.com"
```

ConfigMaps can also store file-like text content using multiline values. Their `data` field contains UTF-8 strings; `binaryData` supports base64-encoded binary values.

### Consuming configuration

**Environment variable:**

```yaml
env:
  - name: APP_ENV
    valueFrom:
      configMapKeyRef:
        name: orders-config
        key: APP_ENV
```

`envFrom` can import eligible keys from a whole ConfigMap. Environment variables are established at container start and do not update in an existing container when the ConfigMap changes.

**Mounted files:**

```yaml
volumeMounts:
  - name: app-config
    mountPath: /etc/orders
    readOnly: true
volumes:
  - name: app-config
    configMap:
      name: orders-config
```

ConfigMap keys become files in the mounted directory. Projected files update eventually, but applications must reload them to use new values. A ConfigMap mounted through `subPath` does not receive automatic updates. Mounting over an existing directory can hide image files at that path.

### Updates and rollouts

Updating a ConfigMap alone does not generally change a Deployment's Pod template or trigger a rollout. A changed environment variable requires a container restart to be picked up. For mounted files, Kubernetes projection and application reload behavior determine when new values take effect. A rollout, checksum annotation, or application-supported reload can be used deliberately.

### ConfigMap vs Secret

Use ConfigMaps for non-confidential settings and Secrets for passwords, tokens, and other sensitive values. Secret data is base64-encoded by default, not thereby encrypted; use suitable RBAC, encryption at rest, and careful access controls.

## Real World Example

Multiple replicas of the same orders-service image consume environment-specific API URLs and logging settings through a ConfigMap. The image remains the same across environments, while the team manages configuration changes and rollouts separately.

## Deep Dive

- ConfigMaps are namespaced; a Pod's normal ConfigMap reference targets a ConfigMap in the same namespace.
- Missing required ConfigMaps or keys can prevent container startup.
- Mounted ConfigMap content updates eventually, not necessarily immediately.
- The application may need to watch, reload, validate, or restart to use updated configuration.
- ConfigMaps are not a database, a large-data store, or a secret store.
- Configuration changes should be validated and rolled out with an appropriate rollback plan.

## Hands-on Exercise

Create and inspect a ConfigMap in a local or authorized cluster:

```bash
kubectl apply -f orders-config.yaml
kubectl get configmap orders-config
kubectl describe configmap orders-config
kubectl get configmap orders-config -o yaml
kubectl get pods
kubectl get deployments
kubectl get events --sort-by=.metadata.creationTimestamp
```

Trace how a Pod could consume a key as an environment variable and how it could mount a configuration file. Predict the effect of changing a key on existing containers. Only delete resources created for the exercise and not used by other workloads:

```bash
kubectl delete configmap orders-config
```

## Common Misconceptions

- ConfigMaps change application code or rebuild images.
- Updating a ConfigMap automatically restarts Pods.
- Mounted files update instantly or every application automatically reloads them.
- ConfigMaps are appropriate for passwords when access is restricted.
- ConfigMaps are cluster-global rather than namespaced.

## Summary

ConfigMaps externalize non-confidential configuration from application images. Pods can consume their values as environment variables or mounted files, but update behavior depends on the delivery method and application reload strategy.

## Key Takeaways

- ConfigMap stores non-confidential configuration.
- Environment variables in existing containers do not change when the ConfigMap changes.
- Mounted files update eventually, except that `subPath` mounts do not receive automatic updates.
- ConfigMap changes alone do not generally trigger a Deployment rollout.
- Use Secrets with appropriate security controls for sensitive values.

## Reflection Questions

1. Why separate configuration from a Docker image?
2. How do environment-variable and file-based ConfigMap consumption differ?
3. Why might an application keep using old configuration after a ConfigMap update?
4. Why should credentials not be stored in ConfigMaps?
5. How would you investigate a configuration change that appears not to have taken effect?

## What's Next

Lesson 112 — Kubernetes Secrets: sensitive configuration, Pod consumption, and security limitations.
