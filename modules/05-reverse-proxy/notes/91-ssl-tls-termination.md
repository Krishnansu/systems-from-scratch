# Lesson 91 — SSL/TLS Termination

## Objectives
- Explain TLS termination at a reverse proxy.
- Compare termination, re-encryption, and TLS passthrough.
- Understand certificates, private keys, SNI, and trusted forwarding headers.
- Identify production TLS configuration and certificate lifecycle risks.

## Prerequisites
- TLS and HTTPS fundamentals
- Lesson 88 — Reverse Proxy Fundamentals
- Lesson 89 — NGINX Fundamentals

## Theory
TLS termination occurs when a TLS connection ends at an intermediary such as NGINX. The proxy decrypts client traffic and can inspect HTTP requests before forwarding them to a backend.

```text
Browser -- HTTPS/TLS --> Proxy -- HTTP or HTTPS --> Backend
```

The client-to-proxy connection and proxy-to-backend connection are separate connections. Encryption on one hop does not automatically encrypt the next.

## Real World Example
A store serves `shop.example.com` over HTTPS at NGINX and forwards requests to an application on port 3000. NGINX presents the public certificate and terminates client TLS. The upstream hop may use HTTP on a suitably protected host/network or HTTPS when the internal trust boundary requires encryption.

## Deep Dive
- **TLS termination:** The proxy decrypts client traffic and can perform HTTP-aware routing, load balancing, and policy enforcement.
- **TLS re-encryption:** The proxy terminates client TLS and establishes a separate TLS session to the backend. Configure upstream certificate-chain and hostname verification; HTTPS alone is not sufficient.
- **TLS passthrough:** The proxy forwards encrypted TLS traffic without decrypting HTTP. It generally cannot route by HTTP path, though it may use SNI or connection-level information.
- Certificates authenticate the server during TLS setup; symmetric traffic keys protect connection data. The private key must be protected.
- SNI can help select a certificate during the TLS handshake. HTTP `Host` is available after the HTTP request is decrypted; these are distinct routing stages.
- `X-Forwarded-Proto` can communicate the original client scheme after termination. Forwarding headers must be overwritten or sanitized and trusted only from known proxies.
- mTLS allows both sides of a TLS connection to authenticate. It does not replace application-level authorization.
- Certificate lifecycle management includes issuance, renewal, deployment, reload, expiry monitoring, and consistency across proxy instances.
- Common failures include expired or mismatched certificates, incomplete trust chains, incorrect SNI, upstream verification errors, and configuration drift.

## Hands-on Exercise
1. Identify which hops are encrypted when a browser uses HTTPS but the proxy forwards HTTP.
2. Decide when the upstream hop should use HTTPS.
3. Explain why upstream certificate and hostname verification matter.
4. Explain how trusted forwarding headers help an application understand the original request scheme.
5. Describe the risks of renewing a certificate on only one proxy instance.

## Common Misconceptions
- HTTPS at the public edge does not mean every internal hop is encrypted.
- A certificate is not the symmetric key used for all application data.
- Private IP addresses do not provide encryption by themselves.
- Enabling HTTPS upstream without verification does not reliably authenticate the backend.
- Trusted forwarding headers are not safe if untrusted clients can spoof them.
- mTLS authenticates a connection peer but does not grant unrestricted access to application resources.

## Summary
TLS termination centralizes client-facing TLS and enables HTTP-aware proxy features. The upstream connection may use plaintext HTTP, a separate verified TLS session, or TLS passthrough to a backend that terminates the original client connection. Production systems must protect private keys, verify upstream identities, trust forwarding headers carefully, and maintain consistent certificate deployment and renewal.

## Key Takeaways
- TLS protection applies to a particular connection between endpoints.
- Termination and re-encryption use separate TLS sessions.
- Upstream HTTPS requires appropriate certificate and hostname verification.
- Forwarding headers must be trusted only across controlled proxy boundaries.
- Certificate lifecycle and configuration consistency are production responsibilities.

## Reflection Questions
1. Why can a proxy route by HTTP path after TLS termination but not normally during TLS passthrough?
2. How do TLS termination and re-encryption differ?
3. Why is upstream certificate verification important?
4. Why should an application not blindly trust forwarding headers?
5. How would you investigate inconsistent certificate behavior across proxy instances?

## What's Next
Lesson 92 — Routing Fundamentals: host-based and path-based routing, rule ordering, and backend selection.
