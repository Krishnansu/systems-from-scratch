# Lesson 131 — Indexing

## Objectives
- Explain how indexes help databases locate rows.
- Understand B-tree indexes, selectivity, and composite-index order.
- Balance read performance against storage and write overhead.
- Use query plans to evaluate index choices.

## Concept Summary
An index is a separately maintained data structure that helps the DBMS find rows without scanning the entire table. B-tree indexes commonly support equality and range lookups. Indexes consume storage and require maintenance during writes, so they should be designed around real query patterns and verified with execution plans.

## Core Ideas
- **Sequential scan:** Examines table rows/pages to find matches. It can be efficient when much of the table is needed.
- **Index scan:** Navigates an index to find matching entries, then may fetch table rows.
- **B-tree:** A balanced search-tree family commonly used for equality and range searches; PostgreSQL uses B-tree by default.
- **Selectivity:** How much data a predicate matches. A query returning a large fraction of rows may favor a sequential scan.
- **Composite index:** An index on multiple columns, such as `(customer_id, created_at)`. For B-tree indexes, leading-column order strongly affects which predicates can use it efficiently.
- **Index-only access:** Some queries may be answered from index data alone, depending on the engine and query; it is not guaranteed.
- **Planner:** Chooses a plan using query shape, statistics, estimates, costs, and available access paths.

## Example
```sql
CREATE INDEX idx_orders_customer_created
ON orders (customer_id, created_at);
```

This can suit:
```sql
SELECT order_id, created_at, total
FROM orders
WHERE customer_id = 42
  AND created_at >= TIMESTAMP '2026-01-01';
```
The leading `customer_id` column supports customer filtering, and `created_at` can narrow the range. A query filtering only by `created_at` may benefit less because the leading column is unconstrained.

## Query-Plan Inspection
```sql
EXPLAIN
SELECT *
FROM orders
WHERE customer_id = 42;
```
`EXPLAIN` shows the planned execution. `EXPLAIN ANALYZE` executes the statement and reports observed behavior, so use it carefully, especially for state-changing queries or production workloads. In PostgreSQL, `ANALYZE orders;` updates planner statistics and is distinct from `EXPLAIN ANALYZE`.

## Production Perspective
- Indexes can reduce work for selective reads, range searches, joins, and ordering.
- Indexes consume storage/cache and add work to inserts, deletes, and updates of indexed columns.
- An index does not force the optimizer to use it; a sequential scan can be cheaper.
- Stale statistics can contribute to poor estimates and plans.
- Evaluate query frequency, selectivity, data distribution, read/write mix, and actual plans.
- Composite-index order should reflect real query patterns. The leftmost-prefix heuristic is useful for B-tree indexes, but inspect actual plans.
- Do not assume every `WHERE` column needs an index or that an index eliminates all table I/O.

## Common Mistakes
- Adding indexes without checking workload or query plans.
- Expecting an index to help when a query returns most of the table.
- Ignoring write overhead and storage.
- Assuming `(a, b)` and `(b, a)` are interchangeable.
- Treating any index scan as proof that a query is efficient.
- Confusing `ANALYZE table_name` with `EXPLAIN ANALYZE`.

## Key Takeaways
- Indexes are maintained structures that can improve row lookup.
- B-tree indexes commonly support equality and range predicates.
- Composite-index column order matters.
- Indexing trades read performance against write cost and storage.
- Use plans and measurements rather than assumptions.

## Reflection Questions
1. Why can an index speed up a lookup, and what work may remain?
2. Why might a database choose a sequential scan despite a relevant index?
3. Why might `(customer_id, created_at)` suit a customer-and-date query?
4. What costs do indexes add to a write-heavy table?
5. How do `EXPLAIN` and `EXPLAIN ANALYZE` differ?
6. A query uses an index but is slow. What would you inspect before adding another index?

## What's Next
Lesson 132 — Transactions.
