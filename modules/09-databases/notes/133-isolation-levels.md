# Lesson 133 — Isolation Levels

## Objectives
- Explain why transactions need isolation guarantees.
- Distinguish common concurrency anomalies.
- Compare standard isolation levels and PostgreSQL behavior.
- Recognize when constraints, atomic updates, locks, or Serializable isolation are useful.

## Prerequisites
- Lesson 130 — Database Fundamentals
- Lesson 131 — Indexing
- Lesson 132 — Transactions

## Concept Summary
Isolation levels define which effects of concurrent transactions may be observed and which anomalies the database prevents. Actual guarantees depend on the database implementation.

## Core Ideas
- **Read Uncommitted:** The SQL standard permits dirty reads; PostgreSQL treats this level as Read Committed.
- **Read Committed:** PostgreSQL gives each statement a fresh snapshot of committed data.
- **Repeatable Read:** PostgreSQL maintains a stable transaction snapshot and prevents ordinary non-repeatable and phantom reads, but write skew can still occur.
- **Serializable:** Transactions must produce an outcome equivalent to some serial execution. PostgreSQL may abort a transaction to preserve this guarantee.

## Common Anomalies
- **Dirty read:** Observe another transaction's uncommitted change.
- **Non-repeatable read:** Re-read a row and observe a changed committed value.
- **Phantom read:** Re-run a predicate query and observe a changed set of matching rows.
- **Lost update:** One transaction overwrites another transaction's change.
- **Write skew:** Concurrent transactions update different rows based on a shared snapshot and jointly violate an invariant.

## Practical Examples
A conditional update can combine a check and modification:
```sql
UPDATE accounts
SET balance = balance - 800
WHERE account_id = 'A'
  AND balance >= 800;
```
Check the affected-row count. For multi-row or cross-row invariants, consider constraints, explicit locks, or Serializable isolation as appropriate.

Set a transaction's isolation level in PostgreSQL:
```sql
BEGIN TRANSACTION ISOLATION LEVEL SERIALIZABLE;
-- Perform the complete logical operation.
COMMIT;
```
Applications must handle serialization failures by safely retrying the whole logical transaction.

## Production Perspective
- Choose isolation based on the business invariant, not simply by selecting the strongest level everywhere.
- Read Committed is sufficient for many CRUD operations, but separate statements can observe different committed states.
- Repeatable Read provides a stable snapshot but does not prevent every serialization anomaly.
- Serializable can prevent anomalies but may abort transactions and require retries.
- Constraints, conditional updates, and locks can protect specific invariants without requiring Serializable for every operation.

## Common Misconceptions
- A transaction automatically prevents all concurrency bugs.
- Repeatable Read freezes the database for every transaction.
- Serializable requires all transactions to execute physically one at a time.
- Serializable transactions cannot fail.
- PostgreSQL Read Uncommitted permits dirty reads.
- Atomic updates solve every multi-row concurrency problem.

## Key Takeaways
- Isolation governs interactions between concurrent transactions; atomicity is a separate property.
- Anomalies describe different failure modes and require different reasoning.
- PostgreSQL Repeatable Read provides snapshot isolation but can permit write skew.
- Serializable may abort transactions; retry the complete logical transaction safely.
- Protect business invariants with the appropriate combination of isolation, constraints, atomic operations, and locking.

## Reflection Questions
1. Two transactions read a row; one updates and commits it, and the other sees a different value on its second read. What anomaly is this, and which PostgreSQL isolation level permits it?
2. Explain the difference between non-repeatable reads and phantom reads.
3. Why can PostgreSQL Repeatable Read prevent ordinary phantom reads but still permit write skew?
4. How could Serializable help when two doctors independently decide to go off call based on the same snapshot?
5. Why should an application retry the whole transaction after a serialization failure?
6. When might a conditional UPDATE or database constraint be preferable to Serializable isolation?

## What's Next
Lesson 134 — Replication.
