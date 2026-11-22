# Lesson 153 — Elasticsearch & Kibana

## Objectives
Understand the Elasticsearch ecosystem, its architecture, Kibana's query/visualization capabilities, and how Elastic Stack compares with OpenSearch.

## Prerequisites
- L152 — OpenSearch: indexing, inverted indexes, mappings, shards, replicas.
- L150 — OpenTelemetry.

## Theory
Elasticsearch is a distributed search and analytics engine built on Apache Lucene. It supports centralized log search, full-text search, aggregations, and observability analytics.

OpenSearch originated as a fork of Elasticsearch 7.10.2 and Kibana 7.10.2. The ecosystems have since evolved independently. Elasticsearch pairs with Kibana; OpenSearch pairs with OpenSearch Dashboards. They share historical foundations but APIs, plugins, features, and compatibility are not guaranteed to match.

## Elasticsearch architecture
- Cluster: group of Elasticsearch nodes.
- Node: server/process participating in the cluster.
- Master-eligible node: participates in cluster coordination and management.
- Data node: stores shards and performs indexing/search work.
- Ingest node: runs ingestion pipelines.
- Coordinating node: routes requests and combines results.
Nodes can have multiple roles.

Write flow: client → coordinating node → primary shard → replica shard(s) → acknowledgement.
Search flow: coordinating node routes query to relevant shards → shards execute searches → coordinating node merges results and responds.

## Kibana
Kibana is the UI for exploring and visualizing Elasticsearch data.
- Discover: inspect documents, fields, and filtered results.
- Visualizations: build charts, tables, and aggregations.
- Dashboards: combine visualizations into operational views.
- KQL: concise filtering language for interactive searches.
- Elasticsearch Query DSL: JSON-based query language for richer programmatic queries and aggregations.

## Elastic Stack
- Beats: lightweight data collection agents.
- Elastic Agent: unified agent for logs, metrics, and other telemetry.
- Logstash: ingestion, parsing, transformation, and routing pipeline.
- Elasticsearch: indexing, storage, search, and analytics.
- Kibana: exploration and visualization.
Logstash is optional. Agents can send data directly to Elasticsearch; Elasticsearch ingest pipelines can also process documents. OpenTelemetry can instrument applications and export telemetry through supported integrations/collectors without requiring application-level Elastic-specific instrumentation.

## Production perspective
- Cluster health: green = all primary and replica shards allocated; yellow = all primaries allocated but some replicas unallocated; red = at least one primary unallocated.
- High indexing rates compete with search for CPU, memory, and I/O.
- Newly indexed documents become searchable after refresh; write acknowledgement and search visibility are not necessarily simultaneous.
- Use rollover and retention/lifecycle policies to control storage growth.
- Secure clusters with authentication, role-based access control, TLS, and sensitive-data handling.

## Elasticsearch vs OpenSearch
| Elasticsearch ecosystem | OpenSearch ecosystem |
|---|---|
| Elasticsearch | OpenSearch |
| Kibana | OpenSearch Dashboards |
| Elastic Agent / Beats / Logstash | OpenSearch integrations and compatible ingestion tools |

Both support distributed search, indexing, aggregations, shards, replicas, and observability use cases. APIs, query features, plugins, clients, and operational controls may differ. Do not assume drop-in compatibility.

## Key Takeaways
- Elasticsearch is the search/storage engine; Kibana is its exploration and visualization interface.
- OpenSearch and Elasticsearch share historical roots but are separate evolving ecosystems.
- Elastic Stack collection and processing components are flexible; Logstash is not mandatory.
- Cluster health, ingestion pressure, refresh behavior, retention, and security are important operational concerns.

## Reflection Questions
1. How are Elasticsearch and OpenSearch related? Why shouldn't we assume they are interchangeable?
2. What are the responsibilities of master, data, ingest, and coordinating nodes in an Elasticsearch cluster?
3. Explain the difference between KQL and Elasticsearch Query DSL. When would you use each?
4. What roles do Beats/Elastic Agent and Logstash play in the Elastic Stack? Is Logstash mandatory?
5. An Elasticsearch cluster reports yellow health. What does that mean, and how would you investigate?
