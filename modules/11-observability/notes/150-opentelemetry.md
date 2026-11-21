# Lesson 150 — OpenTelemetry

## Objectives
- Understand why OpenTelemetry exists and its vendor-neutral approach.
- Know the roles of instrumentation, API, SDK, OTLP, and Collector.
- Understand Collector pipelines and Agent/Gateway deployments.
- Connect OTel with existing observability backends.

## Concept Summary
OpenTelemetry (OTel) is a vendor-neutral observability framework for generating, collecting, processing, and exporting telemetry (traces, metrics, and logs). It standardizes instrumentation and telemetry pipelines without requiring a specific backend.

## Core Ideas
- **Instrumentation:** Generates telemetry. Automatic instrumentation captures common framework/library operations; manual instrumentation adds application-specific visibility.
- **API:** Interfaces used to instrument code.
- **SDK:** Implements the API and manages recording, sampling, processing, and export behavior.
- **OTLP:** OpenTelemetry Protocol for transporting telemetry, commonly over gRPC or HTTP.
- **Collector:** Vendor-neutral service that receives, processes, and exports telemetry. Optional but widely useful.
- **Pipeline:** Receiver → Processor → Exporter. Receivers ingest; processors batch, filter, enrich, sample, etc.; exporters forward to destinations. Separate pipelines can be configured per signal.
- **Context propagation:** Propagates trace context (commonly W3C Trace Context) across service boundaries, linking distributed spans.
- **Agent deployment:** Local/host/node collection, often a Kubernetes DaemonSet.
- **Gateway deployment:** Centralized Collector tier for processing, routing, filtering, and exporting. Agent and Gateway patterns can be combined.
- **Backend independence:** Applications can change telemetry destinations without rewriting instrumentation.

## Architecture

```text
Application Instrumentation
       │
       │ OTLP
       ▼
OpenTelemetry Collector
 Receiver → Processor → Exporter
       │
       ├──► Metrics backend (e.g., Prometheus-compatible)
       ├──► Trace backend (e.g., Jaeger)
       └──► Log backend (e.g., OpenSearch)
                   │
             Visualization
          (Grafana / backend UI)
```

## Integration
| Signal | Collection | Backend | Visualization |
|---|---|---|---|
| Metrics | OTel SDK / Collector | Prometheus or compatible backend | Grafana |
| Traces | OTel SDK / Collector | Jaeger | Jaeger UI / Grafana |
| Logs | OTel SDK / Collector / agents | OpenSearch | OpenSearch Dashboards / Grafana |

OTel standardizes instrumentation and the telemetry pipeline; it is not the storage or visualization backend.

## Production Perspective
- Collectors can batch, enrich with metadata, filter, sample, route, and export telemetry.
- Reliability depends on queue/buffer sizing, retry behavior, backend availability, and configuration; telemetry may still be dropped.
- Watch sampling, cardinality, resource/network overhead, sensitive data, backpressure, and dropped telemetry.
- Collectors can be scaled horizontally, but routing and stateful sampling considerations may matter.

## Common Misconceptions
- OTel is a telemetry database or dashboard.
- OTel is Jaeger or replaces Prometheus.
- Automatic instrumentation captures all business logic.
- Collector is mandatory for every application.
- Telemetry delivery is guaranteed without configuring reliability mechanisms.

## Key Takeaways
- OTel provides vendor-neutral instrumentation and telemetry collection/export.
- API and SDK are used by application instrumentation; OTLP transports telemetry.
- Collector pipelines use Receivers → Processors → Exporters.
- Agent and Gateway Collector deployments can be combined.
- Context propagation links telemetry across services.
- Metrics, traces, and logs can be exported to separate backends.

## Reflection Questions
1. What problem does OTel solve, and why is it vendor-neutral?
2. Explain the difference between the OTel API, SDK, Collector, and OTLP.
3. Describe a Collector pipeline using Receiver → Processor → Exporter.
4. What is the difference between Agent and Gateway deployments? Why might production use both?
5. In an Order → Payment → Inventory request, how does OTel connect telemetry, and where might metrics, traces, and logs be stored?

## Hands-on Exercise
Describe the telemetry flow for a 3-service application using automatic instrumentation, OTLP, Collector, Prometheus, Jaeger, OpenSearch, and Grafana. Identify where data originates, travels, gets processed, stored, and queried.

## Related Lessons
- Lesson 145 — Metrics
- Lesson 146 — Tracing
- Lesson 148 — Prometheus
- Lesson 149 — Grafana

## What's Next
Lesson 151 — Jaeger.
