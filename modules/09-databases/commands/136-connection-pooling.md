# Lesson 136 — Connection Pooling: Practice Reference

Use a disposable local database or an approved development environment. The SQL below is read-only.

## Count database sessions

```sql
SELECT count(*) AS total_connections
FROM pg_stat_activity;
```

This includes sessions from different applications and clients, not only one application's pool. Visibility may depend on database permissions.

## Group sessions by state

```sql
SELECT
    state,
    count(*) AS connection_count
FROM pg_stat_activity
GROUP BY state
ORDER BY connection_count DESC;
```

Interpret states in context. An idle connection may be intentionally retained by a pool. An `idle in transaction` session can indicate a transaction left open while application code waits or performs other work.

## Inspect client sessions

```sql
SELECT
    pid,
    usename,
    application_name,
    state,
    now() - backend_start AS connection_age,
    now() - query_start AS query_age
FROM pg_stat_activity
WHERE backend_type = 'client backend'
ORDER BY query_start NULLS LAST;
```

`query_age` is based on `query_start`. For idle sessions, it may represent time since the last query rather than a currently executing query. Do not infer a leak from connection age alone.

## Pool sizing arithmetic

Potential application connections can be estimated as:

`maximum_instances × pools_per_instance × pool_max_size`

For example, 12 instances × 3 shard pools × 10 connections gives a potential maximum of 360 application connections across the shard fleet, if every pool can reach its configured maximum.

Budget separately for each database server. Include workers, migrations, monitoring, administration, other applications, and proxy behavior. A proxy may change the relationship between client connections and backend database connections.

## Investigation checklist

1. Check pool utilization, acquisition wait time, and acquisition timeouts.
2. Identify long-running queries, lock waits, and idle-in-transaction sessions.
3. Verify that borrowed connections are released on both success and error paths.
4. Look for external calls or long computations performed while holding a connection or transaction.
5. Compare aggregate pool limits at maximum autoscaling capacity with database connection budgets.
6. Check CPU, memory, I/O, and query plans before increasing pool size.
7. For sharded systems, inspect each shard independently for uneven load.

## Safety

- These SQL statements inspect PostgreSQL activity and do not intentionally modify data.
- Permissions may limit visibility into other sessions.
- Do not terminate production sessions or change pool/database limits without an approved operational plan.
- Never put database credentials or sensitive query results into source control.
