# Lesson 54 — JWT

## Objectives

- Understand what a JSON Web Token (JWT) is and why it exists.
- Understand the structure of a JWT: header, payload, and signature.
- Distinguish encoding from encryption.
- Understand signing and signature verification.
- Understand authentication versus authorization.
- Understand how JWTs can reduce per-request server-side session lookups.
- Understand access tokens, refresh tokens, expiration, and revocation trade-offs.
- Understand symmetric versus asymmetric signing.
- Understand key rotation and distributed verification.
- Understand where JWTs are stored for browser and non-browser clients.

## Prerequisites

- HTTP statelessness
- Cookies and sessions
- Authentication basics
- Basic cryptography concepts

## Concept Summary

A JWT is a compact, signed representation of claims that can be carried by a client and verified by a server.

A typical JWT has three parts:

```text
HEADER.PAYLOAD.SIGNATURE
```

The core architectural difference from a traditional session is:

```text
Session:

Client → session_id → Server → Session Store → User

JWT:

Client → signed JWT → Server → verify signature → Claims
```

JWT can therefore make access-token validation independent of per-user server-side session state.

## Core Ideas

### 1. JWT Structure

Header:

```json
{
  "alg": "HS256",
  "typ": "JWT"
}
```

Payload:

```json
{
  "sub": "42",
  "role": "user",
  "iat": 1756650000,
  "exp": 1756653600
}
```

Signature:

```text
sign(header + payload, secret/private-key)
```

The three components are encoded and joined with dots.

### 2. Encoding Is Not Encryption

A normal signed JWT's header and payload can be decoded by anyone possessing the token.

```text
JSON
  ↓
Base64URL encoding
  ↓
JWT component
```

The signature protects integrity and authenticity. It does not provide confidentiality.

Never put secrets such as passwords into a normal JWT payload.

### 3. Signature Verification

When a server receives a JWT:

```text
Receive JWT
    ↓
Parse token
    ↓
Verify signature
    ↓
Validate relevant claims
    ↓
Authenticate request
```

An attacker can read the payload but cannot modify it and produce a valid signature without the appropriate signing key.

### 4. Claims

Important registered claims include:

- `iss` — issuer
- `sub` — subject
- `aud` — audience
- `exp` — expiration time
- `iat` — issued-at time
- `nbf` — not-before time

Claims should be validated according to the application's security requirements.

### 5. Authentication vs Authorization

JWT verification answers:

```text
Who does this credential represent?
```

Authorization answers:

```text
Is this identity allowed to perform this operation?
```

A valid JWT does not automatically grant permission for every operation.

### 6. JWT Does Not Have to Contain Everything

A JWT can be self-contained enough for authentication and some authorization decisions:

```text
JWT
 ├── sub = 42
 ├── role = user
 └── exp = ...
```

But the application may still need a database or cache lookup:

```text
JWT
 ↓
user_id = 42
 ↓
Database / Cache
 ↓
Current user data
```

The JWT should be treated as a signed credential, not as a copy of the user database.

### 7. Horizontal Scaling

With server-side sessions:

```text
                    Load Balancer
                   /      |      \
                  v       v       v
              Server A Server B Server C
                   \       |       /
                    \      |      /
                     Session Store
```

With locally verifiable JWTs:

```text
                    Load Balancer
                   /      |      \
                  v       v       v
              Server A Server B Server C
                 |        |        |
             verify    verify    verify
                 \        |        /
                    signed JWT
```

Each server can verify the token using the appropriate verification key.

### 8. Access Tokens and Refresh Tokens

A common design is:

```text
Login
  ↓
+-------------------+
| Access Token      | short-lived
+-------------------+

+-------------------+
| Refresh Token     | longer-lived
+-------------------+
```

The access token is used for normal API requests. A refresh token can be used to obtain a new access token after expiration.

This limits the lifetime of the frequently presented access credential while providing a mechanism for continued login.

### 9. Revocation Trade-off

With a server-side session, logout can remove the session immediately:

```text
ABC123 → User 42
       ↓
     delete
       ↓
ABC123 → nothing
```

A self-contained JWT may remain cryptographically valid until expiration.

Therefore JWT-based systems may use short-lived access tokens, refresh-token revocation, deny lists, or additional server-side checks when immediate invalidation is required.

### 10. Symmetric vs Asymmetric Signing

Symmetric signing, such as HS256:

```text
             Shared Secret
                /      \
             Sign     Verify
```

The same secret is needed for signing and verification.

Asymmetric signing, such as RS256:

```text
Private Key → Sign
Public Key  → Verify
```

This is useful in distributed systems because services can receive the public key without obtaining the signing secret.

### 11. Key Rotation

Signing keys eventually need to be replaced:

```text
K1 → K2
```

A distributed system may temporarily need multiple verification keys so that tokens issued under the previous key remain verifiable during the transition.

Key management and rotation are therefore important parts of production JWT infrastructure.

### 12. JWT Storage

JWT storage depends on the client type.

For browser applications, common approaches include:

- Secure, `HttpOnly` cookies.
- Short-lived tokens kept in application memory.
- Browser storage such as `localStorage`, with significant XSS considerations.

For native/mobile/desktop clients, persistent credentials should generally use platform-provided secure credential storage such as OS keychains or secure keystores.

For backend services, credentials should generally be managed using protected configuration or a secret-management system rather than treating them like browser tokens.

The important distinction is:

```text
JWT security = cryptographic protection + secure credential storage
```

A valid signature does not protect a legitimately stolen bearer token.

## Practical Example

A typical API request might look like:

```text
Client
  |
  | Authorization: Bearer <JWT>
  v
API Server
  |
  | verify signature
  | validate exp / iss / aud
  v
Authenticated User
  |
  | authorization check
  v
Application logic
```

The JWT might contain only:

```json
{
  "sub": "42",
  "role": "user",
  "exp": 1788200000
}
```

If the endpoint requires additional user information, the application can retrieve it separately.

## Production Perspective

JWTs are particularly useful when multiple independently deployed services need to verify the same authentication credential.

```text
                 Authentication Service
                         |
                    signs JWT
                         |
                         v
                    API Gateway
                         |
          +--------------+--------------+
          |              |              |
          v              v              v
       Users          Orders        Payments
       Service        Service        Service
          |              |              |
       verify          verify        verify
```

However, JWTs introduce operational concerns around signing-key management, key rotation, token lifetime, refresh tokens, revocation, and authorization correctness.

## Common Mistakes

### JWT payloads are encrypted

Usually false. A normal JWT is signed/encoded, not encrypted.

### A valid JWT means every operation is allowed

False. Authentication and authorization are separate.

### JWT means there is no server-side state anywhere

False. User databases, refresh-token state, revocation state, signing keys, and authorization data may still exist.

### JWT always eliminates database lookups

False. It can eliminate the per-request session lookup, but applications may still need user or authorization data.

### JWT is automatically better than sessions

False. JWT and sessions make different trade-offs, particularly around scalability, revocation, server-side control, and key management.

### Storing a JWT securely is unimportant because it is signed

False. A stolen valid JWT can usually be replayed as a bearer credential until it expires or is otherwise invalidated.

## Key Takeaways

1. A JWT is commonly structured as `header.payload.signature`.
2. The payload is normally encoded, not encrypted.
3. The signature provides integrity and authenticity.
4. JWTs can carry identity and authorization claims.
5. A JWT can be minimal; it does not need to contain the complete user profile.
6. JWT verification and application-data lookup are separate concerns.
7. JWTs can simplify horizontally scaled authentication by enabling local verification.
8. Short-lived access tokens and refresh tokens are common architectural patterns.
9. Revocation is harder for self-contained JWTs than for server-side sessions.
10. Symmetric signing uses a shared secret; asymmetric signing separates signing and verification keys.
11. Key rotation is an important production concern.
12. A JWT is a bearer credential and must be protected wherever it is stored.
13. The real systems question is where authentication state lives and what trade-offs that creates.

## Reflection Questions

1. Why can a service verify a JWT without querying a session store?
2. Why is a signed JWT readable by the client?
3. Why can a JWT contain only a user ID instead of the complete user profile?
4. Why is JWT revocation harder than deleting a server-side session?
5. Why might asymmetric signing be preferable when many services verify tokens?
6. Why is secure token storage important even though JWTs are cryptographically signed?

## Related Lessons

- Lesson 53 — Sessions
- Lesson 55 — Caching

## What's Next

Lesson 55 — Caching: understand why systems keep copies of frequently accessed data closer to consumers, and how cache hierarchy, TTL, eviction, invalidation, cache stampedes, hot keys, and distributed caches affect real production systems.
