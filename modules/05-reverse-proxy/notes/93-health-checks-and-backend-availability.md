# Lesson 93 — Health Checks and Backend Availability

## Objectives
- Distinguish liveness from readiness.
- Compare active and passive health checks.
- Understand failure detection, recovery thresholds, and flapping.
- Recognize the limits of health checks in production.

## Prerequisites
- Lesson 88 — Reverse Proxy Fundamentals
- Lesson 89 — NGINX Fundamentals
- Lesson 90 — Load Balancing Fundamentals
- Lesson 92 — Routing Fundamentals

## Theory
Health checks help a proxy decide which backend instances should receive traffic. A running process is not necessarily able to serve requests successfully.

- **Liveness:** Is the process alive, or is it irrecoverably stuck?
- **Readiness:** Can the instance currently accept the intended production traffic?
- **Active checks:** Send independent periodic probes to a backend.
- **Passive checks:** Infer backend health from failures observed during real requests.

## Real World Example
A reverse proxy has three application instances. If one becomes unhealthy, the proxy can stop sending it new requests while the other instances continue serving traffic. The remaining instances may still become overloaded, so backend removal is not a complete recovery strategy.

## Deep Dive
- A health endpoint should test what its consumer needs to know. A deep dependency check can mark every instance unready during a shared database incident, even when some requests could still be served.
- NGINX Open Source supports passive upstream failure handling. `max_fails` and `fail_timeout` configure failure thresholds and temporary unavailability behavior; they are not a complete active readiness-check system. NGINX Plus supports active health checks.
- Detection time depends on probe interval, failure threshold, probe timeout, and when the failure begins relative to the next probe.
- Flapping is rapid switching between healthy and unhealthy states. Consecutive successful checks, warm-up periods, and gradual traffic restoration can reduce it.
- Health checks do not repair instances, guarantee low latency for every endpoint, or replace logs, metrics, and traces.
- When health checks pass but requests are slow, investigate resource pressure, queueing, connection pools, cache behavior, and downstream latency.

## Hands-on Exercise
1. Estimate detection time for a probe every 5 seconds with three consecutive failures.
2. Distinguish active from passive health checks.
3. Choose between liveness and readiness for traffic eligibility.
4. Explain how recovery thresholds reduce flapping.

## Common Misconceptions
- A running process is not necessarily ready.
- One failed probe does not always mean an instance should be removed immediately.
- A successful health endpoint does not guarantee every request will succeed or be fast.
- Health checks detect conditions; they do not automatically repair them.
- Marking every instance unhealthy during a shared dependency incident can amplify an outage.

## Summary
Health checks inform traffic decisions by estimating backend availability. Good policies balance timely failure detection with stable recovery and reflect the requests an instance can actually serve. Observability is still needed to diagnose performance and dependency problems.

## Key Takeaways
- Liveness and readiness answer different questions.
- Active checks probe independently; passive checks observe real traffic failures.
- Intervals, timeouts, and thresholds determine detection behavior.
- Recovery safeguards help prevent flapping.
- Health checks complement, rather than replace, production observability.

## Reflection Questions
1. Why can an application be live but not ready?
2. What is the key difference between active and passive health checks?
3. Why might removing every instance when a shared database is temporarily unavailable make an incident worse?
4. What is flapping, and how can a system reduce it?
5. If all backends pass their health checks but users still see slow requests, what would you investigate next?

## What's Next
Lesson 94 — Firewall Fundamentals: understand traffic filtering, firewall rules, and how firewalls differ from reverse proxies.
