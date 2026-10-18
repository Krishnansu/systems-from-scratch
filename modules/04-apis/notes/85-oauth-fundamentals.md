# Lesson 85 — OAuth Fundamentals

## Objectives
- Explain why OAuth exists and distinguish authorization from authentication.
- Identify OAuth roles and understand Authorization Code with PKCE.
- Distinguish authorization codes, access tokens, refresh tokens, and OIDC ID tokens.
- Understand Client Credentials flow and production security requirements.

## Prerequisites
- Lesson 83 — Authentication Fundamentals
- Lesson 84 — Authorization Fundamentals

## Theory
OAuth 2.0 allows an application to obtain limited access to a protected resource without collecting the resource owner's password. OAuth is primarily an authorization framework. OpenID Connect (OIDC) adds an identity layer for authentication.

### Core roles
- **Resource owner:** usually the user who can authorize access.
- **Client:** the application requesting access.
- **Authorization server:** authenticates the user as needed, obtains consent, and issues tokens.
- **Resource server:** the API hosting protected resources and enforcing access rules.

### Authorization Code with PKCE
1. The client creates a high-entropy code verifier and derives a code challenge.
2. The client redirects the user to the authorization server with the requested scopes, registered redirect URI, state, and PKCE challenge.
3. The authorization server authenticates the user as needed and obtains consent.
4. The user is redirected to the registered callback with a short-lived authorization code.
5. The client exchanges the code at the token endpoint, supplying the PKCE verifier.
6. The client sends the access token to the resource server.

PKCE binds the code exchange to the initiating client and helps prevent an intercepted authorization code from being redeemed by an attacker. Validate redirect URIs and use `state` to protect the authorization response flow.

### Token types
- **Authorization code:** short-lived, single-purpose credential exchanged for tokens; not an API access token.
- **Access token:** presented to a resource server to access protected resources within its intended audience, scope, and validity.
- **Refresh token:** exchanged at the authorization server for new access tokens when permitted.
- **OIDC ID token:** conveys authentication and identity claims to the client; it is not a substitute for an API access token.

Access tokens may be opaque or structured as JWTs. A resource server must validate tokens according to the issuer's design, not assume every token is a JWT.

### Scopes and permissions
Scopes express requested or granted permissions, such as `calendar.read` and `calendar.write`. A requested scope is not automatically granted. APIs must enforce the actual permissions and resource-level authorization.

### Client Credentials flow
Use this flow when an application acts on its own behalf rather than on behalf of a user:
1. The client authenticates to the authorization server using a supported client-authentication method.
2. The authorization server issues an access token within the client's allowed permissions.
3. The client presents that token to the resource server.

Client authentication may use a client secret, private-key-based authentication, or a supported workload identity mechanism. The access token is a separate credential used to call the API.

## Real World Example
A calendar application asks a user to grant read-only calendar access. OAuth lets the application obtain a limited token without receiving the user's calendar password. A scheduled backend reconciliation job may instead use Client Credentials to access an API as the job's own service identity.

## Deep Dive
- OAuth answers **what access is delegated**, while authentication establishes **who or what is acting**.
- OIDC ID tokens are intended for the client; access tokens are intended for resource servers. Do not treat them as interchangeable.
- Validate issuer, audience, expiry, signature or introspection result, and applicable scopes. Authorization still needs to be checked against the requested resource and action.
- Use HTTPS, exact redirect URI validation, PKCE for authorization-code flows, least-privilege scopes, and secure token storage.
- Keep confidential client secrets out of browser and mobile application bundles.
- Protect refresh tokens and use rotation or revocation controls where supported.
- A valid token does not automatically authorize every operation or resource.

## Hands-on Exercise
For a hypothetical calendar application:
1. Identify the resource owner, client, authorization server, and resource server.
2. Trace Authorization Code with PKCE from redirect to API request.
3. Explain what fails if an attacker intercepts the authorization code but lacks the PKCE verifier.
4. Explain why a token issued for the Calendar API should not be accepted by the Payments API.
5. Choose between Authorization Code with PKCE and Client Credentials for a user-driven calendar app and a user-independent scheduled job.

## Common Misconceptions
- OAuth alone is not a complete user-authentication protocol; OIDC provides the identity layer.
- An authorization code is not an access token.
- An access token is not necessarily a JWT.
- An ID token and an access token are not interchangeable.
- Client Credentials is not limited to a literal password or shared secret.
- A valid token does not remove the need for authorization checks in the API.

## Summary
OAuth enables scoped delegated access through an authorization server and access tokens. Authorization Code with PKCE is a standard choice for user-facing applications. Client Credentials supports application-to-application access when no user delegation is involved. OIDC should be used when the client needs an authentication and identity layer.

## Key Takeaways
- OAuth is mainly about delegated authorization.
- PKCE protects authorization-code redemption.
- Access tokens are for protected APIs; OIDC ID tokens carry identity claims to the client.
- Client Credentials represents the client's own authority, not a user's delegated authority.
- APIs must validate tokens and enforce least-privilege, resource-level authorization.

## Reflection Questions
1. Why is an access token not automatically proof of a user's identity?
2. When would you choose Client Credentials instead of Authorization Code with PKCE?
3. Why must a resource server validate the token's audience?
4. Why is PKCE useful even when a redirect URI is registered?
5. Why are client credentials and access tokens separate credentials?

## What's Next
Lesson 86 — API Gateway Fundamentals: how a gateway provides a controlled entry point for API traffic, routing, policy enforcement, and operational visibility.
