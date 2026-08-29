# HTTP/1.1 Limitations

```text
                    HTTP/1.1
                       │
             ┌─────────┴─────────┐
             ▼                   ▼
   Multiple Connections      Pipelining
             │                   │
             ▼                   ▼
 Connection overhead      Ordered responses
                                 │
                                 ▼
                         Head-of-line blocking
```

**Key Point**

HTTP/1.1 needs multiple independent requests to make progress efficiently, but multiple connections add overhead and pipelining is constrained by response ordering.