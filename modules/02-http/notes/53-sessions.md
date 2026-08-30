# Lesson 53 — Sessions

## Objectives

- Understand why application-level sessions are needed when HTTP is stateless.
- Distinguish cookies from sessions.
- Understand session IDs and server-side session state.
- Trace login and authenticated-request flows.
- Understand session expiration, fixation, and hijacking.
- Understand why sessions become a distributed-systems problem when applications scale horizontally.
- Understand sticky sessions versus shared session stores.

## Prerequisites

- HTTP request/response model
- HTTP cookies and statelessness
- HTTP status codes
- Load balancing basics

## Theory

HTTP is stateless: each HTTP request is independently interpretable by the protocol. Applications often need continuity across requests, such as remembering that a user has logged in.

A session provides application-level state associated with a session identifier.

```text
Browser
   |
   | session_id = ABC123
   v
Server
   |
   v
Session Store
   |
   v
User 42
```

The session ID is commonly transported in a cookie.

Important distinction:

```text
Cookie  = client-side storage/transport mechanism
Session = server-side state associated with an identifier
```

## Real World Example

A typical login flow:

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

The client carries the identifier; the server determines what that identifier means.

## Deep Dive

### Session State

A session may contain information such as:

```text
Session ABC123

user_id       = 42
authenticated = true
created_at    = ...
expires_at    = ...
```

Session state should generally remain reasonably small and should not become an uncontrolled application-state dump.

### Session IDs

A session ID should be unpredictable, sufficiently random, and treated as a credential. A user should not be able to modify a session ID to select another user's identity.

The safer model is:

```text
Client sends:
    session_id = ABC123

Server decides:
    ABC123 → User 42
```

### Expiration

Sessions commonly have expiration policies.

Absolute expiration:

```text
Created: 10:00
Expires: 18:00
```

Idle expiration:

```text
No activity for 30 minutes
        ↓
Session expires
```

Production systems may combine both.

### Cookie Security

Authentication cookies commonly use:

- `Secure` — send the cookie only over HTTPS.
- `HttpOnly` — prevent normal JavaScript access to the cookie.
- `SameSite` — control cross-site cookie sending and help with CSRF defenses.

### Session Hijacking

A stolen valid session ID can allow an attacker to act as the associated user because the session ID is generally a bearer credential.

```text
Attacker
   |
   | stolen session_id = ABC123
   v
Server
   |
   v
ABC123 → User 42
```

Therefore session IDs must be protected like authentication credentials.

### Session Fixation

Session fixation occurs when an attacker causes a victim to use a known session identifier and that identifier later becomes authenticated.

A key defense is to regenerate the session ID after successful authentication:

```text
Before login:
ABC123 → anonymous

Successful login:
ABC123 → invalidated
XYZ789 → User 42
```

### Horizontal Scaling

A single server can keep sessions in its own memory:

```text
User
  ↓
Server
  ↓
Memory
```

But this breaks down when requests can reach multiple servers.

```text
                 Load Balancer
                /             \
               v               v
           Server A         Server B
```

If the session exists only in Server A's memory, Server B cannot find it.

### Sticky Sessions

A load balancer can attempt to keep a user on the same application server.

```text
User
  |
  v
Load Balancer
  |
  v
Server A
  |
  +-- Session ABC123
```

This is simple but introduces operational drawbacks. If Server A fails and session state exists only there, the session may be lost.

### Shared Session Store

A common scalable architecture moves session state into shared infrastructure.

```text
                    Load Balancer
                    /           \
                   v             v
             Server A        Server B
                   \             /
                    \           /
                     v         v
                   Session Store
```

Both servers can resolve:

```text
ABC123 → User 42
```

An in-memory distributed store such as Redis is a common implementation choice.

Conceptually:

```text
Key:   session:ABC123
Value: { user_id: 42, authenticated: true }
TTL:   1800 seconds
```

### Distributed Dependency

Moving sessions to a shared store solves application-server locality but introduces a new dependency:

```text
Request
   |
   +-- Application Server
   |
   +-- Session Store
```

If the session store becomes unavailable, authenticated requests may fail even when the application servers themselves are healthy.

This makes session management a distributed-systems concern involving:

- replication
- failover
- persistence
- expiration
- eviction
- capacity
- network latency
- connection management

## Hands-on Exercise

Build a minimal HTTP application with:

1. `POST /login`
2. A generated random session ID.
3. An in-memory session map.
4. `Set-Cookie` on successful login.
5. An authenticated endpoint such as `GET /profile`.
6. Session expiration.
7. Logout that destroys the session.

Then run two application instances and observe why process-local sessions do not naturally work when requests are distributed between instances.

## Common Misconceptions

### Cookies and sessions are the same thing

They are not. A cookie is a client-side storage/transport mechanism; a session is application state associated with an identifier.

### HTTP being stateless means servers cannot maintain state

False. Statelessness describes HTTP's request model. Applications can maintain state independently.

### Sending user_id directly in a cookie is sufficient authentication

Not by itself. The client controls the cookie and could modify the value. Server-controlled session state avoids trusting an arbitrary client-provided identity value.

### Sticky sessions solve all scaling problems

They solve session locality but create coupling between users and servers and can make failure handling more difficult.

### JWT is automatically better than sessions

Not necessarily. JWT and server-side sessions make different trade-offs around state, revocation, token size, expiration, and failure behavior.

## Summary

Sessions provide application-level continuity over stateless HTTP by associating a client-held session identifier with server-side state. Cookies commonly transport the identifier. A simple in-memory implementation works on one server but creates problems under horizontal scaling. Sticky sessions are one solution, while shared session stores allow multiple application servers to access the same state. This introduces distributed-system concerns around availability, latency, replication, and failure.

## Key Takeaways

1. HTTP is stateless, but applications can maintain state across requests.
2. A session is server-side state associated with a session identifier.
3. Cookies commonly transport session IDs.
4. Cookie and session are different concepts.
5. Session IDs are bearer credentials and must be protected.
6. Authentication sessions need sensible expiration policies.
7. Regenerating the session ID after login helps prevent session fixation.
8. Process-local sessions do not naturally scale across multiple application servers.
9. Sticky sessions provide locality but introduce operational trade-offs.
10. Shared session stores allow horizontal scaling but introduce another distributed dependency.
11. Session management is ultimately a state-management problem.

## Reflection Questions

1. Why can't two independently running application servers reliably share in-memory sessions?
2. What is the difference between a cookie and a session?
3. Why should a session ID be treated like a credential?
4. What problem do sticky sessions solve, and what problems do they introduce?
5. What new failure mode appears when sessions are moved into a shared store?

## What's Next

Lesson 54 — JWT: explore an alternative authentication model where the client carries a signed token and the server can often authenticate without a central session lookup.
