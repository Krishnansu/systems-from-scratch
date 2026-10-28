# Lesson 137 — Redis

## Objectives
- Explain Redis and its role alongside a traditional database.
- Recognize common Redis data structures and commands.
- Describe cache-aside, TTL, invalidation, and cache stampedes.
- Understand memory limits, eviction, persistence, and command atomicity.

## Prerequisites
- Lessons 130–136: database fundamentals, indexing, transactions, isolation, replication, sharding, and connection pooling.

## Concept Summary
Redis is an in-memory data store with native data structures and efficient operations. It is often used for caching, counters, sessions, rate limiting, leaderboards, and coordination. Its memory-first design offers low latency but introduces memory, durability, consistency, and availability trade-offs.

## Core Ideas
- **Strings:** values, serialized data, counters, and simple flags.
- **Hashes:** field-value records; **lists:** ordered sequences; **sets:** unique members; **sorted sets:** unique members ordered by score; **streams:** append-oriented entries with consumer groups.
- **Cache-aside:** check Redis, load from the source of truth on a miss, then populate the cache.
- **TTL:** expires keys after a configured lifetime; expiration alone does not guarantee freshness.
- **Invalidation:** delete or update cached entries after source data changes. Concurrent reads and writes can still create stale-cache races.
- **Cache stampede:** many requests reload the same expired or missing key concurrently. Consider request coalescing, jittered TTLs, stale-while-revalidate, or controlled refresh.
- **Memory:** Redis data consumes finite RAM. Understand maxmemory and eviction policy; do not assume all keys remain available.
- **Persistence:** RDB snapshots and AOF provide different recovery and data-loss trade-offs. Persistence is not a backup; replication does not prevent replicated mistakes.
- **Atomicity:** individual commands such as INCR are atomic, but multi-command read-check-write workflows are not automatically atomic.

## Practical Example
```redis
SET product:42 '{"name":"Wireless Mouse","price":999}' EX 60
GET product:42
TTL product:42
DEL product:42

HSET user:7 name "Asha" plan "premium"
SADD event:42:attendees user:7 user:8
ZADD leaderboard 950 player:7
ZREVRANGE leaderboard 0 9 WITHSCORES
INCR product:42:views
```

## Production Perspective
- Keep the source of truth and acceptable staleness explicit.
- Handle cache misses and Redis outages without overwhelming the database.
- Monitor hit rate, latency, memory use, evictions, rejected writes, and connection health.
- Choose persistence, replication, and recovery settings according to data-loss requirements.
- Use atomic scripts or other coordination mechanisms when correctness spans multiple commands.
- Evaluate whether Redis is appropriate for critical inventory, financial, or coordination workflows rather than assuming it replaces database transactions.

## Common Mistakes
- Treating cached values as necessarily fresh.
- Assuming TTL alone solves invalidation races.
- Ignoring cache stampedes and hot keys.
- Assuming in-memory data cannot be persisted or that persistence is equivalent to backup.
- Assuming atomic individual commands make a whole workflow atomic.
- Using Redis without a clear memory and eviction budget.

## Key Takeaways
- Redis provides specialized in-memory data structures and fast operations.
- Cache-aside reduces repeated source-database reads but requires a freshness strategy.
- Memory limits, eviction, outages, and persistence must be planned explicitly.
- Command-level atomicity is not workflow-level atomicity.

## Reflection Questions
1. How does cache-aside reduce database load, and what happens when a key expires?
2. PostgreSQL changes a price but Redis retains the old value. Give two mitigation strategies and their trade-offs.
3. Why can a simultaneous cache miss overload the database, and how can it be mitigated?
4. Why use a set rather than a list for unique event attendees?
5. Why does Redis eviction policy matter when memory is full?
6. Why doesn't atomic DECR make a read-check-decrement inventory workflow safe?

## Related Lessons
- Lesson 130 — Database Fundamentals
- Lesson 132 — Transactions
- Lesson 134 — Replication
- Lesson 135 — Sharding
- Lesson 136 — Connection Pooling

## What's Next
Lesson 138 — Why Messaging.
