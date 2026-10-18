# Lesson 81 — Circuit Breakers & Resilience

## Objectives

- Understand how circuit breakers prevent cascading failures.
- Explain Closed, Open, and Half-Open states.
- Distinguish circuit breakers from timeouts, retries, rate limiters, and bulkheads.
- Understand local versus shared breaker state and safe fallbacks.

## Prerequisites

- API fundamentals and downstream service dependencies
- Rate limiting and distributed service architecture
- Timeouts, retries, and failure handling

## Theory

A circuit breaker monitors calls to a dependency and temporarily blocks calls when failures exceed a configured threshold. It prevents a failing or slow dependency from continuously consuming caller resources and contributing to cascading failures.

## Real World Example

An Order API calls Shipping to retrieve delivery status. Shipping becomes slow, causing requests to accumulate and consume application resources. When the breaker opens, the Order API stops calling Shipping temporarily. It can still return order details with a clearly indicated unavailable shipping status, provided the product semantics allow it.

## Deep Dive

### Circuit breaker states

- **Closed:** calls are allowed; outcomes are monitored.
- **Open:** calls are blocked locally; the caller can fail fast or use a fallback.
- **Half-Open:** a limited number of test calls determine whether the dependency has recovered.

Typical transitions:

- Closed → Open: failures or slow calls cross a configured threshold.
- Open → Half-Open: the waiting period expires.
- Half-Open → Closed: test calls succeed.
- Half-Open → Open: test calls fail.

### Related resilience mechanisms

- **Timeout:** bounds how long a call can wait.
- **Retry:** repeats an operation under a bounded policy.
- **Rate limiter:** restricts traffic or usage.
- **Bulkhead:** isolates resource consumption.
- **Fallback:** provides safe alternative behavior.

Use bounded retries, backoff with jitter, and idempotency or deduplication where needed.

### Production considerations

- Breakers are commonly local to an application process or proxy and scoped to a dependency.
- Different pods may observe failures and open their breakers at different times.
- A shared breaker is possible but adds coordination complexity.
- Count meaningful dependency failures, not every unsuccessful business outcome.
- Half-Open probes should be limited to avoid overwhelming a recovering dependency.
- Monitor state transitions, timeouts, rejected calls, latency, and fallback usage.

## Hands-on Exercise

Scenario: Three Order API pods call Shipping with a two-second timeout. Each pod has its own breaker, which opens after enough failures and remains open for ten seconds.

Key conclusions:

1. Pod B can still call Shipping while Pod A's independent breaker is Open.
2. A timeout bounds resource consumption for an individual call.
3. A valid business response is not necessarily a dependency failure.
4. Half-Open permits limited recovery probes.
5. A safe fallback can preserve useful functionality without fabricating unavailable data.

## Common Misconceptions

- A circuit breaker repairs the failing service. It does not.
- Every pod automatically shares the same breaker state. Not with independent local breakers.
- Every error should count as a breaker failure. Failure classification matters.
- Retries always improve reliability. Excessive retries can worsen overload.
- Fallbacks can return arbitrary substitute data. They must preserve correctness.

## Summary

Circuit breakers reduce cascading failures by temporarily stopping calls to dependencies that appear unhealthy. They complement timeouts, bounded retries, bulkheads, and safe fallbacks.

## Key Takeaways

- Closed allows calls; Open blocks calls; Half-Open tests recovery.
- Breaker state is commonly local and dependency-specific.
- Timeouts, retries, and breakers solve different problems.
- Resilience means preserving correct functionality where possible, not hiding every failure.

## Reflection Questions

1. Why is a circuit breaker not a replacement for a timeout?
2. What can happen if all breakers close simultaneously?
3. Which failures should count toward opening a breaker?

## What's Next

Lesson 82 — gRPC Fundamentals: RPC, Protocol Buffers, HTTP/2, and service-to-service communication.
