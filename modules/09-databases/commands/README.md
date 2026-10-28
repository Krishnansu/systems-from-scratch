# Database Command References

This directory contains practical command and SQL references for Module 09. Use disposable local databases or approved development environments.

## Lessons
- [130 — Database Fundamentals](130-database-fundamentals.md)
- [131 — Indexing](131-indexing.md)
- [132 — Transactions](132-transactions.md)
- [133 — Isolation Levels](133-isolation-levels.md)
- [134 — Replication](134-replication.md)
- [135 — Sharding](135-sharding.md)
- [136 — Connection Pooling](136-connection-pooling.md)
- [137 — Redis](137-redis.md)

## General Safety Notes
- Confirm the target database and environment before running commands.
- Treat SQL or Redis commands that create, modify, or delete data as state-changing.
- Use parameterized queries rather than concatenating untrusted SQL input.
- Do not run exploratory or destructive commands against production.
- Keep credentials and sensitive query results out of source control and shared logs.
