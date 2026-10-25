# Lesson 129 — Public/Private Keys, Certificates, Trust & Validation

## Objectives

- Explain public/private key pairs and digital signatures.
- Understand what a certificate contains and why it is signed by a CA.
- Trace certificate issuance from key generation through delivery.
- Explain trust anchors, certificate chains, and certificate validation.
- Distinguish CA signature verification, proof of private-key possession, authentication, and authorization.
- Trace how certificates are used in TLS/mTLS and an Istio service mesh.

## Prerequisites

- TLS fundamentals and the TLS handshake.
- Lessons 127–128: Istio and mTLS.

## Concept Summary

A public/private key pair enables cryptographic operations. A certificate binds an identity to a public key and is digitally signed by a certificate authority (CA). A receiver validates the certificate using its configured trust anchors and validation rules. During TLS, the peer also proves possession of the corresponding private key. mTLS performs peer authentication in both directions. Authorization separately determines what an authenticated identity may access.

## Core Ideas

- **Public key:** Shareable key used for operations such as verifying signatures or participating in public-key cryptography.
- **Private key:** Secret key protected by its owner or authorized key-management component. It may be used to sign data or participate in cryptographic protocols; it is not sent with the certificate.
- **Digital signature:** Cryptographic evidence that signed content has not been altered and that the signature was produced using the corresponding private key.
- **Certificate:** Structured, signed data binding an identity and public key, with validity information and other fields governing its use.
- **Certificate authority (CA):** An authority that issues certificates after applying its identity-verification and authorization policies, then signs them with its CA signing private key.
- **Certificate Signing Request (CSR):** A request commonly containing a public key and requested identity information, signed with the corresponding private key. A CSR alone does not establish that the requester is entitled to the identity.
- **Trust anchor:** A CA or public key explicitly trusted by the receiver. A self-signed root is not trusted merely because it is self-signed; trust comes from configuration or another trusted mechanism.
- **Certificate chain:** A leaf certificate may be signed by an intermediate CA, which chains to a trusted root. The chain must validate under the receiver's trust configuration.
- **Proof of private-key possession:** During the TLS handshake, the peer demonstrates possession of the private key corresponding to its certificate's public key. Exact handshake messages depend on TLS version and configuration.
- **Certificate validation:** Typically checks the chain and signatures, validity dates, identity, intended use, and relevant policy. Revocation checking varies by environment.
- **Authentication:** Establishes who the peer is under the configured trust and identity rules.
- **Authorization:** Determines what an authenticated identity is allowed to do.

## Certificate Issuance Flow

1. The workload or its authorized key-management component generates a key pair.
2. The requester creates a CSR containing its public key and requested identity information.
3. The CA verifies the requester's identity and authorization according to its policy.
4. The CA issues and signs a certificate using the CA's signing private key.
5. The requester receives the certificate and keeps its own private key protected.

The workload's private key and the CA's private signing key are different keys with different responsibilities. The CA does not need the workload's private key to sign its certificate.

## Validation and TLS Flow

```text
Inventory creates or receives a key pair
  → CA verifies identity/authorization and signs certificate
  → Inventory receives certificate; private key remains protected
  → Checkout receives Inventory's certificate during TLS
  → Checkout validates chain, identity, validity, and policy
  → Inventory proves possession of its private key in the handshake
  → TLS establishes shared session keys
  → Application/mesh authorization determines permitted access
```

In TLS with server authentication, the client validates the server. In mTLS, both peers authenticate each other using certificates and proof of private-key possession. The private keys are not exchanged. TLS derives session keys for protecting traffic; certificate signatures and handshake proofs serve different purposes.

## Who Makes the Decision?

- The receiver's TLS implementation validates the peer certificate against its configured trust information and rules. It does not normally ask the CA to approve every live connection.
- A CA controls certificate issuance according to its identity and authorization policies; its signature does not grant access to every resource.
- In a typical Istio deployment, Istio's CA functionality issues workload credentials, while Envoy proxies use configured certificates, trust information, and policies to handle live mTLS connections.
- Istiod coordinates configuration and credential distribution; it is not normally in the live request path.
- Istio authorization policies and application-level access controls make separate access decisions after identity has been established.

## Real-World Example

Checkout connects to Inventory through Envoy proxies. Inventory's inbound proxy presents its certificate. Checkout's outbound proxy validates the certificate against its trust configuration and verifies Inventory's proof of private-key possession. In mTLS, Inventory's proxy also authenticates Checkout. If authentication succeeds, authorization policy still determines whether Checkout may perform the requested operation.

## Production Perspective

- A valid certificate does not guarantee a successful connection: trust, identity, validity, TLS compatibility, routing, or other checks can still fail.
- A valid certificate does not prove that the current peer possesses its private key; the handshake must establish possession.
- A valid signature from an untrusted CA is not sufficient for trust.
- A trusted certificate establishes identity only within the applicable validation rules; it does not automatically grant authorization.
- Protect private keys, manage certificate expiry and rotation, and investigate trust or identity failures before changing security policies.

## Common Misconceptions

- A certificate is not a private key; it contains the public key and signed identity information.
- The workload's private key and the CA's signing private key are not interchangeable.
- A CA signature does not, by itself, prove that the current peer possesses the corresponding private key.
- A root certificate is not trusted merely because it is self-signed.
- Authentication, encryption, and authorization are distinct properties.
- The CA does not usually participate in every live TLS handshake decision.
- Successful mTLS does not guarantee that the application request will succeed.

## Key Takeaways

- A certificate binds an identity to a public key under a CA's signature.
- The receiver's configured trust anchors and validation rules determine whether to accept the certificate.
- TLS verifies peer key possession and establishes session keys without exchanging private keys.
- mTLS authenticates both peers; authorization separately controls access.
- In a service mesh, proxies commonly handle workload certificates and live TLS validation while the control plane manages configuration and credentials.

## Reflection Questions

1. Why does a certificate contain a public key but not its corresponding private key?
2. Who generates a workload key pair, who signs its certificate, and what must the CA verify?
3. Why is a mathematically valid certificate signature not sufficient if the CA is not trusted?
4. What is the difference between validating a CA's signature and proving that the peer possesses its private key?
5. In Istio, which components issue/distribute credentials, validate live connections, and enforce authorization?
6. Why can a successfully authenticated workload still receive an authorization denial?

## What's Next

Module 09 — Database Fundamentals.
