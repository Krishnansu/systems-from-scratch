# Lesson 152 — OpenSearch

## Purpose
OpenSearch is an open-source search and analytics engine. In observability, it is commonly used for centralized log storage, search, filtering, aggregation, and analysis across services and infrastructure.

## Architecture
Applications generate logs → collectors/agents (e.g., Fluent Bit, OTel Collector) gather them → logs are parsed/enriched → OpenSearch indexes and stores them → OpenSearch Dashboards supports searching, analyzing, and visualizing.

## Indexing
Logs are commonly stored as structured documents. OpenSearch uses inverted indexes to efficiently locate documents matching terms without scanning every document. Mappings define field types and indexing behavior:
- `keyword`: exact matching, filtering, aggregations
- `text`: analyzed full-text search
- Numeric/date fields: ranges, sorting, time filtering

Mapping and field design affect query capability and resource usage.

## Indexes, shards, replicas
- Index: logical collection of documents.
- Shard: partition of an index, enabling distributed storage and parallel search.
- Primary shard: main shard for a partition and writes.
- Replica: copy of a primary shard, improving availability and potentially search capacity.
Shards enable distribution, but too many shards create overhead. Shard sizing and index design matter.

## Production considerations
- Ingestion rate and burst handling
- Index mappings and field design
- Shard sizing and cluster capacity
- Retention/rollover/deletion policies due to high log volume
- Storage and indexing/search resource costs
- Access control, sensitive data redaction, and secure logging
Time-based indexes or data streams with lifecycle policies are common for log retention and rollover.

## Logs and traces correlation
Structured logs should carry `trace_id` and optionally `span_id`. Search logs by trace ID to inspect events associated with a request; span ID narrows to a specific operation. Metrics detect a symptom, traces locate where time is spent, and logs provide event-level details and context.

Example investigation: Grafana indicates high API latency → Jaeger identifies a slow payment span → OpenSearch shows timeout/retry/connection-wait logs correlated by trace ID → investigate the cause.

## Reflection questions
1. Why is OpenSearch preferable to searching log files manually across individual service instances?
2. What is an inverted index, and how does it improve search?
3. Explain the difference between an index, a shard, and a replica.
4. Why can having too many shards be harmful, and why are log retention policies important?
5. An alert shows API latency increased. Jaeger identifies a slow payment span, and OpenSearch shows timeout and retry logs. Explain how these signals together help you troubleshoot.
