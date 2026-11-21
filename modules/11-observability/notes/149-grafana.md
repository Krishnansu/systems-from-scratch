# Lesson 149 — Grafana

## Objectives
- Understand Grafana's role in the observability stack.
- Understand data sources, dashboards, and panels.
- Learn dashboard variables, templating, and transformations.
- Understand Grafana alerting and its relationship with Prometheus Alertmanager.
- Learn production dashboard design practices.

## Concept Summary
Grafana is an observability and visualization platform that queries external data sources and presents their data through dashboards and panels. It complements Prometheus rather than replacing its metric collection and storage responsibilities.

## Core Ideas
- **Architecture:** Grafana connects to data sources, executes queries, and renders results. The data source generally owns its underlying storage and query engine.
- **Data sources:** Grafana supports Prometheus, Loki, Jaeger, Elasticsearch, PostgreSQL, InfluxDB, and others.
- **Dashboards:** Collections of visualizations designed around a system, service, infrastructure component, or operational question.
- **Panels:** Individual dashboard visualizations. A panel configures its data source, query, visualization, transformations, and field presentation.
- **Time range:** The dashboard time range controls the period being visualized. A PromQL range selector such as `[5m]` controls the lookback window used by a query function such as `rate()`.
- **Variables and templating:** Dynamic values such as environment, service, and instance can be reused in queries, allowing one dashboard to serve multiple targets.
- **Transformations:** Process query results before visualization, for example filtering, renaming, joining, organizing, or reducing fields.
- **Visualizations:** Time series, gauges, stat panels, tables, bar charts, and other visualizations should match the operational question.
- **Alerting:** Grafana supports its own alert evaluation and notification workflow. Prometheus can independently evaluate alerting rules and send alerts to Alertmanager.
- **Provisioning:** Dashboards and data sources can be provisioned through configuration and dashboard definitions, enabling version control and repeatable deployment.
- **Availability:** Grafana is separate from Prometheus collection and storage. A Grafana outage does not inherently stop Prometheus scraping or Prometheus-managed alerting.

## Practical Examples

Example panel query:

```promql
sum(rate(http_requests_total[5m]))
```

Example variable-based query:

```promql
sum(rate(http_requests_total{instance=~"$instance"}[5m]))
```

Suggested service dashboard panels:
- Request rate
- Error rate by status code
- p50, p95, and p99 latency
- CPU and memory utilization
- Database connection pool usage
- Downstream dependency latency

Useful dashboard variables include environment, service, and instance.

## Production Perspective
Organize dashboards from system overview to service-level, instance-level, and dependency-level views. Start with traffic, errors, latency, and saturation. Use meaningful units and thresholds, avoid noisy or redundant panels, and make dashboards reusable through variables. Store dashboard definitions in version control and provision them consistently across environments.


## Reflection & Hands-on Insights

### 1. Dashboard Time Range vs. PromQL Range Selector
- **Dashboard time range:** Determines how far back the graph displays data (e.g., last 1 hour).
- **PromQL range selector (`[5m]`):** Determines how much historical data each calculation uses at an evaluation point.
- Grafana evaluates the query repeatedly across the dashboard range, producing graph points. The evaluation step/resolution influences point spacing.
- For `rate(counter[5m])`, each evaluation uses a sliding 5-minute window. A shorter window is more reactive/noisy; a longer one is smoother but less immediate.

> Dashboard range determines how much history I see; the PromQL range selector determines how much history each calculation looks at.


### 2. Dashboard Design Hierarchy
Build dashboards to support progressive investigation:

1. **System overview:** Is the system unhealthy? Which service appears affected?
2. **Service dashboard:** Is the issue in the application, runtime, database, or a dependency?
3. **Instance/endpoint view:** Is the problem isolated to particular instances, routes, or operations?
4. **Dependency view:** Is a downstream system contributing to the issue?

### 3. System Overview Dashboard
Useful panels:
- Total traffic / request rate
- System error rate
- End-to-end p50/p95/p99 latency
- Service health / availability
- Per-service request rate, error rate, and latency
- CPU, memory, and active alerts

Core question: **Is the system unhealthy, and which service is likely contributing?**

Example PromQL:

```promql
sum by (service) (
  rate(http_requests_total[5m])
)
```

```promql
sum by (service) (
  rate(http_requests_total{status=~"5.."}[5m])
)
```

### 4. Order Service Dashboard
Organize panels by category:

- **Application:** Request rate, errors by HTTP status, p50/p95/p99 latency, endpoint traffic, retries, and timeouts.
- **Runtime:** CPU, memory, threads/goroutines, GC pauses, instance health, and restarts.
- **Database:** Query latency, connection pool usage, connection acquisition wait, errors/timeouts, lock waits, and slow queries.
- **Dependencies:** Downstream latency, errors, timeouts, and retry activity for systems such as Payment, Inventory, or Redis.

Core question: **Why is this service slow—is it the application, database, or a dependency?**

### 5. Reusable Dashboard Variables
Common variables:
- `$environment`
- `$service`
- `$instance`
- `$endpoint`
- `$region`

Example:

```promql
sum(
  rate(http_requests_total{
    environment="$environment",
    service="$service",
    instance=~"$instance",
    endpoint=~"$endpoint"
  }[5m])
)
```

Variables allow one dashboard to be reused across environments, services, instances, endpoints, and regions rather than maintaining separate dashboards.

### 6. Diagnosing High API Latency
Compare API latency with other indicators before assuming a CPU or database problem:

| Observation | Possible area to investigate |
|---|---|
| API latency ↑, DB latency ↑ | Database query performance |
| API latency ↑, DB latency normal, CPU ↑ | Application CPU-bound work |
| API latency ↑, DB latency normal, CPU normal | Network, locks, downstream calls, or other waits |
| API latency ↑, connection acquisition wait ↑ | Connection pool starvation or insufficient pool capacity |
| API latency ↑, downstream latency ↑ | Dependency degradation |
| API latency ↑, retries ↑ | Retry amplification or dependency failures |

Useful supporting panels: request latency, DB query latency, connection acquisition latency, pool utilization, lock waits, slow queries, downstream latency, CPU, errors, and timeouts.

Metrics help narrow down **where or when** a problem occurs. Distributed traces provide request-level breakdowns of time spent in individual operations and dependencies. Metric latency components should not automatically be assumed additive or perfectly comprehensive.

### 7. Alerting Responsibilities
- **Prometheus:** Evaluates Prometheus alerting rules using metric queries and conditions.
- **Alertmanager:** Handles grouping, deduplication, routing, inhibition, silencing, and notifications.
- **Grafana Alerting:** A separate alert evaluation and notification workflow, useful where Grafana-managed alerts fit the use case.

Avoid duplicate alert ownership and keep alert rules/configuration version-controlled where possible. Prometheus-managed alerting can continue independently of Grafana availability.


## Common Mistakes
- Treating Grafana as a replacement for the underlying metrics database.
- Assuming Grafana only supports Prometheus.
- Confusing dashboard time range with PromQL range selectors.
- Creating too many panels without clear operational purpose.
- Treating dashboards and alert rules as the same thing.
- Assuming Grafana-managed and Prometheus-managed alerting are identical.
- Assuming a Grafana outage stops Prometheus scraping or Alertmanager notifications.
- Assuming normal CPU utilization means the application isn't experiencing performance problems.
- Assuming API latency is entirely caused by DB query latency without checking connection waits and dependencies.
- Using dashboard transformations for metric calculations that are better handled by the data source query.

## Key Takeaways
- Grafana is the visualization and exploration layer of an observability stack.
- Data sources retain responsibility for their own data and query models.
- Dashboards contain panels, and panels execute queries and visualize results.
- Variables and transformations make dashboards reusable and adaptable.
- Grafana and Prometheus provide distinct alerting workflows.
- Dashboard design should help engineers answer operational questions quickly.
- Dashboards and data sources can be provisioned and version-controlled.
- Use an overview-first hierarchy to drill into service, instance, and dependency details.
- Compare application, database, connection pool, and downstream signals to diagnose latency.
- Metrics help identify patterns; traces help localize time spent within requests.

## Reflection Questions
1. What problem does Grafana solve? Why isn't Prometheus alone sufficient for convenient operational monitoring?
2. Explain the complete flow when an engineer opens a Grafana dashboard containing a Prometheus-backed panel.
3. What is the difference between a Grafana dashboard and a panel? What configuration does a panel contain?
4. Can Grafana connect to multiple data sources? Explain how this helps during a production incident.
5. What is the difference between the dashboard time range and a PromQL range selector such as `[5m]`?
6. What are Grafana variables? How would you use them to build one dashboard for multiple service instances?
7. What are Grafana transformations? Give an example of when you might use one.
8. Compare Prometheus-managed alerting with Grafana-managed alerting. What role does Alertmanager play?
9. If Grafana becomes unavailable, what happens to Prometheus scraping, metric storage, and Prometheus-managed alerts?
10. Your Order Service has high p95 latency, but CPU utilization is normal. Design a dashboard layout that helps an on-call engineer investigate the issue. Explain which panels and filters you'd include.

## Related Lessons
- Lesson 144 — Logging
- Lesson 145 — Metrics
- Lesson 146 — Tracing
- Lesson 148 — Prometheus

## What's Next
Lesson 150 — OpenTelemetry.
