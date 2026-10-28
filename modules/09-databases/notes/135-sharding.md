# Lesson 135 — Database Sharding

## Objectives
- Explain why sharding is used and how it differs from replication.
- Compare range-, hash-, and directory-based sharding.
- Understand shard keys, routing, hot shards, cross-shard operations, and resharding.

## Prerequisites
- Lesson 130 — Database Fundamentals
- Lesson 131 — Indexing
- Lesson 132 — Transactions
- Lesson 133 — Isolation Levels
- Lesson 134 — Replication

## Concept Summary
Sharding partitions a logical dataset across multiple database servers. Each shard owns a subset of the data, allowing storage and workload to scale beyond a single server while introducing routing and distributed-operation complexity.

## Core Ideas
- **Shard key:** field or combination of fields used to determine data placement and request routing.
- **Good shard key:** supports even data and workload distribution, common-query locality, sufficient cardinality, and stable placement.
- **Range sharding:** assigns key ranges to shards; useful for range queries but may create hotspots for sequential keys.
- **Hash sharding:** hashes a key to distribute records; often balances keys but complicates range queries and remapping when shard counts change.
- **Directory-based sharding:** uses metadata mapping keys or groups to shards; flexible but depends on correct, available routing metadata.
- **Hot shard:** a shard overloaded by data skew or request skew, even if record counts appear balanced.
- **Cross-shard query:** may fan out to multiple shards and merge results, increasing latency and failure complexity.
- **Cross-shard transaction:** requires supported distributed coordination or an application-level workflow; a local transaction does not automatically provide atomicity across independent servers.
- **Resharding:** requires controlled data movement, synchronization of concurrent writes, safe routing changes, and verification of ownership.

## Sharding vs. Replication
- Sharding divides data ownership among nodes.
- Replication maintains copies of the same data.
- A sharded architecture can replicate each shard for availability and read scaling.

## Practical Example
For a multi-tenant SaaS application, `tenant_id` may localize most tenant-scoped requests to one shard. Very large tenants may still become hot, and global reports may need distributed aggregation or a separate analytics pipeline.

## Production Perspective
- Choose the shard key based on real access patterns and both data and traffic distributions.
- Monitor per-shard CPU, storage, latency, request volume, and skew.
- Define authoritative ownership and safe behavior for unavailable or stale routing metadata.
- Plan migrations and resharding before capacity pressure becomes urgent.
- Keep replication, backup, and recovery plans for each shard.

## Common Misconceptions
- Sharding and replication are the same.
- More shards automatically make every query faster.
- Hashing guarantees balanced request traffic.
- A primary key must always be the shard key.
- Adding a shard completes resharding without data migration or routing changes.
- Sharding removes the need for backups.

## Key Takeaways
- Sharding distributes a dataset; replication copies data.
- Shard-key design determines placement, routing, and query locality.
- Hotspots can come from popular keys as well as uneven data volume.
- Cross-shard queries and transactions add coordination and failure complexity.
- Safe resharding preserves ownership and concurrent-write correctness.

## Reflection Questions
1. How can sharding help with write throughput, and what does it not guarantee?
2. Why can a time-based range shard become a write hotspot?
3. How would you choose between `tenant_id` and `user_id` for a multi-tenant application?
4. Why can global aggregation become more expensive after sharding?
5. What can go wrong when routing metadata is stale during resharding?
6. How would you combine sharding, replication, and backups?

## Related Lessons
- Lesson 131 — Indexing
- Lesson 132 — Transactions
- Lesson 133 — Isolation Levels
- Lesson 134 — Replication
- Lesson 136 — Connection Pooling

## What's Next
Lesson 136 — Connection Pooling.
