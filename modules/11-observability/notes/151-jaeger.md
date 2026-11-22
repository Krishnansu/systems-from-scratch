# Lesson 151 — Jaeger

## What Jaeger does
Jaeger is a distributed tracing platform used to collect, store, query, search, and visualize traces. It helps investigate request journeys across microservices, identify latency bottlenecks, understand dependency relationships, and diagnose failures.

## OpenTelemetry and Jaeger
- OpenTelemetry handles instrumentation, telemetry generation, context propagation, collection, and export.
- Jaeger ingests, stores, queries, and visualizes traces.
- Telemetry can be exported directly to Jaeger or through an OpenTelemetry Collector. OTLP is commonly used for ingestion.

## Trace investigation
- Inspect span duration, hierarchy, status, and events.
- A parent span may include time spent in child spans; do not add nested durations blindly.
- A long downstream span can indicate dependency latency rather than slow application logic.
- Parallel child spans may overlap.

## Repeated spans
Repeated downstream spans may indicate retries, loops, fan-out, or duplicate calls. Investigate span ordering, durations, statuses, retry attributes/events, gaps between attempts, and correlated logs.

## Troubleshooting workflow
1. Metrics identify the symptom (e.g., high API latency).
2. Inspect affected traces in Jaeger.
3. Find the long-duration span(s) in the waterfall.
4. Investigate dependencies, retries, network/I/O waits, locks, or pool waits.
5. Correlate spans with logs using trace/span IDs to find the underlying cause.

Metrics show trends and symptoms; traces locate time spent across operations; logs provide event-level details. Jaeger helps locate bottlenecks but may not reveal the exact cause without useful instrumentation and correlated logs.

## Reflection review
- Q1 Jaeger purpose: 9.5/10
- Q2 OpenTelemetry relationship: 10/10
- Q3 Slow operation vs downstream: 9/10
- Q4 Repeated spans/retries: 8.5/10
- Q5 Latency troubleshooting: 9.5/10
- Total: 46.5/50 (93%)

Key takeaway: Jaeger enables request-level reasoning across distributed services by showing span relationships, timing, dependencies, and repeated operations.