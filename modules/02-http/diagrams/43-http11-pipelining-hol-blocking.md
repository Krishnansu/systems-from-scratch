# HTTP/1.1 Pipelining and Head-of-Line Blocking

```text
Client                         Server

Request A ------------------->
Request B ------------------->
Request C ------------------->

                         A = slow
                         B = fast
                         C = fast

             <--------------- Response A
             <--------------- Response B
             <--------------- Response C
```

Even if B and C finish before A, their responses cannot move ahead of A when ordered pipelining is used.

```text
A ────────────────────┐
B ──────── ready ─────┤── wait
C ──────── ready ─────┤── wait
                      ▼
                 Response A
                      ↓
                 Response B
                      ↓
                 Response C
```

**Key Point**

A slow request at the front of the sequence can block later responses. This is head-of-line blocking.