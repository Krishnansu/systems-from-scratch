# Lesson 80 — API Rate Limiting, Quotas & Abuse Prevention

## Objectives
- Explain rate limits, quotas, concurrency limits, and query-cost limits.
- Compare common rate-limiting algorithms.
- Understand distributed enforcement and abuse prevention.

## Concept Summary
Rate limiting controls how frequently a client can make requests. It protects shared capacity, improves fairness, controls costs, and reduces some forms of abuse. Quotas limit total usage over a period; concurrency limits bound simultaneous work; query-cost limits account for expensive operations.

## Core Ideas
- **Fixed window:** Simple counters per time interval; bursts can occur across window boundaries.
- **Sliding window:** Counts recent requests more smoothly; precise logs cost more memory than approximate counters.
- **Token bucket:** Tokens refill at a configured rate. Requests consume tokens. Bucket capacity controls burst size, while refill rate controls sustained usage.
- **Leaky bucket:** Smooths traffic toward a controlled processing rate; queues must be bounded.
- Apply limits by API key, user, tenant, IP, endpoint, or globally according to the threat and fairness model.
- HTTP `429 Too Many Requests` signals a rate-limit rejection. `Retry-After` can guide client retries.
- Exponential backoff with jitter helps prevent synchronized retry storms.

## Practical Example
For a multi-tenant API, enforce per-user and per-tenant request limits, restrict concurrent expensive reports, and apply stricter cost limits to expensive GraphQL operations. A tenant-level limit prevents one customer from consuming all shared capacity.

## Production Perspective
- Per-process counters on multiple API servers can multiply the effective limit.
- Shared state such as Redis can coordinate enforcement; use atomic operations or scripts to avoid races.
- An API gateway can enforce common policies at the entry point.
- Decide whether limiter-backend failure should fail open (preserve availability, risk excess traffic) or fail closed (preserve enforcement, risk rejecting legitimate requests).
- Monitor allowed and rejected traffic, per-tenant and per-route trends, limiter latency/errors, backend resource usage, and false positives.
- Do not log API keys or other secrets. Rate limiting complements authentication, authorization, validation, and abuse detection; it does not replace them.

## Common Mistakes
- Treating a requests-per-minute limit as a guarantee that all requests can arrive in one burst.
- Using only IP-based limits despite shared networks or changing addresses.
- Assuming one HTTP request equals one unit of backend work.
- Using rate limits alone to control long-running simultaneous work instead of adding concurrency limits.
- Performing non-atomic counter updates across concurrent requests.

## Key Takeaways
1. Rate limits control request frequency; quotas control total usage.
2. Token buckets allow bounded bursts while limiting sustained traffic.
3. Tenant-level limits help protect fairness between customers.
4. Distributed enforcement requires shared or carefully partitioned state.
5. Use `429`, retry guidance, and observability to support safe client behavior.

## Reflection Questions
1. Why can a per-server counter fail to enforce a global customer limit?
2. How does token-bucket capacity differ from refill rate?
3. Why might an expensive endpoint need a concurrency limit in addition to a rate limit?

## Related Lessons
- Lesson 76 — REST API Design in Practice
- Lesson 78 — GraphQL Execution, Resolvers & DataLoader
- Lesson 79 — GraphQL Performance, Security & Production Design

## What's Next
Lesson 81 — Circuit Breakers & Resilience (proposed continuation).
