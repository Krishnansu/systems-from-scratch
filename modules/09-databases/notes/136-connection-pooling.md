# Lesson 136 — Database Connection Pooling

## Objectives
- Explain the cost of repeatedly establishing database connections.
- Describe pool checkout, reuse, release, and exhaustion.
- Size pools against database capacity and application replica counts.
- Diagnose slow queries, connection leaks, and pool saturation.
- Distinguish application pools from database proxy pooling modes.

## Prerequisites
- Lesson 130 — Database Fundamentals
- Lesson 132 — Transactions
- Lesson 134 — Replication
- Lesson 135 — Sharding

## Concept Summary
A connection pool manages a bounded set of reusable database connections. Callers borrow a connection, perform database work, and return it rather than establishing and closing a physical connection for every request.

## Core Ideas
- **Connection:** a communication channel and database session. One connection can execute many queries and transactions sequentially.
- **Checkout/release:** borrow an available connection and return it safely, including on exceptions. Returning a pooled connection normally does not close the physical connection.
- **Pool settings:** maximum size, minimum idle connections, acquisition timeout, idle timeout, maximum lifetime, and validation behavior.
- **Pool exhaustion:** all available connections are busy or unavailable. Callers wait, acquire a new connection if permitted, or time out.
- **Connection leak:** code fails to release a borrowed connection, reducing effective pool capacity.
- **Long-held connections:** slow queries, locks, and transactions that wait on external services keep connections occupied.
- **Pool sizing:** consider query duration, useful database concurrency, bursts, replica counts, background workers, and all other clients.
- **Horizontal scaling:** maximum application connections can approach `application_instances × pools_per_instance × pool_max_size`, adjusted for which pools each instance creates and uses.
- **Sharded databases:** each shard may have its own pool; calculate budgets per shard and across the entire deployment.
- **Database poolers:** PgBouncer session pooling retains a server connection for a client session; transaction pooling reuses server connections between transactions but constrains session-dependent behavior.

## Practical Example
Eight application instances with a pool maximum of 20 can potentially open 160 connections. At 30 instances, the potential maximum becomes 600. Autoscaling can therefore exceed the database's connection budget unless pool sizing accounts for peak instance count and other clients.

Use Little's Law, `L = λW`, to estimate average concurrent work: 100 database operations per second occupying a connection for 0.1 seconds imply approximately 10 concurrent operations on average. This is a starting point, not a universal pool-size recommendation.

## Production Perspective
- Budget connections across every application replica, worker, shard, proxy, and operational client.
- Investigate slow queries, lock waits, connection leaks, and time spent holding connections before increasing pool size.
- Keep transactions short; avoid holding a database transaction open while waiting for external HTTP calls when correctness permits.
- Set acquisition timeouts and monitor pool utilization, wait time, timeouts, query latency, and database resource usage.
- A larger pool can increase contention when the database is already saturated.
- Connection poolers reduce connection overhead or multiplex clients; they do not remove query bottlenecks or add database compute capacity.
- Validate compatibility before using transaction pooling with session state, temporary tables, advisory locks, or prepared statements.

## Common Misconceptions
- Every HTTP request needs its own physical database connection.
- Closing a borrowed pooled connection is equivalent to returning it to the pool.
- Increasing pool size always increases throughput.
- A long-lived idle connection is necessarily a leak.
- A per-instance pool limit is a global database connection limit.
- Connection pooling replaces indexing, query optimization, or capacity planning.

## Key Takeaways
- Pools reuse connections and bound application concurrency.
- Connections must be released reliably, including after exceptions.
- Pool exhaustion is a symptom to investigate, not proof that the configured pool is too small.
- Plan for the maximum number of application instances and connections per shard.
- Pool size should match workload characteristics and effective database capacity.

## Reflection Questions
1. Why is opening a database connection for every request inefficient?
2. Fifteen instances each have a pool maximum of 12. What is their maximum potential connection count, and why could it overwhelm a database?
3. Why might a larger pool worsen performance when database CPU is saturated?
4. What problems can occur when a transaction remains open while an external API call takes five seconds?
5. How does PgBouncer transaction pooling differ from session pooling, and what compatibility issues can result?
6. An application uses four shards with a pool maximum of eight connections per shard per instance. How does the potential connection count change when instances scale from five to twenty?

## Related Lessons
- Lesson 131 — Indexing
- Lesson 132 — Transactions
- Lesson 134 — Replication
- Lesson 135 — Sharding

## What's Next
Lesson 137 — Redis.
