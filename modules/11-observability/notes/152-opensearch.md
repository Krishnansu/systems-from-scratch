# Lesson 152 — OpenSearch

## Purpose
OpenSearch is an open-source search and analytics engine. In observability, it is commonly used for centralized log storage, search, filtering, aggregation, and analysis across services and infrastructure.

## Architecture
Applications generate logs → collectors/agents (e.g., Fluent Bit, OTel Collector) gather them → logs are parsed/enriched → OpenSearch indexes and stores them → OpenSearch Dashboards supports searching, analyzing, and visualizing.

## Indexing and inverted index
Logs are commonly stored as structured documents. OpenSearch uses inverted indexes to efficiently locate documents matching terms without scanning every document.
An inverted index maps terms to the documents containing them (term → document IDs), rather than mapping documents to their contents. For example, `timeout → D1, D3` enables quick lookup of matching documents. Indexes can also store term frequencies and positions for advanced search.
Mappings define field types and indexing behavior:
- `keyword`: exact matching, filtering, aggregations
- `text`: analyzed full-text search
- Numeric/date fields: ranges, sorting, time filtering
Mapping and field design affect query capability and resource usage.

## Indexes, shards, replicas
- Index: logical collection of documents.
- Shard: partition of an index, enabling distributed storage and parallel search.
- Primary shard: main shard for a partition and writes.
- Replica: copy of a primary shard, improving availability and potentially search capacity.
Shards enable distribution, but too many shards create overhead (memory, metadata, file handles, coordination, and background work). Shard sizing and index design matter.

## Production considerations
- Ingestion rate and burst handling
- Index mappings and field design
- Shard sizing and cluster capacity
- Retention/rollover/deletion policies due to high log volume
- Storage and indexing/search resource costs
- Access control, sensitive data redaction, and secure logging
Time-based indexes or data streams with lifecycle policies are common for log retention and rollover.

## Logs and traces correlation
Structured logs should carry `trace_id` and `span_id`. Search logs by trace ID to inspect events associated with a request; span ID narrows to a specific operation. Metrics detect a symptom, traces locate where time is spent, and logs provide event-level details.

Example investigation: Grafana indicates high API latency → Jaeger identifies a slow payment span → OpenSearch shows timeout/retry/connection-wait logs correlated by trace ID → investigate the cause.

## Reflection review
- Q1 Centralized log search: 9/10
- Q2 Inverted index: 8/10
- Q3 Index/shard/replica: 9.5/10
- Q4 Shard overhead/retention: 9/10
- Q5 Troubleshooting workflow: 10/10
- Total: 45.5/50 (91%)

Key takeaway: An inverted index maps terms to documents, enabling efficient search. Metrics show symptoms, traces locate bottlenecks, and logs help explain events. OpenSearch supports centralized log investigation and correlation with trace/span IDs.
