# Lesson 134 — Replication: Commands

Use only a database environment where you have permission to inspect replication state. These examples are observational; availability of statistics and columns may depend on PostgreSQL version and permissions.

## Check whether the server is in recovery
```sql
SELECT pg_is_in_recovery();
```
A physical standby normally returns `true`. A `false` result alone does not establish the intended role in every architecture.

## Inspect connected standbys on the primary
```sql
SELECT
    application_name,
    client_addr,
    state,
    sync_state,
    sent_lsn,
    write_lsn,
    flush_lsn,
    replay_lsn
FROM pg_stat_replication;
```
The view reports connected WAL senders and standby progress. It may return no rows when no standby is connected.

## Inspect the WAL receiver on a standby
```sql
SELECT
    status,
    written_lsn,
    flushed_lsn,
    latest_end_lsn,
    latest_end_time
FROM pg_stat_wal_receiver;
```
Use this to inspect receiver status and reported WAL progress. Receiving and replaying WAL are distinct stages.

## Investigation checklist
- Confirm whether the query runs on the intended primary or standby.
- Check whether a standby is connected and whether its state is healthy.
- Compare send, write, flush, and replay positions where available.
- Check whether lag reflects delayed delivery, delayed replay, or an idle workload before interpreting time-based metrics.
- Confirm permissions and PostgreSQL version when a view or column is unavailable.

## Safety
- Do not test promotion, failover, or replication reconfiguration on production.
- Observational statistics do not by themselves prove that a failover will be lossless or safe.
- Follow the database platform's documented procedure for recovery and promotion.
