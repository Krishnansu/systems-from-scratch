# HTTP/2 Binary Framing

```text
HTTP/2
  |
  v
+----------------------+
| Length               |
+----------------------+
| Type                 |
+----------------------+
| Flags                |
+----------------------+
| Stream ID            |
+----------------------+
| Payload              |
+----------------------+
```

Common frame types include HEADERS, DATA, SETTINGS, WINDOW_UPDATE, PING and GOAWAY.

**Key Point**

HTTP/2 retains HTTP semantics but represents communication using binary frames.