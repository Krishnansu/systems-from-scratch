# Diagram 118 — Distributed Sessions

```text
                         Users
                           |
                           v
                    +-------------+
                    |Load Balancer|
                    +-------------+
                       /       \
                      /         \
                     v           v
              +-----------+ +-----------+
              | Server A  | | Server B  |
              +-----------+ +-----------+
                     \           /
                      \         /
                       v       v
                   +-------------+
                   |   Session   |
                   |    Store    |
                   +-------------+
                         |
                         v
                    User State

             ABC123 → User 42
```

A shared session store allows multiple application servers to resolve the same session identifier.
