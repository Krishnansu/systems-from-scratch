# Diagram 117 — Cookie vs Session

```text
                    AUTHENTICATION STATE

Browser                                      Server

+-------------------------+                  +-------------------------+
| Cookie                  |                  | Session Store           |
|                         |                  |                         |
| session_id = ABC123     |----------------->| ABC123 → User 42       |
|                         |                  | authenticated = true   |
+-------------------------+                  +-------------------------+

        Client-side                              Server-side
        identifier                              application state
```

A cookie transports the identifier. The session is the server-side state associated with that identifier.
