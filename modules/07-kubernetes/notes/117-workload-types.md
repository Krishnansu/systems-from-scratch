# Lesson 117 — Kubernetes Workload Types

## Core Concepts

| Controller | Best suited for | Key behavior |
|---|---|---|
| Deployment | Long-running, interchangeable application replicas | Manages ReplicaSets and rolling updates |
| StatefulSet | Workloads requiring stable identity or storage association | Stable Pod identity; supports ordered operations |
| DaemonSet | Node-level agents | Runs Pods on eligible nodes |
| Job | Finite tasks | Tracks completion and retries according to configuration |
| CronJob | Scheduled tasks | Creates Jobs according to a schedule |

## Choosing a Controller

- Use a Deployment for interchangeable API or frontend replicas.
- Use a StatefulSet when stable identity, ordered behavior, or per-Pod storage association is needed. It does not itself provide database replication or high availability.
- Use a DaemonSet for log collectors, monitoring agents, and other node-level components.
- Use a Job for a finite task such as an import or migration.
- Use a CronJob to schedule recurring work. Scheduling is not an exactly-once guarantee.

## CronJob Lifecycle

```text
CronJob (schedule)
    -> Job (completion and retries)
        -> Pod (executes task)
```

Jobs may retry tasks, and CronJob runs can be delayed or missed depending on configuration and cluster conditions. Make batch operations tolerant of retries where possible.

## Common Mistakes

- Choosing a StatefulSet solely because an application uses a database.
- Assuming a StatefulSet automatically replicates data or makes a service highly available.
- Assuming a DaemonSet must run on every node regardless of eligibility or scheduling constraints.
- Assuming Jobs or CronJobs guarantee exactly-once execution.

## Related Lessons

- Lesson 106 — Pods
- Lesson 108 — Deployments
- Lesson 113 — Persistent Volumes
- Lesson 115 — Scheduling
