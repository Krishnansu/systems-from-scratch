# Diagram 116 — Session Login Flow

```text
Browser                         Server
  |                               |
  | POST /login                   |
  | username + password           |
  |------------------------------>|
  |                               |
  |                       Validate credentials
  |                       Create session
  |                       session_id = ABC123
  |                               |
  | Set-Cookie: session_id=ABC123 |
  |<------------------------------|
  |                               |
  | Store cookie                  |
  |                               |
  | GET /profile                  |
  | Cookie: session_id=ABC123     |
  |------------------------------>|
  |                               |
  |                    Lookup ABC123
  |                    User = 42
  |                               |
  | Profile response              |
  |<------------------------------|
```
