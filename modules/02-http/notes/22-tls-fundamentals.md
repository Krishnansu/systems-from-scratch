# TLS Fundamentals

TLS (Transport Layer Security) provides security for application protocols such as HTTP.

## What TLS Provides

TLS provides three major security properties:

- **Confidentiality** — attackers should not be able to read application data.
- **Integrity** — attackers should not be able to silently modify application data.
- **Authentication** — the client can verify the identity of the server.

## HTTPS Layering

HTTPS is HTTP carried through TLS over a transport such as TCP:

```text
HTTP
  |
  v
TLS
  |
  v
TCP
  |
  v
IP
  |
  v
Network
```

HTTP remains an application protocol. TLS provides the secure channel underneath it.

## Symmetric Encryption

Symmetric encryption uses the same secret key for encryption and decryption.

```text
Plaintext
   |
   | Secret Key
   v
Encrypt
   |
   v
Ciphertext
   |
   | Secret Key
   v
Decrypt
   |
   v
Plaintext
```

Symmetric encryption is efficient and is therefore used for bulk application traffic after the TLS handshake establishes the required keys.

## Asymmetric Cryptography

Asymmetric cryptography uses a key pair:

- Public key — can be distributed.
- Private key — must remain secret.

TLS uses asymmetric cryptography and key agreement during connection establishment rather than using expensive public-key operations for all application data.

## Certificates

A TLS certificate binds a server identity to a public key.

A certificate conceptually contains:

- Domain identity
- Public key
- Validity information
- Issuer
- Certificate Authority signature

The browser validates the certificate before trusting the server identity.

## Certificate Authorities

Certificate Authorities (CAs) establish a chain of trust.

```text
Root CA
   |
   v
Intermediate CA
   |
   v
Server Certificate
   |
   v
example.com
```

The browser/operating system maintains trusted root certificates and uses them to validate certificate chains.

## Digital Signatures

The server proves possession of the private key corresponding to the authenticated public key by producing a digital signature over handshake information.

The client verifies the signature using the public key.

## Key Exchange

Modern TLS 1.3 normally uses ephemeral Diffie-Hellman key exchange, commonly ECDHE.

Both endpoints exchange public key material and independently derive a shared secret without sending the shared secret directly over the network.

## Forward Secrecy

Ephemeral key pairs are generated for individual connections. Compromise of a server's long-term identity private key therefore does not automatically reveal previously recorded session traffic.

## High-Level TLS Flow

```text
TCP Connection
      |
      v
TLS Handshake
      |
      +-- Negotiate parameters
      +-- Authenticate server
      +-- Perform key exchange
      +-- Derive traffic keys
      |
      v
Secure TLS Connection
      |
      v
HTTP Application Data
```

## Important Distinction

```text
Certificate
    -> Who is the server?

ECDHE / Key Exchange
    -> How do both sides establish shared secrets?

Symmetric Encryption
    -> How is application data protected efficiently?
```

## HTTPS Request Flow

```text
Browser
   |
   v
DNS
   |
   v
TCP Handshake
   |
   v
TLS Handshake
   |
   v
Secure TLS Connection
   |
   v
HTTP Request
   |
   v
TLS Encryption
   |
   v
TCP
   |
   v
IP
   |
   v
Network
```
