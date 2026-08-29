# Multiple HTTP Requests in One TCP Buffer

```text
             TCP recv()
                 |
                 v
+----------------------+----------------------+
|      Request 1       |      Request 2       |
+----------------------+----------------------+
          |
          | Parse Request 1
          v
+----------------------+----------------------+
|      Request 1       |      Request 2       |
+----------------------+----------------------+
          |
          | Consumed
          v
+----------------------+
|      Request 2       |
+----------------------+
          |
          | Process Request 2
          v
+----------------------+
|        Empty         |
+----------------------+
```

**Key Points**
- One TCP `recv()` can contain multiple HTTP requests.
- The server should process all complete requests currently available.
- After parsing Request 1, bytes belonging to Request 2 must not be discarded.
- The remaining bytes become the new buffer.