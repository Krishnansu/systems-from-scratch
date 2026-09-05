# Lesson 55 — Caching: Redis Persistence, Replication & Failure Model

## Redis Persistence

Redis primarily keeps its working dataset in RAM. RAM is fast but volatile, so persistence mechanisms can be used to recover state after a process or machine restart.

### RDB — Snapshotting

RDB periodically creates a point-in-time snapshot of the dataset.

```text
12:00       12:05       12:10
  |           |           |
Snapshot    Snapshot    Snapshot
              |
              v
        Crash at 12:08
              |
              v
       Recover from 12:05
```

Changes made after the latest snapshot may be lost.

Mental model:

> RDB = "What did the dataset look like at this point in time?"

### AOF — Append Only File

AOF records write operations so Redis can replay them during recovery.

```text
WRITE A
WRITE B
WRITE C
   |
   v
  AOF
   |
   v
Replay after restart
```

Mental model:

> AOF = "What write operations happened?"

Redis can use persistence mechanisms together depending on the durability requirements.

## Persistence vs Availability

Persistence and replication solve different failure problems.

```text
Persistence
    |
    v
Process / machine restart
    |
    v
Recover state

Replication
    |
    v
Primary failure
    |
    v
Use replica / failover
```

Persistence does not automatically keep the service available while a node is down.

Replication does not automatically guarantee zero data loss.

## Redis Replication

A common topology is:

```text
        Primary
           |
      replication
           |
           v
        Replica
```

The replica maintains a copy of the primary's data and can potentially be promoted if the primary fails.

Replication is commonly asynchronous. Therefore:

```text
Primary  = newest state
Replica  = slightly older state
```

If the primary fails before a recent write reaches the replica, the promoted replica may not contain that latest acknowledged write.

This creates a replication-lag failure window.

## Redis Cluster + Replication

A distributed Redis deployment can combine sharding and replication:

```text
Primary A  ---> Replica A
    |
  Slots

Primary B  ---> Replica B
    |
  Slots

Primary C  ---> Replica C
    |
  Slots
```

Each primary owns part of the keyspace. Its replica provides another copy of that partition.

Remember:

> Sharding answers "where does the data live?"
>
> Replication answers "how many copies exist?"

## Failure Scenarios

### Primary fails, replica survives

```text
Primary A  X
     |
     v
Replica A
     |
     v
Promote replica
```

The replica can potentially take over the failed primary's role.

### Primary fails before replication catches up

```text
Client
  |
  v
Primary
  |
  |  write acknowledged
  |
  X  failure before replica receives it
  |
  v
Replica
```

The latest acknowledged state may be missing from the replica.

Therefore:

> Replication improves availability and fault tolerance, but asynchronous replication can still have a data-loss window.

### Both primary and replica fail

The impact depends on whether Redis is merely a cache or the source of truth.

If Redis is a cache:

```text
Redis data lost
      |
      v
Read database
      |
      v
Repopulate cache
```

If Redis is the source of truth, losing all recoverable copies can become a genuine data-loss event unless persistence/backups provide recovery.

## Failure Protection Hierarchy

Different mechanisms protect against different failures:

```text
Persistence
    |
    v
Restart / recovery

Replication
    |
    v
Single-node failure

Multiple replicas / failure domains
    |
    v
Infrastructure failure

Source-of-truth database / backups
    |
    v
Catastrophic cache loss
```

A production system may combine several of these mechanisms.

## Important Distinction

Do not think:

```text
Redis replication = backup
```

A replica is another live copy of the current dataset. If bad data is written or deleted on the primary, that change can also propagate to replicas.

Backups/persistence serve a different recovery purpose.

Mental model:

```text
Replication -> "Keep another live copy"
Persistence -> "Recover state after restart"
Backup      -> "Recover an older recoverable state"
```

## Production Perspective

When Redis is used purely as a cache, durability requirements are often lower because the database remains the source of truth.

When Redis is used as a primary datastore, durability and recovery requirements become much more important.

Production design should consider:

- Persistence strategy
- Replication topology
- Replication lag
- Failover behaviour
- Number of replicas
- Failure-domain placement
- Backup and recovery strategy
- Whether Redis is cache or source of truth
- Acceptable data-loss window

## Key Takeaways

- Redis primarily keeps its working dataset in RAM.
- RDB provides point-in-time snapshots.
- AOF records write operations for replay-based recovery.
- Persistence primarily addresses restart/recovery.
- Replication primarily addresses node failure and availability.
- Redis replication is commonly asynchronous, so replicas can lag.
- Failover can therefore involve a small data-loss window.
- Sharding distributes data; replication duplicates data.
- Replication is not the same as backup.
- A cache can often be rebuilt from its source of truth after total cache loss.
- If Redis is the source of truth, persistence and recovery become critical.
