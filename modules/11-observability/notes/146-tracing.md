# Lesson 146 — Tracing

## Objectives
- Understand distributed tracing and why metrics/logs alone are insufficient.
- Distinguish traces, spans, and their identifiers.
- Understand parent-child relationships and context propagation.
- Read trace timelines to identify latency and bottlenecks.
- Understand sampling and trace-log correlation.

## Concept Summary
Distributed tracing follows a request across services and records timed operations (spans), showing its execution path, relationships, and time spent.

## Core Ideas
- **Trace:** End-to-end request journey, identified by Trace ID.
- **Span:** Individual operation within a trace; records name, start/end/duration, attributes, and status.
- **Span context:** Trace ID, Span ID, and Parent Span ID establish identity and hierarchy.
- **Parent-child:** A downstream span's Parent Span ID points to the caller's Span ID, preserving causality.
- **Context propagation:** Trace context travels across service/HTTP/messaging boundaries (e.g., W3C Trace Context) to connect spans.
- **Timeline:** Waterfall view of spans; durations may not add up due to overlap, gaps, uninstrumented work, or different boundaries.
- **Use cases:** Bottleneck localization, error origin, dependency discovery, retries, fan-out, and waiting investigation.
- **Sampling:** Head-based sampling decides early; tail-based sampling evaluates collected trace data and can prioritize slow/error traces, but requires buffering/processing.
- **Trace-log correlation:** Include trace_id and span_id in structured logs to navigate from a trace to relevant log events.
- **Limitations:** Missing instrumentation, broken propagation, sampling misses, overhead, and sensitive data.

## Practical Example
Gateway → Checkout → Inventory / Payment / DB. A trace waterfall shows the Payment span is slow. Inspect nested spans and correlated logs to distinguish internal processing from downstream provider latency, pool waits, network delays, retries, or queueing.

## Production Perspective
Metrics detect and quantify an issue, traces localize the request path and time spent, and logs provide event-level detail. A common investigation loop is metrics → trace → logs → fix → verify. Instrumentation and sampling must balance visibility, cost, and overhead.

## Common Mistakes
- Assuming a slow span means the service's own code is slow.
- Assuming child span durations always sum to parent duration.
- Forgetting context propagation across service boundaries.
- Confusing Trace ID, Span ID, and Parent Span ID.
- Recording sensitive information in span attributes.
- Sampling so aggressively that important failures are missed.

## Key Takeaways
- Trace = whole request journey; span = individual operation.
- IDs connect and organize spans.
- Context propagation preserves distributed causal relationships.
- Timelines reveal duration, overlap, and where time is spent.
- Sampling controls observability cost.
- Metrics, traces, and logs complement one another.

## Reflection Questions
1. What is distributed tracing, and what problem does it solve that metrics alone cannot?
2. Explain trace vs span.
3. What are Trace ID, Span ID, and Parent Span ID?
4. How are parent-child relationships formed?
5. What is context propagation?
6. Why don't child span durations necessarily add up to parent duration?
7. How does a trace help identify a bottleneck?
8. Explain sampling and head vs tail sampling.
9. How do traces and structured logs connect?
10. Does a slow Payment span prove the service is the root cause? How would you investigate?

## Related Lessons
- Lesson 144 — Logging
- Lesson 145 — Metrics
- Lesson 123 — API Gateway
- Lesson 136 — Connection Pooling
- Lesson 143 — Saga Pattern

## What's Next
Lesson 147 — Health Checks.
