# Lesson 145 — Metrics

## Objectives
- Understand metrics and time series.
- Distinguish counter, gauge, histogram, and summary.
- Understand percentiles, golden signals, labels, and cardinality.
- Design useful service metrics for production monitoring.

## Concept Summary
Metrics are numerical measurements collected over time to monitor system behavior, identify trends, quantify problems, and support alerting.

## Core Ideas
- **Time series:** Sequence of timestamped measurements associated with a metric and label set.
- **Counter:** Cumulative value that increases as events occur; may reset on process restart. Useful for request totals and events processed.
- **Gauge:** Value that can rise or fall; e.g., active connections, queue depth, CPU/memory usage.
- **Histogram:** Observations grouped into buckets; commonly used for aggregatable latency and size distributions.
- **Summary:** Often computes quantiles locally; quantiles generally cannot be merged accurately across instances to obtain a global quantile.
- **Percentiles:** p50/p95/p99 describe observation thresholds; tail latency can be hidden by averages.
- **Golden signals:** Traffic, latency, errors, saturation.
- **Labels/tags:** Dimensions used to filter, group, and compare metric series (service, normalized endpoint, method, status, region).
- **Cardinality:** Number of unique label-value combinations. High-cardinality labels (user_id, request_id, order_id, raw dynamic URLs) can create excessive time series and increase storage, memory, and query costs.
- **Instrumentation:** Decide what to measure, units, labels, and operational questions before choosing monitoring tools.
- **Signal complementarity:** Metrics reveal scale/trends; logs give event detail; traces show request paths and time spent across components.

## Practical Example
For an Order Service, consider metrics such as request count, request duration, error count, active database connections, pool maximum, queue depth, processed orders, and payment attempts. Use bounded labels such as service, normalized endpoint, method, and status. Avoid unique identifiers as metric labels.

## Production Perspective
Use metrics to detect anomalies and quantify impact. Watch tail latency, error rate, traffic, and resource saturation. Metrics help narrow investigation but rarely establish root cause alone; use traces to localize latency and logs to investigate individual events.

## Common Mistakes
- Treating a gauge as a cumulative event counter.
- Using averages alone to understand latency.
- Assuming histogram and summary quantiles are interchangeable or equally aggregatable.
- Adding unbounded identifiers as labels.
- Confusing resource utilization with resource saturation.
- Expecting metrics alone to explain root cause.

## Key Takeaways
- Metrics are measurements over time, not isolated numbers.
- Counters accumulate; gauges move up and down.
- Histograms help analyze distributions and aggregate observations across instances.
- Percentiles reveal tail latency.
- Labels enable analysis but high cardinality can be costly.
- Traffic, latency, errors, and saturation are useful starting signals.
- Metrics, logs, and traces work together.

## Reflection Questions
1. What is a time series, and how is it different from a single metric value?
2. Why should total requests be represented by a counter rather than a gauge?
3. What is the difference between a counter and a gauge? Give two examples of each.
4. Why is average latency insufficient for monitoring an API? Explain p95 and p99.
5. What does a histogram measure, and why is it useful for latency?
6. What is a summary metric, and what is one limitation when aggregating across multiple instances?
7. Explain the four golden signals: traffic, latency, errors, and saturation.
8. What are metric labels? Give a useful example of labels for an HTTP metric.
9. What is cardinality, and why can labels such as user_id or request_id be problematic?
10. If checkout latency increases while CPU stays low, what would metrics suggest investigating next, and which observability signal would you use to drill deeper?

## Related Lessons
- Lesson 144 — Logging
- Lesson 123 — API Gateway
- Lesson 136 — Connection Pooling
- Lesson 140 — Kafka

## What's Next
Lesson 146 — Tracing.
