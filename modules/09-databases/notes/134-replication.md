# Lesson 134 — Database Replication

## Objectives
- Explain why databases replicate data.
- Compare primary/replica architectures and synchronous/asynchronous replication.
- Understand replication lag, read consistency, failover, RPO, and RTO.
- Distinguish replication from sharding and backups.

## Prerequisites
- Lesson 130 — Database Fundamentals
- Lesson 132 — Transactions
- Lesson 133 — Isolation Levels

## Concept Summary
Replication maintains additional copies of database data on other servers. It can improve availability and distribute read traffic, but introduces consistency, lag, failover, and operational trade-offs.

## Core Ideas
- **Primary/replica:** a common design sends writes to a primary and streams changes to replicas.
- **Incremental replication:** PostgreSQL physical streaming replication uses WAL records to maintain standby state.
- **Asynchronous replication:** the primary does not wait for the configured replica acknowledgement before acknowledging a commit; recent acknowledged writes may be lost during some failures.
- **Synchronous replication:** the primary waits for a configured standby acknowledgement. The exact guarantee depends on whether the standby has written, flushed, or replayed WAL and on failover policy.
- **Replication lag:** a replica may not yet have received or replayed the primary's latest changes.
- **Failover:** promote an eligible replica and redirect writes, while preventing the old primary from accepting conflicting writes.
- **RPO:** acceptable recovery-point/data-loss window. **RTO:** acceptable recovery time.

## Replication vs. Sharding
- Replication keeps copies of the same data on multiple nodes.
- Sharding partitions data across nodes.
- Primary/replica replication does not automatically distribute writes across multiple primaries.

## Practical Example
A user updates their address on the primary and immediately reads from a lagging asynchronous replica. The replica may return the old value. Route read-after-write requests to the primary or use an appropriate consistency mechanism.

## Production Perspective
- Monitor replication connectivity, WAL progress, replay progress, and lag.
- Choose replication acknowledgement guarantees based on durability, latency, and availability requirements.
- Design failover around replica freshness, promotion rules, and split-brain prevention.
- Replication can copy accidental deletions or corrupted writes; maintain and test backups, and consider point-in-time recovery.
- RPO and RTO are recovery objectives, not guarantees created merely by adding replicas.

## Common Misconceptions
- Replicas are always immediately current.
- Synchronous replication guarantees zero data loss under every possible failure.
- Adding replicas automatically scales writes.
- Any replica can be promoted safely without coordination.
- Replication replaces backups.

## Key Takeaways
- Replication improves redundancy and can support read scaling.
- Sync and async modes trade off latency, availability, and loss risk.
- Replica lag can cause stale reads.
- Safe failover must account for data freshness and prevent split brain.
- Replication and backup/recovery are complementary.

## Reflection Questions
1. Does replication divide data across replicas the way sharding does?
2. What can happen if an asynchronous primary fails before its latest WAL reaches a replica?
3. Why can synchronous replication increase write latency or reduce write availability?
4. How can replication lag cause stale reads, and how might an application avoid them?
5. Why is split brain dangerous during failover?
6. Why are backups still needed when a database has synchronous replicas?

## Related Lessons
- Lesson 130 — Database Fundamentals
- Lesson 132 — Transactions
- Lesson 133 — Isolation Levels
- Lesson 135 — Sharding

## What's Next
Lesson 135 — Sharding.
