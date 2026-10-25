# Lesson 128 — Mutual TLS (mTLS)

## Objectives

- Explain TLS versus mutual TLS.
- Understand certificates, trust, and workload identity.
- Distinguish encryption, authentication, and authorization.
- Describe Istio PeerAuthentication and DestinationRule TLS behavior.
- Diagnose common mTLS failures safely.

## Prerequisites

- Lessons 125–127: Envoy, Service Mesh, Istio.
- TLS, certificates, trust chains, and Kubernetes workloads.

## Concept Summary

TLS protects communication and commonly authenticates the server. Mutual TLS (mTLS) authenticates both peers using certificates. In a sidecar-based service mesh, proxies can establish mTLS for application-to-application traffic. Authentication does not itself authorize an operation.

## Core Ideas

- **Encryption:** protects data in transit.
- **Authentication:** establishes peer identity according to certificate and trust rules.
- **Authorization:** decides whether an identity can access a resource or perform an operation.
- **Certificate:** binds identity information to a public key; the corresponding private key must remain protected.
- **CA and trust bundle:** support certificate-chain validation.
- **Workload identity:** represents the communicating workload under the configured identity system.
- **Certificate rotation:** replaces credentials before expiry or when required by policy.
- **PeerAuthentication:** configures inbound peer-authentication behavior, including mTLS mode.
- **DestinationRule:** can configure client-side TLS behavior for a destination; `ISTIO_MUTUAL` is used in applicable Istio-managed mTLS configurations.

## Conceptual Request Flow

```text
Checkout app
  → checkout Envoy
  → encrypted mTLS connection
  → inventory Envoy
  → inventory app
```

Both proxies authenticate their peers according to the active TLS configuration and trust. Exact traffic paths depend on the Istio deployment mode and configuration.

## Common Inbound Modes

- `STRICT`: requires mTLS for applicable inbound traffic.
- `PERMISSIVE`: can accept mTLS and plaintext, subject to configuration.
- `DISABLE`: disables Istio's inbound mTLS requirement for the applicable scope.

Policy scope, precedence, defaults, and client-side configuration matter. Do not assume all clusters behave identically.

## Production Perspective

- Valid certificates do not guarantee successful connectivity or authorization.
- A TLS failure may result from mode mismatch, trust or identity validation, certificate validity, proxy configuration, or other handshake issues.
- Establish the incident scope and first failing hop before changing policies.
- Inspect authorized proxy diagnostics and logs; treat certificate and proxy output as sensitive.
- Follow incident procedures before modifying security policy, restarting workloads, or weakening transport security.

## Common Misconceptions

- mTLS does not automatically authorize requests.
- Private networking does not establish workload identity.
- `STRICT` does not guarantee application security or correct authorization.
- PeerAuthentication and DestinationRule have different responsibilities.
- Proxy health does not prove end-to-end application health.

## Key Takeaways

- mTLS authenticates both peers and protects the connection.
- Certificates, trust, and workload identity are central to authentication.
- Encryption, authentication, and authorization are separate properties.
- Diagnose mode, trust, certificate, configuration, and path issues using evidence.

## Reflection Questions

1. What assurance does mTLS add over server-authenticated TLS?
2. Why can valid certificates still result in a failed connection?
3. How do PeerAuthentication and DestinationRule differ?
4. Why does successful mTLS not automatically permit a request?
5. What would you inspect after a STRICT policy change breaks legacy clients?

## What's Next

Module 09 — Database Fundamentals.
