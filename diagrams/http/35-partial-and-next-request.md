# Complete Request Followed by Partial Request

```text
TCP recv() #1

+----------------------+----------------------+
| Complete Request 1   | Partial Request 2    |
+----------------------+----------------------+
          |
          v
    Parse Request 1
          |
          v
    Send Response 1
          |
          v
    Remove Request 1
          |
          v
+----------------------+
| Partial Request 2    |
+----------------------+
          |
          | recv() #2
          v
+---------------------------------------------+
| Complete Request 2                          |
+---------------------------------------------+
          |
          v
    Parse Request 2
          |
          v
    Send Response 2
```

**Key Points**
- A buffer can contain a complete request and part of the next request.
- The complete request is processed immediately.
- The partial request remains in the buffer.
- New TCP bytes are appended to the existing buffer.