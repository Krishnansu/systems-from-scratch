# Lesson 55 — Caching

## Objectives

- Understand why caching exists and what problem it solves.
- Understand cache hits, misses, TTL, expiration, and eviction.
- Understand cache hierarchy from browser/CDN to application caches.
- Understand cache-aside and other cache access patterns.
- Understand cache invalidation, stale data, cache stampedes, and hot keys.
- Understand cache consistency and common DB/cache race conditions.
- Understand concurrent updates, lost updates, atomic operations, pessimistic locking, and optimistic concurrency control.
- Understand the architectural difference between a cache such as Redis and a database.
- Build a production-oriented mental model for distributed caching.

## Prerequisites

- HTTP caching fundamentals
- HTTP request/response lifecycle
- Sessions and JWT
- Basic understanding of databases
- Basic understanding of concurrency

## Theory

Caching stores a copy of data so repeated requests can be served faster and the underlying source of truth receives less work.

The fundamental flow is:

```text
Request
   |
   v
 Cache?
  /   \\
Hit   Miss
 |      |
 v      v
Data   Source
         |
         v
       Cache
         |
         v
      Response
```

A cache is normally a derived copy, while the database or origin remains the source of truth.

### Why caching exists

Caching primarily provides:

- Lower latency
- Higher throughput
- Reduced database/backend load
- Reduced network distance when caching occurs at the edge

Caching introduces trade-offs: stale data, invalidation complexity, memory cost, and cache failure modes.

### Cache hierarchy

A request can encounter several caching layers:

```text
Browser
   |
   v
CDN
   |
   v
Reverse Proxy
   |
   v
Application Cache
   |
   v
Distributed Cache
   |
   v
Database
```

Each layer serves a different purpose. A CDN primarily brings content closer to users, while an application/distributed cache reduces backend work and latency.

### Cache hit and miss

A cache hit means the requested key is present and usable in the cache. A cache miss means the application must obtain the value from another source, commonly the database, and may then populate the cache.

```text
GET key
   |
   v
 Cache?
  /   \\
Hit   Miss
 |      |
 v      v
Value   DB
          |
          v
        Cache
```

### TTL and expiration

TTL (Time To Live) limits how long an entry remains valid. A long TTL improves hit rate but permits data to remain stale for longer. A short TTL improves freshness but causes more misses.

TTL is different from eviction: TTL answers when an entry expires, while eviction answers which entry should be removed when cache capacity is constrained.

TTL can also act as a safety bound for stale data. If invalidation fails, the entry eventually expires, although it may remain stale until that happens.

### Eviction

Common eviction approaches include:

- LRU — Least Recently Used
- LFU — Least Frequently Used
- FIFO — First In, First Out
- MRU — Most Recently Used
- Random eviction

Real systems may use more sophisticated combinations of recency, frequency, and aging.

## Cache Access Patterns

The central question behind cache access patterns is:

> Who is responsible for loading data into the cache and keeping the cache synchronized with the source of truth?

### Cache-aside

The application explicitly checks and populates the cache:

```text
Application
    |
    v
  Cache?
  /    \\
HIT    MISS
 |       |
 |       v
 |     Database
 |       |
 |       v
 |      Cache
 |       |
 +-------+
    |
    v
Response
```

On a miss, the application reads from the source of truth, stores the result in the cache, and returns it.

Cache-aside is common because the application retains explicit control over what gets cached.

### Read-through

With read-through caching, the application talks to the cache layer and the cache itself knows how to load missing data from the backing store.

```text
Application
     |
     v
   Cache
     |
    MISS
     |
     v
    DB
     |
     v
   Cache
     |
     v
Application
```

This moves cache-miss loading logic into the cache abstraction rather than duplicating it throughout application code.

### Write-through

The application writes through the cache, and the cache synchronously writes the backing store.

```text
Application
     |
   WRITE
     v
   Cache
     |
   WRITE
     v
    DB
```

The write is generally considered complete only after the backing store has also been updated. This improves synchronization but adds write latency and coupling between the cache and database.

### Write-back / write-behind

The application writes to the cache and the cache asynchronously persists the change to the backing store.

```text
Application
     |
   WRITE
     v
   Cache ---- later ----> DB
     |
     v
  success
```

This can make writes very fast, but introduces a durability window: if the cache fails before the database write occurs, the update may be lost unless additional durability mechanisms exist.

### Write-around

The application writes directly to the database and does not immediately populate the cache.

```text
Application
     |
     v
    DB
```

A later cache miss loads the value into the cache. This can avoid filling the cache with data that is written frequently but rarely read.

### Pattern summary

| Pattern | Read responsibility | Write responsibility |
|---|---|---|
| Cache-aside | Application | Application |
| Read-through | Cache | — |
| Write-through | — | Cache → DB synchronously |
| Write-back | — | Cache → DB asynchronously |
| Write-around | — | Application → DB |

These patterns can be combined, such as read-through + write-through.

## Cache Consistency

The difficult part of caching is not storing data. It is keeping multiple copies of state sufficiently synchronized for the application's correctness requirements.

Consider:

```text
DB    = Alice
Cache = Alice
```

An update changes the database:

```text
UPDATE DB → Bob
```

If the cache still contains Alice, the next cache hit can return stale data.

### Update DB → Delete cache

A common cache-aside invalidation sequence is:

```text
UPDATE DB
   |
   v
DELETE CACHE
```

The next read misses the cache and repopulates it from the database.

This is simple and widely useful, but distributed systems introduce races.

### Database replica lag

Suppose the database uses replication:

```text
             +----------+
             | Primary  |
             +----------+
                  |
             replication
                  |
          +-------+-------+
          v               v
      Replica A        Replica B
```

After a write:

```text
Primary = Bob
Replica = Alice
Cache   = Alice
```

If the cache is invalidated and a cache miss reads from a lagging replica, the old value can be placed back into the cache:

```text
DELETE CACHE
     |
CACHE MISS
     |
READ REPLICA
     |
Alice
     |
SET CACHE
     |
Cache = Alice  <- stale again
```

Therefore cache consistency depends on the consistency characteristics of the database and other services beneath the cache.

### Update cache instead of deleting it

Another strategy is:

```text
UPDATE DB
   |
   v
SET CACHE(new value)
```

This avoids a subsequent cache miss but creates another failure case: the database update may succeed while the cache update fails.

### Delete cache before updating DB

Deleting first also has a race:

```text
DELETE CACHE
     |
     | DB update not finished
     |
     v
Another request reads
     |
CACHE MISS
     |
READ old DB value
     |
SET old value in cache
```

Moving invalidation earlier therefore does not automatically solve consistency.

## Strong vs Eventual Consistency

Strong consistency means a successful write is followed by reads that observe the newest state according to the system's consistency guarantees.

Eventual consistency allows temporary stale reads while the system converges toward the latest state.

Caching frequently introduces eventual-consistency windows. Whether that is acceptable depends on the business requirement.

Examples:

| Data | Typical tolerance for staleness |
|---|---|
| Profile picture | High |
| Product description | Moderate |
| News content | Moderate |
| Leaderboard | Often seconds are acceptable |
| Inventory | Low |
| Bank balance | Very low |
| Payment status | Very low |

The key design question is:

> How stale can this data safely be?

## Cache Stampede and Hot Keys

A cache stampede occurs when many requests simultaneously miss the same popular key and all hit the origin/database.

Common mitigations include:

- Request coalescing / single-flight
- Locking around cache population
- Jittered expiration
- Stale-while-revalidate

A hot key is a disproportionately popular key that can overload one cache node even when the overall cache cluster has sufficient capacity.

## Concurrent Updates and Lost Updates

Caching systems frequently interact with concurrent writes, but the underlying lost-update problem exists even without a cache.

Suppose:

```text
counter = 100
```

Two requests arrive:

```text
A: +10
B: +20
```

A naive read-modify-write implementation can produce:

```text
A: READ 100
B: READ 100

A: WRITE 110
B: WRITE 120

Final = 120  <- A's update was lost
```

The logical result should be:

```text
100 + 10 + 20 = 130
```

This is a lost update.

## Solving Concurrent Updates

There is no single universal solution. The correct mechanism depends on the operation and its consistency requirements.

### 1. Pessimistic locking

A database transaction can lock the relevant row before reading and modifying it.

```text
counter = 100

A: acquire lock
A: read 100
A: write 110
A: commit
A: release lock

B: acquire lock
B: read 110
B: write 130
B: commit
B: release lock
```

This serializes conflicting operations. It is useful when operations involve business invariants that must be checked while the state is protected.

However, locking a highly contended resource can become a throughput bottleneck.

### 2. Atomic operations

For naturally composable operations such as increments, prefer an atomic state transition when the datastore supports it.

Conceptually:

```text
counter = 100

A: INCREMENT BY 10
B: INCREMENT BY 20

Final = 130
```

The important principle is:

> Prefer an atomic datastore operation over application-level READ → CALCULATE → WRITE when possible.

SQL can perform the same idea:

```sql
UPDATE accounts
SET counter = counter + 10
WHERE id = 123;
```

Redis also provides atomic increment operations such as `INCR` and `INCRBY`.

### 3. Optimistic concurrency control

Instead of blocking writers, the system detects conflicting updates using a version number.

Initial state:

```text
value   = 100
version = 5
```

Both A and B read version 5.

A updates conditionally:

```text
UPDATE ...
WHERE version = 5
```

A succeeds and creates:

```text
value   = 110
version = 6
```

B's update still expects version 5, so it affects zero rows. B detects the conflict, rereads the current value, recalculates, and retries.

```text
B:
READ 110
calculate 130
UPDATE where version = 6
        |
      success
```

This is optimistic concurrency control: allow concurrent work, detect conflicts, and retry when necessary.

### 4. Event/log-based approaches

For extremely high-contention workloads, repeatedly updating one mutable value can become a bottleneck.

An alternative is to record operations/events and aggregate them:

```text
Requests
   |
   v
Event stream
   |
   v
Consumers
   |
   v
Aggregated state
```

This can increase scalability and reduce contention, but usually introduces additional complexity and potentially eventual consistency.

## Distributed Locks

A distributed application cannot rely on ordinary process-local locks:

```text
App A → local lock
App B → local lock
```

A's lock is invisible to B.

A real distributed lock requires shared coordination:

```text
App A ──┐
App B ──┼──> Shared coordination mechanism
App C ──┘
```

Distributed locks introduce their own concerns:

- Lock expiration
- Client crashes
- Ownership
- Network failures
- Retries
- Stale lock holders
- Split-brain scenarios

Therefore distributed locking should not automatically be the first answer. If an atomic datastore operation or database transaction can solve the problem more simply, prefer that approach.

## Cache vs Database

A cache and a database both store and retrieve data, but their responsibilities differ.

A database is normally the authoritative, durable source of state. It is designed around persistent storage, indexing/querying, consistency, recovery, and large datasets.

Redis is an in-memory data store commonly used as a cache. Its working dataset resides in RAM, providing very low latency. Redis can also be used as a primary datastore for appropriate workloads, but it should not be assumed to be a universal replacement for databases.

The key distinction is not simply RAM versus disk. Modern databases also use RAM heavily, and Redis supports persistence. The deeper distinction is the system's data model, durability expectations, query model, scaling characteristics, workload, and cost.

## Redis and Distributed Memory

A distributed Redis deployment consists of multiple physical or virtual machines running Redis processes. Each process primarily keeps its working dataset in that machine's RAM.

Sharding distributes keys across nodes:

```text
product:123
     |
     v
Determine shard
     |
     v
Redis Node B
     |
     v
Node B RAM
```

Replication creates additional copies on other nodes. Sharding answers "where does this key live?" while replication answers "how many nodes have a copy?"

## Failure Model

If a cache node fails and the cache contains only derived data, the application can often recover by reading the source of truth and repopulating the cache. Replication can reduce availability impact and recovery time.

If Redis itself is the source of truth, however, losing Redis data can be a data-loss event unless persistence and recovery mechanisms are in place.

## Production Decision Framework

When designing a cached piece of state, ask:

1. What is the source of truth?
2. How stale can the cached value safely be?
3. What happens on a cache miss?
4. How is the cache invalidated or refreshed after writes?
5. Can database replica lag make cache repopulation stale?
6. What happens if invalidation fails?
7. What happens if the cache disappears?
8. Is the workload vulnerable to a stampede?
9. Is there a hot key?
10. Can concurrent updates produce lost updates?
11. Can the datastore perform the state transition atomically?
12. If not, should the system use a transaction, pessimistic locking, optimistic concurrency, or another coordination mechanism?

## Real World Example

Consider a product API:

```text
GET /products/123
```

Without caching:

```text
Client → Application → Database → Application → Client
```

With cache-aside:

```text
Client → Application → Redis
                         |
                       HIT → Client
                         |
                       MISS
                         v
                     Database
                         |
                         v
                       Redis
                         |
                         v
                       Client
```

If product 123 is requested thousands of times but changes infrequently, most requests can avoid the database.

Now consider a write:

```text
UPDATE product
      |
      v
UPDATE DB
      |
      v
DELETE Redis key
```

The next read repopulates the cache. The design must still account for races, replica lag, invalidation failure, and acceptable staleness.

## Hands-on Exercise

1. Pick a frequently requested API response such as a product or user profile.
2. Design a cache key for it.
3. Decide an appropriate TTL based on how stale the data may safely become.
4. Describe what happens on a cache hit and cache miss.
5. Decide how the cache is invalidated when the underlying record changes.
6. Identify what happens if the cache disappears completely.
7. Identify a possible hot key and cache stampede scenario.
8. For a counter receiving concurrent increments, compare atomic increment, pessimistic locking, and optimistic concurrency control.
9. Identify a workload where a distributed lock would be justified and explain why an atomic operation would not be sufficient.

## Common Misconceptions

- A cache is not necessarily Redis; browser caches and CDNs are also caches.
- Redis is not merely a temporary key-value map; it is a powerful in-memory data store that can also persist data.
- "Database uses disk and Redis uses RAM" is useful intuition, but not a strict physical distinction. Databases use RAM extensively, and Redis supports persistence.
- TTL and eviction are not the same thing.
- A cache hit does not mean the data is guaranteed to be perfectly fresh.
- Distributed caching does not mean one giant shared RAM module; it means multiple machines collectively provide the cache.
- A cache does not automatically make a database unnecessary.
- A write lock is not the universal solution to concurrent updates.
- Atomic operations are often preferable to locking for naturally composable operations such as increments.
- Optimistic concurrency is not the same as pessimistic locking: optimistic concurrency detects conflicts rather than blocking them up front.
- A distributed lock is not simply a mutex shared magically between application processes; it requires a coordination mechanism and has failure modes of its own.

## Summary

Caching keeps frequently needed data closer to the consumer and avoids repeated expensive work. Caches can exist at many layers, from browsers and CDNs to application-local and distributed caches such as Redis.

Cache-aside is a common pattern, while read-through, write-through, write-back, and write-around provide different ways to distribute responsibility between the application, cache, and source of truth.

The difficult part of caching is consistency. Cache invalidation, stale data, replica lag, concurrent updates, and race conditions can cause incorrect or temporarily stale results. TTL provides an expiration bound but does not itself guarantee freshness.

For concurrent state updates, production systems do not automatically serialize everything with write locks. Depending on the operation, they may use atomic datastore operations, transactions and pessimistic locks, optimistic concurrency control, or event/log-based designs.

## Key Takeaways

- A cache is usually a derived copy; the database is commonly the source of truth.
- Cache-aside puts cache management in application code.
- Read-through puts cache-miss loading responsibility in the cache layer.
- Write-through synchronously propagates writes through the cache to the database.
- Write-back asynchronously persists cache writes and therefore introduces a durability window.
- Write-around writes directly to the database and populates the cache later on reads.
- TTL controls expiration, while eviction controls removal under capacity pressure.
- Cache invalidation is difficult because reads, writes, replication, and cache operations can race.
- Database replica lag can cause stale values to be repopulated into an otherwise correctly invalidated cache.
- Strong versus eventual consistency is a business requirement, not merely a cache setting.
- Lost updates occur when concurrent read-modify-write operations overwrite one another.
- Pessimistic locking serializes conflicting operations but can become a bottleneck.
- Atomic operations are usually preferable for simple composable operations such as increments.
- Optimistic concurrency detects conflicting writes using versions and retries.
- Distributed locks are powerful but introduce significant coordination and failure complexity.
- Redis primarily keeps its working dataset in RAM and can be distributed across multiple machines.
- Sharding distributes keys; replication creates additional copies.
- Cache stampedes and hot keys are important production failure modes.
- Redis can be a primary datastore for some workloads, but cache and database roles should be chosen based on workload, durability, data model, query needs, and cost.

## Reflection Questions

1. Why is a cache useful even when the database is already fast?
2. What is the difference between TTL, eviction, and invalidation?
3. Why can `UPDATE DB → DELETE CACHE` still result in stale data?
4. How can database replica lag cause stale cache repopulation?
5. When is eventual consistency acceptable?
6. Why is an atomic increment usually better than a write lock for a counter?
7. When would pessimistic locking be preferable to an atomic operation?
8. How does optimistic concurrency detect a lost update?
9. Why can't ordinary in-process mutexes coordinate multiple application servers?
10. Why should distributed locks not automatically be the first solution?

## What's Next

Lesson 56 — Compression

We will study why compression exists, how HTTP compression works, the difference between compressing headers and bodies, common algorithms such as gzip and Brotli, and the latency/CPU/bandwidth trade-offs involved in production systems.
