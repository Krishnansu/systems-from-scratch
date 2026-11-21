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

## Common Mistakes
- Treating Grafana as a replacement for the underlying metrics database.
- Assuming Grafana only supports Prometheus.
- Confusing dashboard time range with PromQL range selectors.
- Creating too many panels without clear operational purpose.
- Treating dashboards and alert rules as the same thing.
- Assuming Grafana-managed and Prometheus-managed alerting are identical.
- Assuming a Grafana outage stops Prometheus scraping or Alertmanager notifications.

## Key Takeaways
- Grafana is the visualization and exploration layer of an observability stack.
- Data sources retain responsibility for their own data and query models.
- Dashboards contain panels, and panels execute queries and visualize results.
- Variables and transformations make dashboards reusable and adaptable.
- Grafana and Prometheus provide distinct alerting workflows.
- Dashboard design should help engineers answer operational questions quickly.
- Dashboards and data sources can be provisioned and version-controlled.

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
