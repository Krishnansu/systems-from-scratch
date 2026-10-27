# Lesson 132 — Transactions: Commands

Use a disposable PostgreSQL database or an approved development environment. These examples create and modify data.

## Setup
```sql
CREATE TABLE accounts_lab (
    account_id TEXT PRIMARY KEY,
    balance NUMERIC(12, 2) NOT NULL CHECK (balance >= 0)
);

INSERT INTO accounts_lab VALUES ('A', 2000), ('B', 1000);
```

## Commit a transfer
```sql
BEGIN;
UPDATE accounts_lab SET balance = balance - 500 WHERE account_id = 'A';
UPDATE accounts_lab SET balance = balance + 500 WHERE account_id = 'B';
SELECT * FROM accounts_lab ORDER BY account_id;
COMMIT;
SELECT * FROM accounts_lab ORDER BY account_id;
```
In application code, verify that each expected update affected exactly one row before committing.

## Roll back a transfer
```sql
BEGIN;
UPDATE accounts_lab SET balance = balance - 200 WHERE account_id = 'A';
SELECT * FROM accounts_lab ORDER BY account_id;
ROLLBACK;
SELECT * FROM accounts_lab ORDER BY account_id;
```
Compare the state inside the transaction with the state after rollback.

## Constraint violation
```sql
BEGIN;
UPDATE accounts_lab SET balance = balance - 5000 WHERE account_id = 'A';
-- PostgreSQL should reject the update because the balance would be negative.
ROLLBACK;
SELECT * FROM accounts_lab ORDER BY account_id;
```
After a statement error, PostgreSQL leaves the transaction aborted until rollback or recovery to a savepoint.

## Conditional withdrawal
```sql
UPDATE accounts_lab
SET balance = balance - 800
WHERE account_id = 'A'
  AND balance >= 800;
```
Check the affected-row count: one means the update matched; zero means the account was missing or the balance condition was not satisfied. For an actual multi-step workflow, use an explicit transaction as needed.

## Safety and cleanup
- Confirm the target database before running DDL or modifying data.
- Do not run experiments against production without approval.
- Cleanup only after confirming the table contains no needed data:
```sql
DROP TABLE accounts_lab;
```
