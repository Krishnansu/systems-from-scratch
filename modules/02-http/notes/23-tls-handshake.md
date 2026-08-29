# TLS 1.3 Handshake

TLS 1.3 establishes the cryptographic state required to securely exchange application data.

## High-Level Handshake

```text
Browser                              Server
   |                                    |
   |------ ClientHello ---------------->|
   |                                    |
   |<----- ServerHello -----------------|
   |<----- Certificate -----------------|
   |<----- CertificateVerify -----------|
   |                                    |
   |   Certificate validation           |
   |   Key agreement                    |
   |   Traffic key derivation           |
   |                                    |
   |====== Encrypted Traffic ===========|
```

The exact TLS 1.3 handshake contains additional messages and can vary depending on the connection/resumption path. The diagram represents the core concepts.

## ClientHello

The browser sends a ClientHello containing information such as:

- Supported TLS versions
- Supported cipher suites
- Random data
- Server Name Indication (SNI)
- Supported extensions
- Key-share information for key exchange

SNI allows the client to indicate the hostname it wants to communicate with.

## ServerHello

The server selects compatible cryptographic parameters and sends its own key-share information.

## Ephemeral Key Exchange

TLS 1.3 commonly uses ECDHE.

```text
Browser                         Server

Private A                       Private B
Public A  -------------------->
          <-------------------- Public B

       Calculate Shared Secret
          independently

Browser result = Server result
```

The shared secret itself is never transmitted directly.

## Certificate and Authentication

The server provides a certificate containing its authenticated public key.

The browser checks:

- Domain identity
- Certificate validity period
- Certificate chain
- Trusted issuer
- Certificate signatures
- Appropriate certificate usage

The server also uses CertificateVerify to prove possession of the private key corresponding to the certificate.

## Transcript Authentication

TLS maintains a transcript of handshake messages. Authentication is tied to the handshake transcript so that an attacker cannot freely modify handshake parameters without detection.

## Key Schedule

The shared secret is processed through the TLS 1.3 key schedule, using HKDF, to derive traffic secrets and keys.

```text
ECDHE Shared Secret
        |
        v
       HKDF
        |
        v
   TLS Key Schedule
        |
        +------------------+
        |                  |
        v                  v
Client Traffic Key   Server Traffic Key
```

The actual TLS 1.3 key schedule contains several intermediate secrets; the diagram is intentionally simplified.

## TLS Records

Application data is carried inside TLS records.

```text
HTTP Data
    |
    v
TLS Record Layer
    |
    v
Encrypt + Authenticate
    |
    v
Encrypted TLS Record
    |
    v
TCP
```

TLS uses authenticated encryption so that confidentiality and integrity are provided together.

## What TCP Sees

TCP does not know that the bytes contain HTTP.

```text
HTTP Request
     |
     v
TLS Encryption
     |
     v
Encrypted TLS Record
     |
     v
TCP Byte Stream
```

## What the Server Sees

```text
Network
   |
   v
IP
   |
   v
TCP
   |
   v
TLS
   |
   | Decrypt + Authenticate
   v
HTTP
   |
   v
Application
```

## TLS 1.3 and 1-RTT

A normal new TLS 1.3 handshake can establish the required cryptographic state with approximately one network round trip before normal application data is exchanged.

TLS 1.3 also supports 0-RTT early data for eligible resumed connections, but this introduces replay considerations and should not be treated as equivalent to normal 1-RTT application data.

## Complete HTTPS Mental Model

```text
DNS
 |
 v
TCP Three-Way Handshake
 |
 v
TLS 1.3 Handshake
 |
 +-- ClientHello
 +-- ServerHello
 +-- Certificate
 +-- Authentication
 +-- Key Exchange
 +-- Key Derivation
 |
 v
Encrypted TLS Connection
 |
 v
HTTP Request / Response
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
