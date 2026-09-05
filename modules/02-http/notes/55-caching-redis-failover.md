# Redis Failover, Quorum & Split-Brain

## Why Failover Exists

Redis replication provides a backup copy of data, but replication alone does not decide what happens when the primary becomes unavailable.

A distributed system needs to determine:

- Is the primary actually failed?
- Is it merely unreachable?
- Which replica should become the new primary?
- Do enough nodes agree to make the decision safely?

## Failure Detection

Nodes exchange health information such as heartbeats.

```text
A <----> B
 \       /
  \     /
    ---> C
```

If a node stops communicating, other nodes may suspect it has failed.

Important distinction:

```text
Node is dead
    ≠
Node is unreachable
```

A network failure can make a healthy node appear dead.

## Network Partition

A network partition occurs when nodes remain alive but cannot communicate across the partition.

```text
        Network Partition
              ||
       +------+------+
       |             |
       A            B --- C
    PRIMARY
```

A is still physically alive, but B and C cannot reach it.

## Quorum

Quorum is the minimum number of participating voting nodes required for a distributed decision to be considered authoritative.

For `N` voting nodes:

```text
Quorum = floor(N / 2) + 1
```

Examples:

```text
3 nodes → quorum 2
5 nodes → quorum 3
```

The important property is that two different majorities of the same fixed voting set must overlap. This helps prevent independent groups from both obtaining authority.

Quorum is not itself a health check or an election algorithm. It is a threshold used by the coordination/failover mechanism.

## Failover

Conceptually, when a primary becomes unavailable:

```text
Primary A
    |
    X  unreachable
    |
Replica B
    |
    +---- asks for authority
    |
    v
Other voting nodes
    |
    v
Enough agreement?
   /       \\
 No         Yes
 |            |
No takeover  Promote B
```

If the failover mechanism determines that a replica has sufficient authority, the replica can be promoted and take ownership of the failed primary's responsibility.

In Redis Cluster, the failover process is coordinated by cluster nodes rather than by simply having a replica unilaterally declare itself primary.

## Why Unreachable Does Not Mean Dead

Consider:

```text
A = original primary
B = replica
C = cluster participant

A        B --- C
|             |
alive         |
PRIMARY       |
              +-- quorum
              +-- B promoted
```

A may still believe it is primary because it never received the failover decision.

Therefore:

```text
A → "I am still primary"
B → "I am now primary"
```

This is the fundamental split-brain scenario.

## Split-Brain

Split-brain occurs when two separated parts of a distributed system both believe they have authority.

```text
        Network Partition
              ||
       +------+------+
       |             |
       A             B
    PRIMARY        PRIMARY
       |             |
    writes X       writes Y
```

Promoting B does not magically send a message to A if A is unreachable. A can remain alive and continue operating according to its old state unless the system has a mechanism that prevents it from accepting authoritative work.

## What Happens When the Network Heals?

The system cannot blindly synchronize both sides.

Suppose:

```text
Initial balance = ₹1000

A side:
withdraw ₹700 → ₹300

B side:
withdraw ₹800 → ₹200
```

After connectivity returns, the system must determine which history is authoritative. Simply merging the two states can produce an incorrect result.

Therefore systems generally prefer to **prevent split-brain** rather than rely on post-partition reconciliation.

When reconciliation is required, the system may need to:

- Determine the authoritative history.
- Reject or discard writes from the losing side.
- Replay valid operations.
- Merge non-conflicting changes where the data model permits it.

Synchronization is therefore better understood as **history reconciliation**, not merely copying data between nodes.

## Quorum vs Failure Detection vs Election

These concepts solve different problems:

```text
Failure Detection
        |
        v
"Is A considered unavailable?"
        |
        v
Election / Failover
        |
        v
"Who should take over?"
        |
        v
Quorum
        |
        v
"Do we have enough authority to decide?"
```

Quorum does not automatically guarantee that every write has been replicated before acknowledging it.

Therefore:

```text
Quorum for failover
        ≠
Quorum for every data write
```

With asynchronous replication, a primary can still fail before its latest acknowledged write reaches the replica.

## Redis Cluster Mental Model

For a simplified Redis Cluster topology:

```text
Primary A ─── Replica A
Primary B ─── Replica B
Primary C ─── Replica C
```

Sharding determines which primary owns a key's hash slot.

Replication provides additional copies.

Failover allows an appropriate replica to take over when its primary is considered failed.

The overall chain is:

```text
Failure detection
        ↓
Failure/failover coordination
        ↓
Quorum / sufficient authority
        ↓
Replica promotion
        ↓
New primary ownership
```

## Production Perspective

A production distributed system must account for more than machine crashes. It must also handle:

- Network partitions
- Delayed messages
- Nodes that are alive but unreachable
- Simultaneous failures
- Competing failover attempts
- Stale state
- Data that was acknowledged but not yet replicated

This is why distributed coordination is fundamentally harder than simply checking whether a server is running.

## Key Takeaways

- Failure detection determines whether a node is considered unavailable.
- An unreachable node may still be alive.
- Quorum provides the authority threshold for distributed decisions.
- Failover determines whether and which replica should take over.
- Promoting a replica does not physically stop an unreachable primary from believing it is primary.
- Split-brain occurs when multiple sides believe they are authoritative.
- Network partitions are therefore fundamentally dangerous.
- Systems prefer preventing split-brain through coordination rather than relying entirely on reconciliation afterward.
- After a partition heals, synchronization may require resolving conflicting histories, not merely copying state.
- Failover quorum does not automatically guarantee zero data loss for writes.
- These problems motivate consensus algorithms such as Raft, which provide stronger guarantees about distributed authority.
