# Lesson 135 — Sharding: Practice Reference

These examples illustrate concepts using PostgreSQL-compatible SQL. PostgreSQL table partitioning is not the same as distributing shards across independent database servers.

## Illustrative range-partitioned table

```sql
CREATE TABLE events (
    event_id BIGINT NOT NULL,
    tenant_id BIGINT NOT NULL,
    created_at DATE NOT NULL,
    payload TEXT
) PARTITION BY RANGE (created_at);

CREATE TABLE events_2026_q1
    PARTITION OF events
    FOR VALUES FROM ('2026-01-01') TO ('2026-04-01');

CREATE TABLE events_2026_q2
    PARTITION OF events
    FOR VALUES FROM ('2026-04-01') TO ('2026-07-01');
```

The lower bound is inclusive and the upper bound exclusive. These examples define two quarterly partitions only; inserts outside the defined ranges need an appropriate partition or will fail.

## Inspect partition metadata

```sql
SELECT
    parent.relname AS parent_table,
    child.relname AS partition_name
FROM pg_inherits
JOIN pg_class parent ON pg_inherits.inhparent = parent.oid
JOIN pg_class child ON pg_inherits.inhrelid = child.oid
WHERE parent.relname = 'events';
```

## Conceptual routing examples

- Range: choose the shard whose configured key range contains the value.
- Hash: hash the shard key and map the result to a shard using the system's routing scheme.
- Directory: look up the key or tenant in an authoritative placement map.

Do not treat `hash(key) % shard_count` as a migration-safe placement scheme. Changing the shard count can remap many keys.

## Design checklist

- Identify the dominant query patterns and required locality.
- Estimate both record distribution and request distribution.
- Check whether common queries can identify one shard.
- Identify global reports and cross-shard transactions.
- Define ownership metadata and its consistency requirements.
- Plan migration, concurrent-write handling, verification, and rollback.
- Monitor per-shard load and retain per-shard backup and recovery procedures.

## Safety

- Use a disposable database or approved development environment.
- These SQL statements create tables and partitions; they change database state.
- Do not experiment with production sharding or data movement without an approved migration plan.
- Clean up only objects created for the exercise, and only after confirming the target database.
