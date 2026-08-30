# Diagram 113 - QPACK Static vs Dynamic Table

```text
                         QPACK
                           |
             +-------------+-------------+
             |                           |
             v                           v
        STATIC TABLE               DYNAMIC TABLE
             |                           |
             |                           |
       Fixed by spec              Connection state
       Known beforehand           Changes during connection
       Never updated              Insert / evict entries
             |                           |
             |                           ^
             |                           |
             |                    Encoder Stream
             |                           |
             +-------------+-------------+
                           |
                           v
                    Header Compression
                           |
                           v
                    HTTP/3 HEADERS
```

The important distinction is:

```text
STATIC  = predefined and immutable
DYNAMIC = created and modified during the connection
```

The static table does not get periodically refreshed or updated like the dynamic table.
