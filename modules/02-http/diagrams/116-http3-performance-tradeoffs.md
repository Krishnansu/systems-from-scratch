# Diagram 116 — HTTP/3 Performance & Trade-offs

```text
                         HTTP/3
                            |
              +-------------+-------------+
              |                           |
           Benefits                     Costs
              |                           |
      +-------+-------+           +-------+-------+
      |       |       |           |       |       |
 Independent  0-RTT  Migration   More   CPU /   UDP
  streams                     complexity memory  deployment
      |
      v
Reduced TCP-level
cross-stream HOL blocking
      |
      v
Better behavior under
packet loss
```

The important point is that HTTP/3 trades additional transport complexity for capabilities that TCP cannot provide to HTTP/2.
