# Diagram 125 — Distributed Redis

```text
                         REDIS CLUSTER
                              |
              +---------------+---------------+
              |               |               |
              v               v               v
          +---------+     +---------+     +---------+
          | Node A  |     | Node B  |     | Node C  |
          |  Redis  |     |  Redis  |     |  Redis  |
          +---------+     +---------+     +---------+
              |               |               |
             RAM             RAM             RAM
              |               |               |
           Keys A          Keys B          Keys C

             Sharding → distributes keys across nodes
             Replication → keeps additional copies
```

A distributed Redis deployment is a collection of Redis processes running on multiple machines. The working dataset resides primarily in each node's RAM. Sharding distributes keys; replication provides additional copies for availability.
