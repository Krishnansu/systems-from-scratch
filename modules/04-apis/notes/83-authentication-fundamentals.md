# Lesson 83 — Authentication Fundamentals

## Objectives

- Understand authentication and why systems need it.
- Distinguish authentication from authorization.
- Explain identities, credentials, sessions, and access tokens.
- Understand authentication boundaries in distributed systems.

## Prerequisites

- API fundamentals and service-to-service communication
- HTTP sessions and JWT
- gRPC fundamentals

## Theory

Authentication verifies the identity of a user, service, or workload. Authorization determines which actions that established identity may perform. A supplied user ID is only a claim unless it is backed by a trusted authentication mechanism.

Core terms:

- **Identity:** The account or entity being represented.
- **Credential:** Evidence used to prove identity, such as a password, passkey, certificate, or token.
- **Principal:** The identity established by authentication and used in security decisions.
- **Session:** Server-managed state associated with an authenticated client.
- **Access token:** A credential presented to a resource server to establish a client's authorized context.

## Real World Example

A user logs in and receives a session cookie or access token. The API gateway may validate the credential before forwarding the request. The Order Service then checks whether the authenticated principal is allowed to access the requested order.

## Deep Dive

### Typical session flow

1. Client submits credentials over HTTPS.
2. The server verifies them and creates a session.
3. The client sends its session identifier on later requests, commonly in a cookie.
4. The server validates the session and establishes the principal.
5. Application authorization checks permissions for the requested resource.

Cookies should be configured appropriately, including Secure, HttpOnly, and SameSite where applicable. Session expiry, revocation, logout, and CSRF protection also matter.

### Tokens

- A signed JWT must have its signature and relevant claims validated, including issuer, audience, and expiration. Decoding alone is not validation.
- JWT payloads are not necessarily encrypted; do not put secrets in readable claims.
- Opaque tokens generally require a trusted lookup or introspection mechanism.
- A valid token does not guarantee that the principal still has permission to perform every action; authorization may depend on current application state.

### Authentication in distributed systems

- An identity provider or authentication service can handle login and credential issuance.
- An API gateway can authenticate requests at the edge and reject invalid credentials early.
- Backend services must not blindly trust spoofable identity headers or be exposed through an untrusted path that bypasses required controls.
- Services may validate signed tokens locally or use token introspection, depending on the architecture and revocation requirements.
- Service-to-service calls need workload authentication, such as mTLS or another supported credential mechanism. A user's session does not automatically authenticate the calling service.
- Workload identity establishes which service is calling; mTLS can use certificates to authenticate peers and secure the connection. Authorization remains a separate decision.
- Define whether downstream operations need the end-user identity, the calling service identity, or both.

### Production perspective

Use HTTPS, secure credential storage, expiry and revocation strategies, least privilege, and appropriate monitoring. Avoid logging passwords, access tokens, private keys, or session identifiers. Authentication should be consistent across services, while authorization should be enforced at the boundary that understands the requested resource and operation.

## Hands-on Exercise

1. Explain why a request containing `user_id=alice` does not establish Alice's identity by itself.
2. Distinguish authentication from authorization when Alice requests Bob's order.
3. Describe how a server-side session identifies a client on a subsequent request.
4. Explain the risk of trusting gateway authentication if a backend can be reached through an untrusted bypass.
5. Explain why a generated gRPC client stub does not, by itself, authenticate the caller.

## Common Misconceptions

- Authentication and authorization are the same thing.
- HTTPS alone proves the application's user identity.
- A decoded JWT is automatically trustworthy.
- Passing a user ID in a request proves who the caller is.
- Gateway authentication removes the need to secure backend trust boundaries.
- A user's credential automatically authenticates every downstream service.

## Summary

Authentication establishes who is making a request; authorization determines what that identity may do. Production systems can authenticate at the gateway and within services, use identity providers to issue credentials, and use workload identity for service-to-service trust. The correct design depends on trust boundaries, bypass paths, token validation, and resource-level authorization.

## Key Takeaways

- Authentication answers “Who are you?”; authorization answers “What may you do?”
- Credentials must be verified before a principal is trusted.
- Sessions and access tokens carry authenticated context in different ways.
- Gateways can authenticate at the edge, but backend trust boundaries must remain secure.
- User identity and workload identity are distinct and may both matter in a request.

## Reflection Questions

1. Why is authentication not sufficient to authorize access to a particular order?
2. What are the trade-offs between local JWT validation and opaque-token introspection?
3. In a service-to-service call, when does a system need the end-user identity as well as the calling service identity?

## What's Next

Lesson 84 — Authorization Fundamentals.
