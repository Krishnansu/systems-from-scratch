# Diagram 131 — WebSocket Production Architecture

```text
                         Internet
                            |
                            v
                     Load Balancer
                      /          \
                     v            v
              WebSocket S1   WebSocket S2
                     |            |
                     +-----+------+
                           |
                           v
                    Message Broker
                           |
                           v
                    Backend Services
                           |
                           v
                        Database
```
