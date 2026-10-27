# Lesson 132 — Transactions

## Objectives
- Explain why related database changes should be grouped into a transaction.
- Understand ACID and the problem each property addresses.
- Use BEGIN, COMMIT, and ROLLBACK.
- Recognize failure and concurrency risks.
- Distinguish a database transaction from a multi-service workflow.

## Prerequisites
- Lesson 130 — Database Fundamentals
- Lesson 131 — Indexing

## Concept Summary
A transaction is a logical unit of database work with defined commit and rollback semantics. It helps ensure related changes are handled together, while concurrency control and isolation govern interactions between overlapping transactions.

## Core Ideas
- **BEGIN:** Starts an explicit transaction.
- **COMMIT:** Commits the transaction's changes.
- **ROLLBACK:** Aborts the transaction and discards its uncommitted changes.
- **Atomicity:** Transactional changes succeed or fail as a unit.
- **Consistency:** Successful transactions preserve the rules enforced by the database and application.
- **Isolation:** Concurrent transactions are prevented from interfering in ways forbidden by the selected isolation level.
- **Durability:** Committed changes survive failures covered by the database's durability guarantees.
- **Affected-row checks:** Applications must verify that expected rows were updated; transaction boundaries alone do not validate business logic.
- **Ambiguous commit:** A connection failure after sending COMMIT does not prove whether the server committed. Safe retries may require idempotency keys and reconciliation.

## Example: Transfer
```sql
BEGIN;

UPDATE accounts
SET balance = balance - 500
WHERE account_id = 'A'
  AND balance >= 500;

-- Application verifies exactly one row was updated.

UPDATE accounts
SET balance = balance + 500
WHERE account_id = 'B';

-- Application verifies exactly one row was updated.

COMMIT;
```
If either operation fails its business checks, the application must roll back rather than commit a partial transfer. The application should not report success until commit succeeds.

## Internal Mechanisms
- Databases use transaction state, concurrency-control mechanisms, and recovery mechanisms to support transactional behavior.
- PostgreSQL uses MVCC for concurrent access and write-ahead logging (WAL) to support crash recovery and durability.
- A successful commit does not necessarily mean every modified table page has already been flushed to its final location; recovery mechanisms and configuration determine the durability guarantee.

## Concurrency
A conditional update can combine a balance check and modification:
```sql
UPDATE accounts
SET balance = balance - 800
WHERE account_id = 'A'
  AND balance >= 800;
```
Check the affected-row count. For competing updates to the same row, database concurrency control coordinates the writes. More complex read-modify-write workflows may require locks or stronger isolation guarantees.

## Production Perspective
- Keep transactions appropriately short; long transactions can hold locks and retain old row versions.
- Validate expected row counts and handle constraint violations.
- Handle rollback and exceptions correctly in application code.
- Design safe retries for uncertain outcomes; use idempotency and reconciliation where appropriate.
- A database transaction does not automatically include an external payment provider, another independent database, or a message broker. Multi-service workflows may need sagas, compensating actions, and durable event handling.
- ACID does not invent missing business rules; enforce important invariants through constraints and correct application logic.

## Common Misconceptions
- Every SQL statement requires an explicit BEGIN; many clients/databases use implicit transactions.
- ACID guarantees that application business logic is correct.
- ROLLBACK can reverse an already committed transaction or an external side effect.
- A lost COMMIT response means the transaction failed.
- Atomicity alone prevents every concurrency anomaly.
- A database transaction makes a multi-service workflow globally atomic.

## Key Takeaways
- Transactions group related database changes into a logical unit.
- ACID properties address atomicity, rule preservation, concurrency isolation, and durability.
- Check affected rows and constraints; a transaction does not replace business validation.
- A connection failure during commit can leave the client uncertain about the outcome.
- Transaction boundaries end at the database scope unless additional distributed-workflow mechanisms are used.

## Reflection Questions
1. Why is a bank transfer a good example of a transaction? What could go wrong without one?
2. Explain each ACID property with a concrete example. Which properties are easiest to confuse, and why?
3. If an application loses its connection immediately after sending COMMIT, why cannot it safely assume the transaction failed?
4. Two requests concurrently withdraw ₹800 from an account containing ₹1,000. How can a conditional UPDATE help, and why might read-then-write be unsafe?
5. Why does a database transaction not automatically make an order workflow involving a payment provider and inventory service atomic?
6. What can go wrong if a transaction remains open for a long time?

## What's Next
Lesson 133 — Isolation Levels.
