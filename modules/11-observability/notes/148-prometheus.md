# Lesson 148 — Prometheus

## Objectives
- Understand Prometheus architecture and its role in monitoring.
- Understand pull-based scraping, jobs, targets, and exporters.
- Understand time-series storage and metric identity.
- Query metrics using PromQL.
- Understand alerting rules and Alertmanager.

## Concept Summary
Prometheus is an open-source monitoring and alerting system that discovers targets, periodically scrapes metrics, stores timestamped samples in a time-series database, and provides PromQL for querying and alert evaluation.

## Core Ideas
- **Architecture:** Prometheus server handles retrieval, TSDB storage, querying, and rule evaluation. Applications and exporters expose metrics; Alertmanager manages notifications.
- **Instrumentation:** Applications expose metrics, commonly at `/metrics`, using Prometheus exposition format.
- **Exporters:** Translate statistics from external systems into Prometheus-compatible metrics. Examples include Node Exporter, PostgreSQL Exporter, and Redis Exporter.
- **Pull model:** Prometheus periodically requests metrics from targets. Centralizes scrape configuration and makes scrape failures observable.
- **Pushgateway:** Supports selected short-lived batch jobs that cannot reliably be scraped while running. It is not a general replacement for pull-based scraping.
- **Jobs and targets:** A job groups similar scrape targets; a target is an individual endpoint.
- **Service discovery:** Finds dynamic targets through integrations such as Kubernetes, Consul, and DNS. Relabeling filters targets or transforms metadata.
- **Scraping:** Prometheus requests a target's metrics endpoint, parses samples, attaches scrape labels such as job and instance, and stores timestamped values.
- **up metric:** `up = 1` means the last scrape succeeded; `up = 0` means it failed. It does not prove application business functionality is healthy.
- **Time-series identity:** Metric name plus complete label set. Changing labels creates a different series; high cardinality increases storage and query costs.
- **TSDB:** Stores timestamped samples using an in-memory head, WAL, persistent blocks, and indexes. Retention controls how long local data is kept.
- **PromQL:** Supports instant and range vectors, label filtering, `rate()`, aggregation, and histogram quantiles.
- **Alerting:** Prometheus evaluates alerting rules. `for` requires a condition to remain true for a duration before firing. Alertmanager groups, deduplicates, inhibits, silences, and routes notifications.

## Practical Examples

Example scrape configuration:

```yaml
global:
  scrape_interval: 15s

scrape_configs:
  - job_name: order-service
    static_configs:
      - targets: ["order-service:8080"]
```

Useful PromQL:

```promql
# Select all matching request counters
http_requests_total

# Filter HTTP 5xx series
http_requests_total{status=~"5.."}

# Average per-second increase over five minutes
rate(http_requests_total[5m])

# Total request rate across instances
sum(rate(http_requests_total[5m]))

# Request rate grouped by status
sum by (status) (rate(http_requests_total[5m]))

# p95 latency from histogram buckets
histogram_quantile(
  0.95,
  sum by (le) (rate(http_request_duration_seconds_bucket[5m]))
)
```

## Production Perspective
Prometheus is useful for service monitoring, infrastructure metrics, alerting, and dynamic environments such as Kubernetes. Production design must account for scrape intervals, target discovery, cardinality, retention, local storage availability, long-term storage, and monitoring Prometheus itself. Metrics should be correlated with traces and logs during investigation.

## Common Mistakes
- Assuming `up = 1` means the application is functionally healthy.
- Treating Pushgateway as a general-purpose push ingestion system.
- Manually configuring targets in highly dynamic environments when service discovery is available.
- Using unbounded labels that create high cardinality.
- Applying `rate()` to gauges instead of counters.
- Forgetting to aggregate histogram buckets correctly before calculating quantiles.
- Assuming local Prometheus storage alone provides a complete long-term retention and high-availability solution.
- Confusing Prometheus alert evaluation with Alertmanager notification routing.

## Key Takeaways
- Prometheus primarily uses pull-based metric collection.
- Applications and exporters expose metrics; Prometheus scrapes them.
- Jobs group targets, and service discovery supports dynamic infrastructure.
- Time series are identified by metric name and complete label set.
- PromQL enables filtering, rate calculations, aggregation, and quantile analysis.
- Prometheus evaluates alert rules; Alertmanager manages notifications.
- Cardinality, scrape frequency, retention, and storage are important operational concerns.

## Reflection Questions
1. What problem does Prometheus solve, and how does it fit into the observability stack?
2. Explain the difference between an instrumented application and an exporter. Give an example of each.
3. Why does Prometheus primarily use a pull-based collection model? What advantages does it provide over pushing metrics?
4. What are jobs and targets? How does service discovery help when applications scale dynamically in Kubernetes?
5. What happens internally when Prometheus scrapes a target? What does `up = 0` tell us, and what does it not tell us?
6. How is a Prometheus time series identified? Explain how labels affect the number of time series.
7. What is the difference between an instant vector and a range vector in PromQL?
8. Why do we use `rate()` on counters? Explain how you would calculate the total request rate across multiple service instances.
9. Explain the responsibilities of Prometheus and Alertmanager. What is the purpose of the `for` field in an alerting rule?
10. Your Order Service has increasing p95 latency, but CPU utilization is normal. How would you use Prometheus metrics and PromQL to investigate the issue? What other observability signals might you need?

## Related Lessons
- Lesson 145 — Metrics
- Lesson 146 — Tracing
- Lesson 147 — Health Checks
- Lesson 140 — Kafka

## What's Next
Lesson 149 — Grafana.
