# Diagram 122 — Cache-Aside

```text
                         REQUEST
                            |
                            v
                       APPLICATION
                            |
                            v
                          CACHE
                         /     \\
                       HIT     MISS
                        |        |
                        |        v
                        |     DATABASE
                        |        |
                        |        v
                        |      CACHE
                        |        |
                        +--------+
                            |
                            v
                         RESPONSE
```

In cache-aside, the application owns cache lookup and population. A miss reads from the database, stores the result in the cache, and returns it to the caller.
