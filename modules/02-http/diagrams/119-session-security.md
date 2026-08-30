# Diagram 119 — Session Security

```text
SESSION HIJACKING

Attacker
   |
   | stolen session ID
   | ABC123
   v
Server
   |
   v
ABC123 → User 42
   |
   v
Authenticated as User 42


SESSION FIXATION DEFENSE

Before login:
ABC123 → anonymous

Successful authentication:
ABC123 → invalidated
XYZ789 → User 42

Regenerating the session ID breaks the attacker's knowledge of the pre-login identifier.
```
