# Lesson 140 — Kafka

## Objectives
- Explain Kafka's distributed event-log architecture.
- Understand topics, partitions, records, keys, and offsets.
- Explain brokers, replication, leaders, followers, and ISR.
- Understand consumer groups, partition assignment, and offset commits.
- Explain retention, replay, and log compaction.
- Understand ordering, delivery semantics, and consumer lag.
- Compare Kafka with RabbitMQ.

## Prerequisites
- Lesson 138 — Why Messaging?
- Lesson 139 — RabbitMQ

## Concept Summary
Kafka is a distributed event-streaming platform. Producers append records to partitioned topics. Brokers store and replicate partitions. Consumer groups independently read records and track progress using offsets. Records remain available according to retention or compaction policies, enabling replay and independent downstream processing.

## Core Ideas
- **Topic:** Named stream of related records, such as `orders` or `payments`.
- **Record:** Event containing a key, value, timestamp, and optional headers.
- **Partition:** Ordered sequence of records within a topic. Partitions distribute storage and processing.
- **Offset:** Position within one partition. There is no global topic-wide ordering or offset.
- **Partition key:** Commonly hashes a key to select a partition. Using `orderId` can preserve per-order ordering, but hot keys can create uneven load.
- **Broker:** Kafka server that stores and serves partition data.
- **Replication:** A partition has a leader and follower replicas. Producers normally write to the leader; followers replicate its log.
- **ISR:** In-Sync Replicas considered sufficiently caught up. `acks=all` waits for the current ISR; `min.insync.replicas` establishes the minimum ISR size for accepting writes.
- **Consumer group:** Consumers cooperate to process a topic. A partition is assigned to at most one consumer in a group at a time. Different groups independently consume the same topic.
- **Parallelism:** Active consumers in a group are bounded by assigned partitions. Membership or assignment changes can trigger a rebalance.
- **Offset commits:** A committed offset conventionally identifies the next record to read. Committing before processing risks loss; processing before committing risks duplicate processing.
- **Idempotency:** Commit deduplication and business database effects atomically where possible. Kafka offset commits are not automatically atomic with an external database or API.
- **Retention:** `retention.ms` and `retention.bytes` govern time/size-based record retention. Replay is possible only while records remain available.
- **Log compaction:** Eventually retains the latest record per key, useful for reconstructing latest keyed state rather than preserving every historical update.
- **Delivery semantics:** At-least-once is common. Kafka idempotent producers and transactions support exactly-once behavior within defined Kafka processing boundaries, not arbitrary external side effects.
- **Throughput:** Batching, compression, sequential log writes, partitioning, and consumer parallelism contribute to throughput.
- **Consumer lag:** Difference between latest available data and a group's progress. Investigate slow processing, downstream bottlenecks, insufficient partitions, and hot partitions.

## Practical Example
An `orders` topic is partitioned by `orderId`. Analytics, fraud detection, notifications, and warehouse ingestion use separate consumer groups. Each application tracks its own offsets. Analytics can create a new group or reset offsets to rebuild metrics from retained events.

## Production Perspective
Monitor consumer lag per partition, processing latency, producer throughput, broker disk usage, replication health, under-replicated partitions, and failed processing. Choose partition keys based on ordering requirements and traffic distribution. Size retention for replay needs and storage capacity. Ensure downstream consumers are idempotent.

## Common Mistakes
- Assuming offsets or ordering are global across a topic.
- Running more consumers than useful partition assignments.
- Committing offsets before processing without accepting loss risk.
- Assuming Kafka retention is an indefinite archive.
- Assuming `acks=all` means every configured replica must acknowledge.
- Assuming Kafka transactions cover external databases or APIs.
- Increasing partitions or consumers without considering hot keys and downstream capacity.

## Key Takeaways
- Partitions provide parallelism and define the ordering boundary.
- Consumer groups provide independent progress and parallel consumption.
- Offsets track progress; commit timing affects duplicate/loss behavior.
- Retention enables replay; compaction preserves latest keyed state.
- Replication improves fault tolerance, subject to ISR and acknowledgment configuration.
- Kafka emphasizes retained event streams; RabbitMQ emphasizes flexible routing and work distribution.

## Reflection Questions
1. A topic has 6 partitions and a group has 8 consumers. How many can receive partition assignments?
2. Why should independent applications use different consumer groups?
3. What happens if a consumer crashes after a database update but before offset commit?
4. Why might `orderId` be a good partition key, and what is a hot key?
5. What must be configured for 30-day replay?
6. What does `min.insync.replicas` control when using `acks=all`?
7. When might RabbitMQ be a better choice than Kafka?

## Related Lessons
- Lesson 138 — Why Messaging?
- Lesson 139 — RabbitMQ

## What's Next
Lesson 141 — Event-Driven Architecture.
