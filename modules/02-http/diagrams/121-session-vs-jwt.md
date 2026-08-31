# Diagram 121 — Session vs JWT

```text
              SERVER-SIDE SESSION

Client
  |
  | session_id = ABC123
  v
Server
  |
  | lookup
  v
Session Store
  |
  v
User 42


              JWT

Client
  |
  | signed JWT
  v
Server
  |
  | verify signature
  v
Claims
  |
  v
User 42


KEY DIFFERENCE

Session → server looks up per-user state
JWT     → server can verify the credential locally
```
