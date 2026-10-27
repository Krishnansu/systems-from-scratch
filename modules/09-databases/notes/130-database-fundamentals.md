# Lesson 130 — Database Fundamentals

## Objectives

- Explain why applications need databases instead of relying only on process memory or files.
- Distinguish a database, DBMS, database server, and client.
- Understand tables, rows, columns, schemas, keys, and constraints.
- Compare relational and NoSQL database models at a high level.
- Trace a query from application code through the DBMS and back.
- Explain persistence, durability, and the basic role of transactions.

## Prerequisites

- Backend services, HTTP, processes, files, APIs, Docker, and Kubernetes fundamentals.

## Concept Summary

A database provides a shared system for storing and querying data beyond an application's process lifetime. A database management system (DBMS) manages data, query execution, constraints, concurrency, and recovery. Relational databases organize data into tables and use keys and constraints to represent relationships and protect integrity. Databases use memory and persistent storage; transactions coordinate related changes.

## Core Ideas

- **Database:** An organized collection of data managed by database software.
- **DBMS:** Software that manages databases, queries, concurrency, integrity, and recovery; examples include PostgreSQL and MySQL.
- **Database server:** A running database service that accepts client requests; it does not necessarily require a dedicated physical machine.
- **Relational model:** Data represented through relations, commonly tables with rows and columns.
- **Primary key:** Uniquely identifies a row.
- **Foreign key:** Enforces a reference to a valid key in another table or, where allowed, the same table.
- **Constraint:** A rule such as `NOT NULL`, `UNIQUE`, `CHECK`, or a foreign key that data must satisfy.
- **SQL:** A language used to define, query, and modify relational data.
- **NoSQL:** A broad category that includes document, key-value, wide-column, graph, and other data models. Capabilities vary by product.
- **Persistence:** Data is stored beyond the lifetime of an application process.
- **Durability:** A committed transaction survives failures covered by the database's durability guarantees.
- **Transaction:** A unit of database work with defined commit/rollback semantics. It does not automatically make a multi-service workflow atomic.

## Example Schema

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

A customer can have multiple orders. The foreign key prevents an order from referencing a nonexistent customer, provided the constraint is enforced. A join can retrieve related customer and order data without duplicating the customer's attributes in every order row.

## Query Lifecycle

```text
Application
  → database driver and protocol
  → database connection
  → SQL parsing and validation
  → query planning and execution
  → memory cache and/or persistent storage
  → result rows returned through the driver
  → application response
```

The DBMS chooses an execution plan based on the query, available indexes, statistics, and other factors. Data may be served from memory or read from storage. The application translates returned rows into its API response.

## Reliability and Production Perspective

- Shared database state lets multiple application replicas access the same data without relying on independent process memory.
- Databases use persistence and recovery mechanisms; exact durability guarantees depend on database configuration, storage, and replication.
- Constraints protect integrity across multiple code paths; application validation alone may not be sufficient.
- Concurrency control governs overlapping operations. Transactions can make related database changes atomic within their defined boundary.
- Slow queries, lock contention, connection exhaustion, network problems, storage pressure, and replication lag have different causes and require different diagnosis.
- A database transaction does not automatically make a workflow spanning payment providers or multiple services atomic.
- NoSQL does not inherently mean schema-free, transaction-free, or more scalable; evaluate the actual data model and workload.

## Common Misconceptions

- A database is more than an ordinary file, even if files are used underneath.
- A database does not have to run on a separate physical machine.
- NoSQL products differ substantially in data models and guarantees.
- A successful SQL statement does not prove an entire business workflow is atomic.
- Durability guarantees are bounded by configuration and the failures the system is designed to withstand.
- Not every slow query needs an index; investigate plans, locks, resources, and latency.

## Key Takeaways

- A DBMS provides shared data management, querying, integrity, concurrency, and recovery.
- Primary and foreign keys express identity and relationships.
- Query execution involves the driver, protocol, DBMS, memory/storage, and result handling.
- Persistence, durability, integrity, and concurrency are distinct concerns.
- Database design and operation must be considered as part of the complete application architecture.

## Reflection Questions

1. Why can process-local order data fail when an application is scaled to multiple replicas?
2. What is the difference between a database and a DBMS?
3. How does a foreign key protect data integrity?
4. What happens between an application sending SQL and receiving rows?
5. How are persistence and durability different?
6. Why does a database transaction not automatically make a multi-service workflow atomic?

## What's Next

Lesson 131 — Indexing.
