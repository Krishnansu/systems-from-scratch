# Diagram 120 — Cache Hit vs Cache Miss

```text
                         REQUEST
                            |
                            v
                         CACHE
                        /     \\
                      HIT     MISS
                       |        |
                       v        v
                    Return    SOURCE
                     data       |
                                v
                              Fresh
                               data
                                |
                                v
                              CACHE
                                |
                                v
                             RESPONSE
```

A cache hit returns the cached copy immediately. A miss requires the application to obtain the data from the source of truth and commonly populate the cache for future requests.
