# Diagram 121 — Cache Hierarchy

```text
                         CLIENT
                            |
                            v
                     +-------------+
                     |   Browser   |
                     |    Cache    |
                     +-------------+
                            |
                       cache miss
                            |
                            v
                     +-------------+
                     |     CDN     |
                     |    Cache    |
                     +-------------+
                            |
                       cache miss
                            |
                            v
                     +-------------+
                     |   Reverse   |
                     |    Proxy    |
                     +-------------+
                            |
                       cache miss
                            |
                            v
                     +-------------+
                     | Application |
                     +-------------+
                            |
                            v
                     +-------------+
                     | Distributed |
                     |    Cache    |
                     |    Redis    |
                     +-------------+
                            |
                       cache miss
                            |
                            v
                     +-------------+
                     |  Database   |
                     |    Source   |
                     |   of Truth  |
                     +-------------+
```

Different layers optimize different parts of the request path. Browser/CDN caches can avoid reaching the origin entirely, while application/distributed caches primarily reduce backend work and latency.
