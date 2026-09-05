# Diagram 124 — Cache Stampede

```text
                    HOT CACHE KEY
                         |
                    EXPIRES
                         |
          +--------------+--------------+
          |              |              |
          v              v              v
       Request A       Request B      Request C
          |              |              |
          +--------------+--------------+
                         |
                       MISS
                         |
                         v
                    DATABASE
                         |
                  overloaded by
                  many identical
                     requests
```

A cache stampede occurs when many requests miss the same popular key at once and all reach the source of truth. Request coalescing, locking, jittered TTLs, and stale-while-revalidate are common mitigation strategies.
