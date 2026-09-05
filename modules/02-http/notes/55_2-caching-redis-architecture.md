# Lesson 55 — Redis Architecture Deep Dive

## Redis as a Distributed Cache

Redis is a process running on a physical or virtual machine. Its working dataset primarily resides in RAM.

A distributed Redis deployment consists of multiple Redis processes across machines:

```text
                Redis Cluster
                     |
          +----------+----------+
          |          |          |
          v          v          v
       Node A     Node B     Node C
        RAM        RAM        RAM
```

Each node has its own CPU, process, RAM, and persistent storage. A Redis cluster is therefore not one giant shared RAM pool.

## Sharding

Sharding distributes keys across Redis nodes.

Conceptually:

```text
user:1  ──> Node A
user:2  ──> Node B
user:3  ──> Node C
```

Redis Cluster uses 16,384 hash slots:

```text
        key
         |
         v
       hash
         |
         v
    hash slot
         |
         v
       Node
```

The important distinction is:

> A key maps to a hash slot, and the cluster maps that slot to a node.

This indirection makes rebalancing easier. Adding a node does not require recomputing the placement of every key from scratch; slots can be moved between nodes.

### Sharding vs Replication

These solve different problems:

```text
Sharding      -> Where is the data?
Replication   -> How many copies exist?
```

Sharding primarily improves capacity and distributes workload. Replication primarily improves availability and fault tolerance and can also support read scaling.

## Redis Replication

A primary can replicate its data to one or more replicas:

```text
          Primary
             |
       replication
        /         \\
       v           v
   Replica A   Replica B
```

If the primary fails, a replica may be promoted.

With asynchronous replication, there can be replication lag:

```text
Primary  = new value
Replica  = old value
```

If the primary fails before the latest write reaches the replica, the promoted replica may not contain the newest state.

Therefore replication improves availability but does not automatically provide strong consistency.

## Hot Keys

A hot key is a disproportionately popular key that receives far more traffic than other keys.

For example:

```text
product:iphone17
```

might receive hundreds of thousands of reads per second.

Normal Redis Cluster routing sends that key to one hash slot and therefore one primary:

```text
product:iphone17
        |
        v
    hash slot
        |
        v
      Node B
```

Even if Nodes A, C, and D are mostly idle, Node B can become overloaded.

This demonstrates an important principle:

> Balanced data distribution does not necessarily mean balanced traffic distribution.

## Hot-Key Mitigation: Replicating the Key

Hot-key mitigation can deliberately place multiple copies of the same logical data on different Redis nodes.

This is different from normal Redis primary-replica replication.

Normal node replication looks like:

```text
Primary A
    |
    v
Replica A
```

Hot-key replication can instead look conceptually like:

```text
             product:iphone17
                    |
          +---------+---------+
          |         |         |
          v         v         v
       Node A     Node B     Node C
        copy       copy       copy
```

The application can distribute reads across these copies.

The physical keys may be represented explicitly, for example:

```text
product:iphone17:replica:1
product:iphone17:replica:2
product:iphone17:replica:3
```

All represent the same logical product.

This is often useful for extremely hot, mostly-read data.

However, multiple copies introduce a consistency problem. If the value changes, the system must update or invalidate all relevant copies:

```text
Node A -> old value
Node B -> new value
Node C -> old value
```

Therefore hot-key replication trades some consistency complexity for higher read scalability.

## Cache Stampede

A cache stampede occurs when many requests simultaneously miss the same popular key and all access the origin or database.

Example:

```text
Cache:
product:123 -> value
TTL = 60 seconds
```

When the key expires:

```text
          100,000 requests
                  |
                  v
            product:123
                  |
                  v
             Cache MISS
                  |
        +---------+---------+
        |         |         |
        v         v         v
       DB        DB        DB
```

Instead of Redis protecting the database, expiration causes a sudden burst of database traffic.

A stampede can create cascading failure:

```text
Cache expires
     |
     v
Many cache misses
     |
     v
Database load spikes
     |
     v
Database becomes slow
     |
     v
Requests take longer
     |
     v
More requests pile up
```

Cache stampede is also commonly called the thundering-herd problem.

## Preventing Cache Stampedes

### Request Coalescing / Single-Flight

The application identifies requests for the same resource using the cache key.

Example:

```text
GET /products/123 -> product:123
GET /products/123 -> product:123
GET /products/456 -> product:456
GET /products/123 -> product:123
```

Only requests for the same key are coalesced.

The application can maintain an in-flight operation per key:

```text
inFlight = {
    "product:123": existing DB request
}
```

If the first request sees a cache miss and no existing operation, it becomes responsible for loading the data:

```text
Request A
   |
   v
Cache MISS
   |
   v
No in-flight operation
   |
   v
Start DB request
```

Other requests for the same key arriving while the operation is running join the existing operation:

```text
Request A ───────────────┐
                        |
Request B ──> wait ─────┤
                        |
Request C ──> wait ─────┼──> ONE DB fetch
                        |
Request D ──> wait ─────┘
```

When the DB request completes, the result can populate the cache and be returned to all waiting callers.

Requests for different keys remain independent:

```text
product:123 -> one in-flight operation
product:456 -> separate in-flight operation
```

Therefore request coalescing is not random blocking. It is keyed coordination:

> Identify requests asking for the same resource, elect one request to perform the expensive work, and allow the others to share its result.

### Race During Coalescing

The check-and-create operation must itself be coordinated.

Otherwise two requests arriving simultaneously could both observe:

```text
inFlight["product:123"] = absent
```

and both start DB requests.

Conceptually:

```text
Acquire per-key coordination
          |
          v
Check inFlight
      /       \\
   absent     exists
      |          |
      v          v
create fetch   join fetch
      |          |
      +----+-----+
           |
           v
release coordination
```

### Distributed Application Consideration

A process-local in-flight map only coordinates requests handled by the same application instance:

```text
App A -> local inFlight map
App B -> different local inFlight map
App C -> different local inFlight map
```

Therefore requests routed to different application instances can still independently hit the database.

Cross-instance coordination requires a shared mechanism, such as distributed locking or another coordination design.

Distributed coordination introduces its own failure modes, so it should not automatically be preferred when simpler mechanisms are sufficient.

### TTL Jitter

If many keys are created at roughly the same time, identical TTLs can cause synchronized expiration.

Instead of:

```text
TTL = 60 seconds for every key
```

use a randomized TTL such as:

```text
60 + random(0, 10) seconds
```

This spreads expirations over time and reduces synchronized load spikes.

TTL jitter helps with synchronized expiration but does not completely solve a single extremely hot key.

### Refresh Before Expiration

Popular data can be refreshed before its TTL expires:

```text
TTL remaining < threshold
          |
          v
Background refresh
          |
          v
       Database
          |
          v
         Redis
```

This reduces the chance that users encounter a cache miss for popular data.

### Stale-While-Revalidate

If slight staleness is acceptable, the system can temporarily serve a stale cached value while refreshing it in the background.

```text
Request
   |
   v
Stale cached value
   |
   +----> return immediately
   |
   +----> background refresh
                |
                v
               DB
                |
                v
              Redis
```

This trades some freshness for lower latency and reduced origin load.

### Locking Around Cache Population

A lock can ensure that only one request rebuilds a missing cache entry:

```text
Cache MISS
    |
    v
Acquire lock
    |
    v
Read DB
    |
    v
Populate cache
    |
    v
Release lock
```

Other requests wait or retry rather than independently querying the database.

Locks must be designed carefully in distributed systems because of crashes, expiration, ownership, retries, and network failures.

## Hot Key vs Cache Stampede

These are related but distinct problems.

### Hot Key

```text
One popular key
      |
      v
Huge read traffic
      |
      v
One Redis node overloaded
```

### Cache Stampede

```text
Popular key expires
      |
      v
Many simultaneous cache misses
      |
      v
Origin / database overloaded
```

They can occur together:

```text
Extremely hot key
       |
       v
Key expires
       |
       v
Massive cache miss
       |
       v
Many requests hit DB
```

## Key Takeaways

- Redis Cluster distributes keys using hash slots.
- Sharding provides capacity and distributes data; replication provides redundancy and availability.
- A hot key can overload one node even when the cluster has spare capacity elsewhere.
- Hot-key mitigation can place multiple copies of the same logical data on different nodes, but this adds consistency complexity.
- Cache stampede occurs when many requests miss the same popular key simultaneously and overwhelm the origin.
- Request coalescing groups requests by cache key rather than blocking unrelated requests.
- Request coalescing is essentially keyed coordination around in-flight work.
- Process-local coalescing does not automatically coordinate requests across multiple application instances.
- TTL jitter, proactive refresh, stale-while-revalidate, and locking are additional stampede mitigation techniques.
- Caching requires reasoning about both traffic distribution and failure/expiration behavior.
