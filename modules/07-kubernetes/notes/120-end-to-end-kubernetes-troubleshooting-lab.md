# Lesson 120 — End-to-End Kubernetes Troubleshooting Lab

## Objectives

- Diagnose failures across scheduling, workloads, Services, resources, and security.
- Use events, logs, metrics, and object state to test hypotheses.
- Separate symptoms from root causes and verify recovery.

## Diagnostic Workflow

1. Establish the affected service, namespace, version, and scope.
2. Inspect current state, events, logs, and relevant metrics.
3. Form a hypothesis based on evidence.
4. Test it safely, preferring read-only checks.
5. Apply an authorized, proportionate mitigation if needed.
6. Verify recovery and record the root cause.

## First-Pass Commands

```bash
kubectl config current-context
kubectl get pods -A
kubectl get deployments,replicasets -A
kubectl get services,endpointslices -A
kubectl get events -A --sort-by=.metadata.creationTimestamp
kubectl describe pod <pod-name> -n <namespace>
kubectl logs <pod-name> -n <namespace> --all-containers
```

## Symptom-to-Evidence Map

| Symptom | Investigate |
|---|---|
| Pending Pod | Scheduling events, requests, node constraints, volume binding |
| CrashLoopBackOff | Current/previous logs, exit reason, configuration, probes, resources |
| Running but not Ready | Readiness probe, application health, dependencies, events |
| Service unavailable | Selector/labels, readiness, EndpointSlices, ports, DNS, networking |
| Slow requests | CPU/memory, restarts, rollout changes, dependency latency, metrics |
| Forbidden API request | Identity, RBAC rules, and bindings |
| Unexpected network failure | Routing, ports, DNS, and applicable NetworkPolicies |

## Core Reasoning

- Running does not imply Ready or successful requests.
- A Service can have no usable endpoints even while Pods exist.
- Pending Pods have not necessarily started containers, so application logs may not exist.
- `OOMKilled` and node-pressure eviction are different failure mechanisms.
- `kubectl top` provides usage snapshots, not historical trends or direct proof of CPU throttling.
- Events may expire or be incomplete; corroborate with logs, metrics, object state, and external monitoring.

## Common Mistakes

- Restarting or deleting workloads before collecting evidence.
- Treating a single status field as a complete diagnosis.
- Changing multiple settings simultaneously, making the cause harder to identify.
- Using state-changing commands without authorization or a rollback plan.
- Declaring recovery without checking request success, latency, error rates, and workload stability.

## Key Takeaways

Follow evidence across layers, distinguish symptoms from causes, change state deliberately, and verify recovery. Kubernetes troubleshooting is a disciplined hypothesis-testing process rather than a sequence of restart commands.

## Related Lessons

- Lesson 109 — Kubernetes Services
- Lesson 114 — Autoscaling
- Lesson 115 — Scheduling
- Lesson 118 — Resource Management, QoS, and Eviction
- Lesson 119 — Kubernetes Security
