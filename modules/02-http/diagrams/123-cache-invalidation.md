# Diagram 123 — Cache Invalidation

```text
                    UPDATE REQUEST
                           |
                           v
                       DATABASE
                       price=150
                           |
                           v
                    INVALIDATE CACHE
                           |
                           v
                         CACHE
                       entry removed
                           |
                           |
                    next read is MISS
                           |
                           v
                       DATABASE
                           |
                           v
                       fresh data
                           |
                           v
                         CACHE
```

Invalidation removes or refreshes a cached copy after source data changes. TTL can provide a fallback expiration mechanism, but explicit invalidation can provide fresher results when updates are known.
