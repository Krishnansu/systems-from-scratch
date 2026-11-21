# Lesson 147 — Health Checks

## Objectives
- Understand why health checks are needed beyond process/port checks.
- Distinguish liveness, readiness, and startup checks.
- Understand Kubernetes probe mechanisms and failure behavior.
- Design dependency-aware health checks without causing cascading failures.
- Understand health checks during traffic draining and graceful shutdown.

## Concept Summary
Health checks expose application state so infrastructure can make operational decisions such as restarting an instance or stopping traffic to it.

## Core Ideas
- **Liveness:** Is the application functioning enough to continue, or should it be restarted? Repeated failure can trigger container restart.
- **Readiness:** Can this instance serve requests now? Failure marks it unready and removes it from eligible Service endpoints; it does not restart the container.
- **Startup:** Has initialization completed? When configured, liveness and readiness checks are held off until startup succeeds.
- **Probe mechanisms:** HTTP, TCP, exec, and gRPC (where supported/configured).
- **Probe configuration:** Initial delay, period, timeout, success/failure thresholds, and probe execution affect behavior.
- **Dependency health:** Not every dependency failure should make an instance unready. Consider whether the dependency is essential to serving requests and whether fallback behavior exists.
- **Cascading failure:** Dependency-heavy checks can amplify an outage by making many services unhealthy or increasing dependency load.
- **Health vs monitoring:** Health endpoints are lightweight operational signals, not full diagnostics or monitoring dashboards.
- **Graceful shutdown:** Mark instance unready, drain new traffic, allow in-flight work to finish, then terminate.

## Practical Example
An Order Service may be alive while PostgreSQL is unavailable. Liveness may remain healthy to avoid unnecessary restarts, while readiness may fail if the database is essential for handling orders. If Redis is only a cache and fallback exists, Redis failure may not require readiness to fail.

## Production Perspective
Use liveness to detect unrecoverable/stuck application conditions, readiness to control traffic, and startup to protect slow initialization. Keep probes lightweight and avoid turning dependency outages into restart storms. Health checks complement logs, metrics, and traces.

## Common Mistakes
- Checking every dependency from liveness.
- Treating readiness failure as a restart condition.
- Omitting startup probes for slow initialization.
- Making probes expensive or dependent on overloaded systems.
- Always returning healthy from readiness.
- Confusing an instance unable to serve traffic with an instance that needs restarting.

## Key Takeaways
- Alive does not mean ready.
- Liveness failure can restart a container.
- Readiness failure stops routing new traffic to an instance through readiness-controlled endpoints.
- Startup probes protect initialization.
- Dependency checks require careful design to prevent cascading failures.
- Health checks also help deployment traffic draining and graceful shutdown.

## Reflection Questions
1. Why is checking whether a process is running insufficient to determine application health?
2. Explain liveness vs readiness with a concrete scenario.
3. What happens in Kubernetes when a liveness probe repeatedly fails?
4. What happens when a readiness probe fails? Does Kubernetes restart the container?
5. Why is a startup probe useful for a slow-starting application?
6. What are the different mechanisms Kubernetes can use to perform probes?
7. Should every dependency failure cause readiness to fail? Explain.
8. How can poorly designed health checks contribute to cascading failures?
9. How do health checks help during graceful shutdown and rolling deployments?
10. Metrics show an increasing error rate, a trace identifies a slow DB dependency, and readiness fails on one Pod. Explain how these three signals complement each other.

## Related Lessons
- Lesson 116 — Kubernetes Health Checks and Probes
- Lesson 144 — Logging
- Lesson 145 — Metrics
- Lesson 146 — Tracing
- Lesson 123 — API Gateway

## What's Next
Lesson 148 — Prometheus.
