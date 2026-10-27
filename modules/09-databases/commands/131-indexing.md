# Lesson 131 — Indexing: Commands

Use a disposable PostgreSQL database or approved development environment. These examples create objects and data.

## Create sample data
```sql
CREATE TABLE orders_lab (
    order_id BIGINT PRIMARY KEY,
    customer_id BIGINT NOT NULL,
    status TEXT NOT NULL,
    created_at TIMESTAMP NOT NULL
);

INSERT INTO orders_lab
SELECT n, n % 1000,
       CASE WHEN n % 3 = 0 THEN 'PAID' ELSE 'PENDING' END,
       TIMESTAMP '2026-01-01' + n * INTERVAL '1 second'
FROM generate_series(1, 100000) AS n;
```

## Compare query plans
```sql
EXPLAIN
SELECT * FROM orders_lab WHERE customer_id = 42;

CREATE INDEX idx_orders_lab_customer
ON orders_lab (customer_id);

ANALYZE orders_lab;

EXPLAIN
SELECT * FROM orders_lab WHERE customer_id = 42;
```
`ANALYZE orders_lab` updates planner statistics; it is different from `EXPLAIN ANALYZE`.

## Composite index
```sql
CREATE INDEX idx_orders_lab_customer_created
ON orders_lab (customer_id, created_at);

EXPLAIN
SELECT * FROM orders_lab
WHERE customer_id = 42
  AND created_at >= TIMESTAMP '2026-01-02';

EXPLAIN
SELECT * FROM orders_lab
WHERE created_at >= TIMESTAMP '2026-01-02';
```
Compare the plans: the first query constrains the leading column, while the second does not.

## Measure execution carefully
```sql
EXPLAIN ANALYZE
SELECT * FROM orders_lab WHERE customer_id = 42;
```
`EXPLAIN ANALYZE` executes the query. Start with read-only queries in development. For modifying statements, execution can cause changes and consume production resources.

## Inspect indexes
```sql
-- psql client command, not standard SQL:
\d orders_lab

SELECT indexname, indexdef
FROM pg_indexes
WHERE tablename = 'orders_lab';
```

## Safety
- Confirm the database/environment before DDL or inserts.
- Index creation on large tables can consume significant I/O, storage, and time.
- Do not run experiments against production without approval.
- Remove lab objects only after confirming they contain no needed data.
