# Lesson 133 — Isolation Levels: Commands

Use a disposable PostgreSQL database. These examples create and modify data.

## Inspect the configured isolation level
```sql
SHOW transaction_isolation;
```

## Setup
```sql
DROP TABLE IF EXISTS isolation_lab;
CREATE TABLE isolation_lab (
    id INT PRIMARY KEY,
    balance INT NOT NULL
);
INSERT INTO isolation_lab VALUES (1, 1000);
```

## Read Committed: two-session experiment
Session A:
```sql
BEGIN ISOLATION LEVEL READ COMMITTED;
SELECT balance FROM isolation_lab WHERE id = 1;
```
Session B:
```sql
BEGIN;
UPDATE isolation_lab SET balance = 700 WHERE id = 1;
COMMIT;
```
Session A runs the SELECT again. It should see 700, then can COMMIT.

## Repeatable Read: two-session experiment
Reset the value to 1000 and commit the reset. Session A:
```sql
BEGIN ISOLATION LEVEL REPEATABLE READ;
SELECT balance FROM isolation_lab WHERE id = 1;
```
Session B updates the balance to 700 and commits. Session A repeats the SELECT and should still see its original snapshot value, 1000. A conflicting update from Session A may produce a serialization error; if so, ROLLBACK.

## Serializable
```sql
BEGIN ISOLATION LEVEL SERIALIZABLE;
-- Run the complete logical operation and its invariant checks.
COMMIT;
```
Serializable transactions can fail with a serialization error. Application code must retry the whole logical transaction safely.

## Safety and cleanup
- Confirm the database and environment before running DDL or modifying data.
- Run concurrent experiments in separate sessions connected to the same database.
- Roll back open transactions after errors.
- Cleanup only after confirming the table contains no needed data:
```sql
DROP TABLE isolation_lab;
```
