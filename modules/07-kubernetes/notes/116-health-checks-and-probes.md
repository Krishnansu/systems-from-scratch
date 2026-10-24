# Lesson 116 — Kubernetes Health Checks and Probes

## Objectives

- Distinguish startup, liveness, and readiness probes.
- Understand their effects on container restarts and Service traffic.
- Inspect common probe failures.

## Core Concepts

| Probe | Purpose | Failure effect |
|---|---|---|
| `startupProbe` | Determine whether startup completed | Container restarts after the failure threshold is reached |
| `livenessProbe` | Detect an unhealthy or stuck process | Container restarts after the failure threshold is reached |
| `readinessProbe` | Determine whether a Pod should receive traffic | Pod becomes not Ready and is normally excluded from ready Service endpoints |

When configured, a startup probe gates liveness and readiness checks until startup succeeds. A readiness failure does not itself restart the container. A liveness failure does not itself recreate the Pod.

## Example

```yaml
startupProbe:
  httpGet:
    path: /health/startup
    port: 8080
  periodSeconds: 5
  failureThreshold: 30

livenessProbe:
  httpGet:
    path: /health/live
    port: 8080
  periodSeconds: 10
  failureThreshold: 3

readinessProbe:
  httpGet:
    path: /health/ready
    port: 8080
  periodSeconds: 5
  failureThreshold: 3
```

The startup configuration allows approximately 150 seconds of scheduled checking before the failure threshold is reached; actual timing depends on probe execution and timing rules. Select endpoints according to application behavior. This is an illustrative snippet, not a complete Pod manifest.

## Probe Mechanisms

- HTTP: requests an HTTP endpoint.
- TCP: checks whether a connection can be established.
- Exec: runs a command inside the container.
- gRPC: calls a gRPC health-check endpoint.

A successful TCP check does not prove the application can correctly serve requests.

## Troubleshooting

```bash
kubectl describe pod <pod-name>
kubectl get pods -w
kubectl logs <pod-name> --previous
kubectl get endpointslices
```

- Repeated restarts: inspect probe events and previous container logs.
- Running but not Ready: check the readiness endpoint, configuration, and dependencies.
- Startup failures: check startup duration, endpoint behavior, and thresholds.
- Ready but requests fail: readiness is not a guarantee that every request or dependency is healthy.

## Key Takeaways

- Startup protects slow initialization.
- Liveness can trigger container restarts.
- Readiness controls whether a Pod is eligible for normal Service traffic.
- Probe design should reflect the application's real behavior.

## Related Lessons

- Lesson 109 — Services
- Lesson 110 — Ingress
- Lesson 114 — Autoscaling
- Lesson 115 — Scheduling
- Lesson 120 — End-to-End Kubernetes Troubleshooting Lab
