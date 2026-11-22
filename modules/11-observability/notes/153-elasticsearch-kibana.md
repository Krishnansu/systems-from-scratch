# Lesson 153 — Elasticsearch & Kibana

## Objectives
Understand the Elasticsearch ecosystem, its architecture, Kibana's query/visualization capabilities, and how it compares with OpenSearch.

## Elasticsearch and OpenSearch
Elasticsearch is a distributed search and analytics engine built on Apache Lucene. OpenSearch originated as a fork of Elasticsearch 7.10.2 and Kibana 7.10.2. Both ecosystems support similar search, indexing, analytics, and observability use cases but have evolved independently. APIs, plugins, features, integrations, and compatibility should not be assumed interchangeable.

- Elasticsearch pairs with Kibana.
- OpenSearch pairs with OpenSearch Dashboards.

## Elasticsearch architecture
- Cluster: group of Elasticsearch nodes.
- Master-eligible node: participates in cluster coordination; an election selects the active master.
- Data node: stores shards and performs indexing/search.
- Ingest node: runs ingestion pipelines.
- Coordinating node: routes requests and combines results. Every node can perform coordinating duties; dedicated coordinating nodes focus on this role.
- Nodes can have multiple roles.

Write flow: client → coordinating node → primary shard → replica shard(s) → acknowledgement.
Search flow: coordinating node routes query to relevant shards → shards execute searches → coordinating node merges results.

## Kibana
Kibana is the UI for exploring and visualizing Elasticsearch data.
- Discover: inspect documents, fields, and filtered results.
- Visualizations: build charts, tables, and aggregations.
- Dashboards: combine visualizations into operational views.
- KQL: concise filtering language for interactive searches.
- Elasticsearch Query DSL: JSON-based query language for richer programmatic queries, compound filters, sorting, scoring, and aggregations.

## Elastic Stack
- Beats: lightweight agents such as Filebeat and Metricbeat.
- Elastic Agent: unified agent for collecting logs, metrics, and other telemetry.
- Logstash: ingestion, parsing, transformation, and routing pipeline.
- Elasticsearch: indexing, storage, search, and analytics.
- Kibana: exploration and visualization.
Logstash is optional. Agents can send data directly to Elasticsearch; Elasticsearch ingest pipelines can process documents during ingestion. Logstash provides more extensive processing and routing capabilities. OpenTelemetry can instrument applications and export telemetry through supported integrations/collectors.

## Production perspective
- Cluster health: green = all primary and replica shards allocated; yellow = all primaries allocated but some replicas unallocated; red = at least one primary unallocated.
- Investigate yellow/red status using `GET /_cluster/health`, `GET /_cat/shards?v`, and `POST /_cluster/allocation/explain`.
- Common unallocated replica causes: insufficient eligible nodes, allocation constraints, disk watermarks, node failures, and resource constraints.
- High indexing rates compete with search for CPU, memory, and I/O.
- Newly indexed documents become searchable after refresh; write acknowledgement and search visibility are not necessarily simultaneous.
- Use rollover and retention/lifecycle policies to control storage growth.
- Secure clusters with authentication, role-based access control, TLS, and sensitive-data handling.

## Reflection review
- Q1 Elasticsearch vs OpenSearch: 10/10
- Q2 Node roles: 9.5/10
- Q3 KQL vs Query DSL: 10/10
- Q4 Elastic Stack ingestion: 10/10
- Q5 Cluster health: 8.5/10
- Total: 48/50 (96%)

Key takeaways:
- Elasticsearch and OpenSearch are separate ecosystems with similar core concepts but different implementations and compatibility.
- Elasticsearch node roles separate cluster coordination, data storage, ingestion, and request coordination.
- KQL is convenient for interactive filtering; Query DSL provides richer JSON-based query capabilities.
- Logstash is optional; Elasticsearch ingest pipelines also support processing.
- Yellow health means all primary shards are allocated but some replicas are not. Investigate unallocated shards and allocation explanations.
