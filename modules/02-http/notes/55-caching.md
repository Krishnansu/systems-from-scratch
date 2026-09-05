# Lesson 55 — Caching

## Objectives

- Understand why caching exists and what problem it solves.
- Understand cache hits, misses, TTL, expiration, and eviction.
- Understand cache hierarchy from browser/CDN to application caches.
- Understand cache-aside and basic read/write caching patterns.
- Understand cache invalidation, stale data, cache stampedes, and hot keys.
- Understand the architectural difference between a cache such as Redis and a database.

## Prerequisites

- HTTP caching fundamentals
- HTTP request/response lifecycle
- Sessions and JWT
- Basic understanding of databases

## Theory

Caching stores a copy of data so repeated requests can be served faster and the underlying source of truth receives less work.

The fundamental flow is:

```text
Request
   |
   v
 Cache?
  /   \
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

### TTL and expiration

TTL (Time To Live) limits how long an entry remains valid. A long TTL improves hit rate but permits data to remain stale for longer. A short TTL improves freshness but causes more misses.

TTL is different from eviction: TTL answers when an entry expires, while eviction answers which entry should be removed when cache capacity is constrained.

### Eviction

Common eviction approaches include:

- LRU — Least Recently Used
- LFU — Least Frequently Used
- FIFO — First In, First Out
- MRU — Most Recently Used
- Random eviction

Real systems may use more sophisticated combinations of recency, frequency, and aging.

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

### Invalidation

When source data changes, cached copies may become stale. Common approaches include:

- Explicit deletion/update of cache entries
- TTL-based expiration
- Versioned keys
- Event-driven invalidation

Cache invalidation is difficult because updates and reads can race across distributed components.

### Distributed caching

A distributed cache spreads cached data across multiple machines. Sharding determines where a key is stored; replication keeps additional copies for availability.

```text
Redis Cluster
   |
   +---- Node A ---- RAM
   |
   +---- Node B ---- RAM
   |
   +---- Node C ---- RAM
```

Redis is primarily an in-memory data store, so its working dataset resides in the RAM of Redis server machines. Redis can also persist data, but its architecture is optimized around memory-speed access.

A cache does not have to contain the entire database. It is often a smaller hot subset of a much larger persistent dataset.

### Cache stampede and hot keys

A cache stampede occurs when many requests simultaneously miss the same popular key, causing all of them to hit the origin/database.

Common mitigations include request coalescing/single-flight, locking, jittered expiration, and stale-while-revalidate techniques.

A hot key is a single disproportionately popular key that can overload one cache node even when the overall cache cluster has sufficient capacity.

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

## Deep Dive

### Cache vs Database

A cache and a database both store and retrieve data, but their responsibilities differ.

A database is normally the authoritative, durable source of state. It is designed around persistent storage, indexing/querying, consistency, recovery, and large datasets.

Redis is an in-memory data store commonly used as a cache. Its working dataset resides in RAM, providing very low latency. Redis can also be used as a primary datastore for appropriate workloads, but it should not be assumed to be a universal replacement for databases.

The key distinction is not simply RAM versus disk. Modern databases also use RAM heavily, and Redis supports persistence. The deeper distinction is the system's data model, durability expectations, query model, scaling characteristics, workload, and cost.

### Redis and distributed memory

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

### Failure model

If a cache node fails and the cache contains only derived data, the application can often recover by reading the source of truth and repopulating the cache. Replication can reduce availability impact and recovery time.

This is one of the fundamental reasons a cache can tolerate weaker durability guarantees than the source-of-truth database.

## Hands-on Exercise

1. Pick a frequently requested API response such as a product or user profile.
2. Design a cache key for it.
3. Decide an appropriate TTL based on how stale the data may safely become.
4. Describe what happens on a cache hit and cache miss.
5. Decide how the cache is invalidated when the underlying record changes.
6. Identify what happens if the cache disappears completely.
7. Identify a possible hot key and cache stampede scenario.

## Common Misconceptions

- A cache is not necessarily Redis; browser caches and CDNs are also caches.
- Redis is not merely a temporary key-value map; it is a powerful in-memory data store that can also persist data.
- "Database uses disk and Redis uses RAM" is useful intuition, but not a strict physical distinction. Databases use RAM extensively, and Redis supports persistence.
- TTL and eviction are not the same thing.
- A cache hit does not mean the data is guaranteed to be perfectly fresh.
- Distributed caching does not mean one giant shared RAM module; it means multiple machines collectively provide the cache.
- A cache does not automatically make a database unnecessary.

## Summary

Caching keeps frequently needed data closer to the consumer and avoids repeated expensive work. Caches can exist at many layers, from browsers and CDNs to application-local and distributed caches such as Redis. Cache-aside is a common pattern, while TTL, eviction, and invalidation determine how cached data behaves over time. Distributed caches introduce sharding, replication, hot keys, and stampede concerns.

## Key Takeaways

- A cache is a fast copy of data, not usually the source of truth.
- Cache hits reduce latency and backend load.
- TTL controls expiration; eviction controls removal under capacity pressure.
- Cache invalidation is difficult because distributed copies can become stale.
- Redis primarily keeps its working dataset in RAM and can be distributed across multiple machines.
- Sharding distributes keys; replication creates additional copies.
- Cache stampedes and hot keys are important production failure modes.
- Redis can be a primary datastore for some workloads, but cache and database roles should be chosen based on workload, durability, data model, query needs, and cost.

## Reflection Questions

1. Why is a cache useful even when the database is already fast?
2. What is the difference between TTL, eviction, and invalidation?
3. If a Redis node fails, why can a cache-backed application often recover without losing authoritative data?

## What's Next

Lesson 56 — Compression

We will study why compression exists, how HTTP compression works, the difference between compressing headers and bodies, common algorithms such as gzip and Brotli, and the latency/CPU/bandwidth trade-offs involved in production systems.
