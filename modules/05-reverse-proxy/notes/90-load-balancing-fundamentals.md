# Lesson 90 — Load Balancing Fundamentals

## Objectives
- Explain why load balancing is needed.
- Compare common balancing algorithms.
- Understand health checks, backend failures, and recovery.
- Identify scaling bottlenecks and retry risks.

## Prerequisites
- Lesson 88 — Reverse Proxy Fundamentals
- Lesson 89 — NGINX Fundamentals

## Theory
A load balancer distributes incoming requests or connections across eligible backend instances. It can improve capacity and availability, but cannot remove bottlenecks in shared dependencies.

```text
Clients → Load Balancer → App A
                       → App B
                       → App C
```

## Real World Example
An online store distributes traffic across several application instances. If one instance becomes unhealthy, the load balancer stops sending it new work while healthy instances continue serving requests.

## Deep Dive
- **Round robin:** cycles through backends; effective when capacities and request costs are similar.
- **Weighted round robin:** assigns more selections to higher-weight backends.
- **Least connections:** favors backends with fewer active connections; connection count is only an approximation of workload.
- **Latency-aware balancing:** favors faster-responding backends but can react to noisy measurements.
- **IP hash/sticky sessions:** tends to keep a client on one backend, but may create uneven load.
- **Active health checks:** periodically probe backend health.
- **Passive health checks:** infer health from real traffic outcomes.
- Recovery policies can require multiple successful probes to reduce flapping.
- A timeout does not prove a write failed. Retries for operations such as order creation require idempotency safeguards.
- More application instances may increase pressure on a shared database or other dependency.
- A single load balancer can itself become a single point of failure.

## Hands-on Exercise
1. Compare least connections with round robin.
2. Describe how an unhealthy backend can be removed and restored.
3. Explain why retrying order creation can duplicate an operation.
4. Identify shared dependencies that can limit horizontal scaling.
5. Explain why the load-balancing tier also needs availability planning.

## Common Misconceptions
- Equal request counts do not imply equal workload.
- A running process is not necessarily a healthy service.
- Health checks cannot guarantee every request will succeed.
- Load balancing does not guarantee exactly proportional scaling.
- Retrying every failed request is not safe for non-idempotent operations.

## Summary
Load balancing distributes traffic among backend instances using an algorithm suited to the workload. Health checks help avoid unhealthy instances, and recovery policies control their return to service. Production designs must also consider retries, shared dependencies, and redundant load-balancing infrastructure.

## Key Takeaways
- Choose algorithms based on backend behavior and workload.
- Health checks are useful signals, not guarantees.
- Idempotency makes appropriate retries safer.
- Scaling one tier can overload another.
- The load balancer itself must not be an unplanned single point of failure.

## Reflection Questions
1. How does weighted round robin differ from ordinary round robin?
2. Why can least connections help with requests of different durations?
3. What is the difference between active and passive health checks?
4. Why can retrying an order request duplicate an order?
5. What can happen when more application instances share an overloaded database?

## What's Next
Lesson 91 — SSL/TLS Termination.
