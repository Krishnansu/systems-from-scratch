# Lesson 130 — Database Fundamentals: Commands

These examples use PostgreSQL-compatible SQL. Run them only in a disposable local database or an approved development environment.

## Create a small schema

```sql
CREATE TABLE customers (
    customer_id BIGINT PRIMARY KEY,
    name TEXT NOT NULL,
    email TEXT UNIQUE
);

CREATE TABLE orders (
    order_id BIGINT PRIMARY KEY,
    customer_id BIGINT NOT NULL REFERENCES customers(customer_id),
    total NUMERIC(12, 2) NOT NULL CHECK (total >= 0),
    status TEXT NOT NULL
);
```

## Insert sample rows

```sql
INSERT INTO customers (customer_id, name, email)
VALUES (7, 'Asha', 'asha@example.com');

INSERT INTO orders (order_id, customer_id, total, status)
VALUES (101, 7, 1499.00, 'PAID');
```

## Query and join

```sql
SELECT order_id, total, status
FROM orders
WHERE order_id = 101;

SELECT o.order_id, c.name AS customer_name, o.total, o.status
FROM orders AS o
JOIN customers AS c ON c.customer_id = o.customer_id
WHERE o.order_id = 101;
```

## Observe constraint enforcement

```sql
-- Expected to fail if customer 999 does not exist:
INSERT INTO orders (order_id, customer_id, total, status)
VALUES (104, 999, 500, 'PENDING');

-- Expected to fail because the total violates CHECK (total >= 0):
INSERT INTO orders (order_id, customer_id, total, status)
VALUES (105, 7, -10, 'PENDING');
```

The failures demonstrate foreign-key and check constraints. Do not disable constraints merely to make the examples succeed.

## Optional psql client commands

```text
\l                 list databases
\c <database>      connect to a database
\dt                list tables in the current schema search path
\d orders          describe the orders table
\q                 exit psql
```

These backslash commands belong to the `psql` client, not to standard SQL.

## Safety and cleanup

- Use a disposable database; the examples create tables and insert records.
- If you want to rerun the examples, reset only your disposable lab database or remove the lab tables after confirming they contain no data you need.
- Do not execute schema changes or cleanup commands against production data without an approved change process.
- Never put real credentials or sensitive customer data in examples or source control.
