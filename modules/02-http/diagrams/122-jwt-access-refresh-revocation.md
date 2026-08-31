# Diagram 122 — JWT Access Token, Refresh Token & Revocation

```text
                         LOGIN
                           |
                           v
                  +-------------------+
                  | Authentication    |
                  | Server             |
                  +-------------------+
                     /             \
                    /               \
                   v                 v
          +----------------+  +----------------+
          | Access Token   |  | Refresh Token  |
          | short-lived    |  | long-lived     |
          +----------------+  +----------------+
                  |
                  |
                  | API requests
                  v
             Application


Access token expires
        |
        v
Refresh token
        |
        v
Authentication Server
        |
        v
New access token


REVOCATION TRADE-OFF

Server-side session:

ABC123 → User 42
        |
      logout
        v
ABC123 → deleted

JWT:

JWT → cryptographically valid
 |
 +-- may remain usable until expiration
 |
 +-- unless additional revocation/state checks exist
```
