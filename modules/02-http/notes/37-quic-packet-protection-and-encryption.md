# Lesson 37 - QUIC Packet Protection & Encryption

## Objectives

- Understand how QUIC protects packet payloads using AEAD.
- Understand the difference between payload encryption and QUIC header protection.
- Understand confidentiality, integrity and authentication in QUIC.
- Understand the role of the traffic key, IV and header-protection key.
- Understand how the packet number contributes to the AEAD nonce.
- Understand packet number truncation and high-level reconstruction.
- Understand how TLS 1.3-derived secrets become QUIC packet-protection material.
- Understand the high-level send and receive paths for a protected QUIC packet.

## Prerequisites

- Lesson 34 - QUIC Fundamentals
- Lesson 35 - QUIC Packets, Frames & Connection IDs
- Lesson 36 - QUIC Connection Establishment & TLS 1.3

## Theory

QUIC protects packets using two related but distinct mechanisms:

```text
QUIC Packet
    |
    +-------------------------+
    |                         |
    v                         v
Payload protection       Header protection
    |                         |
    v                         v
   AEAD                 Masks selected bits
```

Payload protection provides confidentiality and integrity for the packet payload. Header protection masks selected header bits, including the packet number bytes.

QUIC derives the required cryptographic material from TLS 1.3 secrets. The high-level relationship is:

```text
TLS 1.3 traffic secret
          |
          v
   QUIC key derivation
          |
     +----+----+
     |    |    |
     v    v    v
    Key   IV  HP Key
```

## Real World Example

Suppose an HTTP/3 client sends:

```text
GET /users HTTP/3
```

The application data becomes a QUIC STREAM frame, which becomes part of a QUIC packet payload. QUIC then protects the payload using AEAD and applies header protection.

```text
HTTP/3 request
      |
      v
STREAM frame
      |
      v
QUIC packet payload
      |
      v
AEAD protection
      |
      v
Ciphertext + authentication tag
      |
      v
Header protection
      |
      v
Protected QUIC packet
      |
      v
UDP datagram
```

A passive observer can still see network metadata such as IP addresses, UDP ports, packet timing and packet sizes, but cannot simply read the protected HTTP/3 payload.

## Deep Dive

### 1. What Does QUIC Need to Protect?

QUIC needs to provide:

- Confidentiality - attackers should not be able to read protected application data.
- Integrity - attackers should not be able to modify protected data without detection.
- Authentication - the receiver should be able to detect packets that were not produced using the correct cryptographic keys.

These properties are provided primarily by authenticated encryption for the payload, combined with header protection for selected header fields.

### 2. AEAD

AEAD means **Authenticated Encryption with Associated Data**.

Conceptually:

```text
Plaintext
   +
   + Key
   +
   + Associated Data
   |
   v
 AEAD
   |
   v
Ciphertext + Authentication Tag
```

On reception:

```text
Ciphertext + Authentication Tag
             +
            Key
             +
     Associated Data
             |
             v
            AEAD
             |
       +-----+-----+
       |           |
       v           v
   success       failure
       |           |
       v           v
   plaintext   reject packet
```

The authentication tag allows the receiver to detect modifications.

### 3. Associated Data

AEAD can authenticate data without encrypting it. This is called Associated Data (AD).

Conceptually:

```text
             QUIC packet
                  |
        +---------+---------+
        |                   |
        v                   v
 Associated Data        Payload
        |                   |
        |                   v
        |              Encryption
        |                   |
        +---------+---------+
                  |
                  v
                 AEAD
```

The associated data is authenticated as part of the AEAD operation even though it is not encrypted as ciphertext.

### 4. Payload Protection vs Header Protection

These must not be confused.

```text
Payload protection
    |
    +-- AEAD
    +-- Encrypts payload
    +-- Produces authentication tag
    +-- Provides confidentiality + integrity

Header protection
    |
    +-- Uses a separate header-protection key
    +-- Generates a mask
    +-- Masks selected bits of the first byte
    +-- Masks packet-number bytes
```

Header protection is not simply another application of payload AEAD.

### 5. QUIC Packet Structure

A simplified conceptual packet looks like:

```text
+------------------------------------------------+
| QUIC Header                                    |
+------------------------------------------------+
| Packet Number                                  |
+------------------------------------------------+
| QUIC Frames / Payload                          |
+------------------------------------------------+
| Authentication Tag                             |
+------------------------------------------------+
```

The exact fields differ between QUIC packet types, but the model is useful for understanding protection.

### 6. TLS Supplies the Cryptographic Secrets

Lesson 36 established that TLS 1.3 is integrated into QUIC.

TLS produces traffic secrets, from which QUIC derives packet-protection material.

```text
TLS 1.3
   |
   v
Traffic Secret
   |
   +-------------------+
   |                   |
   v                   v
QUIC key derivation   Header-protection derivation
   |                   |
   +----+----+         +----+
        |    |              |
        v    v              v
       Key   IV           HP Key
```

Different QUIC encryption levels have different packet-protection keys.

```text
Initial
   -> Initial packet-protection material

Handshake
   -> Handshake packet-protection material

1-RTT
   -> Application packet-protection material
```

### 7. The IV

IV stands for **Initialization Vector**.

In QUIC, the IV is cryptographically derived key material used as the base for constructing the AEAD nonce for each packet.

The high-level relationship is:

```text
IV
+
Packet Number
|
v
Nonce
|
v
AEAD
```

The IV is not normally transmitted separately with every packet. Both endpoints derive the necessary IV from their cryptographic state.

### 8. Nonce Construction

AEAD requires a nonce for each encryption operation.

QUIC derives a packet-specific nonce from the packet number and the IV. Conceptually:

```text
Packet Number
      |
      v
Encoded packet number
      |
      +---------+
                |
IV ------------> XOR
                |
                v
              Nonce
                |
                v
               AEAD
```

The actual construction uses the packet number encoded in the required length and combines it with the IV using XOR.

The important mental model is:

> The IV is the base cryptographic value, while the packet number makes the nonce packet-specific.

### 9. Why the Nonce Must Be Packet-Specific

AEAD schemes require careful nonce usage. Reusing the same nonce with the same key can seriously weaken or break the security guarantees of the construction.

QUIC therefore derives different nonces for different packet numbers.

```text
Same traffic key
       |
       +-----------------------------+
       |             |               |
       v             v               v
   PN = 1         PN = 2          PN = 3
       |             |               |
       v             v               v
   Nonce A        Nonce B         Nonce C
```

### 10. Packet Number Truncation

QUIC does not always send the full packet number. It can encode only the required number of low-order bytes.

Conceptually:

```text
Full packet number
0x0000001234

Transmitted packet number
0x34
```

The receiver uses previously received packet numbers to reconstruct the most likely full packet number.

```text
Largest received packet number
             |
             v
     Truncated PN received
             |
             v
   Candidate full numbers
             |
             v
   Choose valid closest value
```

The exact reconstruction algorithm has specific rules; the key idea is that packet numbers are transmitted compactly while the receiver maintains enough state to recover the full value.

### 11. Why Protect Packet Numbers?

Packet numbers are important transport metadata used for:

- ACK processing
- Loss detection
- RTT measurement
- Duplicate detection
- Packet ordering analysis

QUIC applies header protection to the packet-number bytes so that they are not simply exposed in plaintext.

### 12. Header Protection

Header protection uses a separate header-protection key and a sample from the packet ciphertext to generate a mask.

Conceptually:

```text
Ciphertext sample
       +
Header Protection Key
       |
       v
Mask generation
       |
       v
Mask selected header bits
       |
       +-------------------+
       |                   |
       v                   v
First-byte bits       Packet-number bytes
```

The first byte and packet number are therefore protected differently from the payload.

### 13. Why Is the Ciphertext Sample Used?

The sender can generate the header-protection mask from bytes in the packet ciphertext.

The receiver can locate the corresponding sample and independently generate the same mask once it has enough information to process the packet.

Conceptually:

```text
Sender

Encrypt payload
     |
     v
Ciphertext
     |
     v
Take sample
     |
     v
Generate mask
     |
     v
Protect header
```

And the receiver reverses the operation:

```text
Protected packet
      |
      v
Locate ciphertext sample
      |
      v
Generate same mask
      |
      v
Remove header protection
      |
      v
Recover packet number
```

### 14. Sender Pipeline

The high-level sender path is:

```text
HTTP/3 data
      |
      v
QUIC STREAM frame
      |
      v
QUIC packet payload
      |
      v
AEAD encryption
      |
      v
Ciphertext + authentication tag
      |
      v
Header protection
      |
      v
Protected QUIC packet
      |
      v
UDP
```

### 15. Receiver Pipeline

The receiver roughly performs:

```text
UDP datagram
      |
      v
QUIC packet
      |
      v
Locate ciphertext sample
      |
      v
Remove header protection
      |
      v
Recover packet number
      |
      v
Construct AEAD nonce
      |
      v
AEAD authenticate + decrypt
      |
      v
QUIC frames
      |
      v
HTTP/3
```

The important ordering is that the packet number is needed for nonce construction, so header protection is removed before payload decryption.

### 16. What Happens If an Attacker Modifies the Payload?

Suppose the sender transmits:

```text
STREAM frame
GET /home
```

An attacker modifies the protected packet in transit.

```text
Modified ciphertext
       |
       v
AEAD verification
       |
       v
Authentication failure
       |
       v
Packet rejected
```

The attacker cannot simply modify ciphertext and expect the receiver to accept the resulting plaintext.

### 17. Why Protect ACK Frames?

ACK frames influence transport behavior.

If attackers could forge ACK information, they could potentially interfere with:

- loss detection
- RTT estimation
- congestion control

QUIC therefore protects ACK frames as part of the packet payload.

```text
ACK frame
   |
   v
QUIC packet payload
   |
   v
AEAD protection
   |
   v
Authenticated transport signal
```

### 18. Packet Number Spaces

As discussed in Lesson 36, QUIC maintains separate packet number spaces for different packet types.

```text
QUIC connection
      |
      +----------------+----------------+----------------+
      |                |                |
      v                v                v
Initial space     Handshake space   Application space
      |                |                |
      v                v                v
Initial PN        Handshake PN       1-RTT PN
```

Packet protection keys and packet number processing are associated with the relevant encryption level and packet number space.

### 19. What a Passive Observer Can Still See

QUIC does not make network traffic completely invisible.

An observer may still see:

- source and destination IP addresses
- UDP ports
- packet timing
- packet sizes
- some unprotected packet metadata
- Connection IDs where applicable

But protected application payload is not exposed as plaintext.

```text
Visible metadata
       |
       +-- IP addresses
       +-- UDP ports
       +-- timing
       +-- sizes

Protected content
       |
       +-- HTTP/3 payload
       +-- protected QUIC frames
       +-- selected header fields
```

### 20. Complete Mental Model

```text
                    TLS 1.3
                       |
                       v
                Traffic Secret
                       |
                QUIC key derivation
                       |
            +----------+----------+
            |          |          |
            v          v          v
           Key         IV       HP Key
            |          |          |
            |          |          +----------------+
            |          |                           |
            |          v                           v
            |     Packet Number               Ciphertext sample
            |          |                           |
            |          v                           |
            |        Nonce                         |
            |          |                           |
            +----------+                           |
                       |                            |
                       v                            v
                  AEAD payload             Header protection
                       |                            |
                       v                            v
                  Ciphertext                 Protected header
                       \                            /
                        +-----------+--------------+
                                    |
                                    v
                              QUIC packet
```

## Hands-on Exercise

Consider this simplified QUIC packet:

```text
+------------------------------------------------+
| QUIC Header                                    |
+------------------------------------------------+
| Packet Number                                  |
+------------------------------------------------+
| STREAM frame                                   |
|     GET /users HTTP/3                          |
+------------------------------------------------+
| Authentication Tag                             |
+------------------------------------------------+
```

Answer:

1. Which part is protected using AEAD?
2. Which parts are affected by header protection?
3. Where does the AEAD key come from?
4. What is the purpose of the IV?
5. How is the per-packet nonce constructed at a high level?
6. Why can QUIC transmit a truncated packet number?
7. What does the receiver need to do before it can construct the AEAD nonce?
8. What happens if an attacker modifies the ciphertext?
9. Why are ACK frames protected?
10. Can a passive observer still see the packet's IP addresses and size?

## Common Misconceptions

### "QUIC encrypts the entire packet."

Not exactly. QUIC protects the packet payload using AEAD and applies header protection to selected header bits. Some packet metadata remains visible.

### "Header protection and payload encryption are the same thing."

No. Payload protection uses AEAD. Header protection uses a separate mechanism and header-protection key to mask selected fields.

### "The IV is sent with every packet."

No. The IV is derived cryptographic material known to the endpoints. It is used with the packet number to construct the per-packet nonce.

### "The packet number is completely encrypted."

Not exactly. QUIC applies header protection to the packet-number bytes rather than encrypting them as part of the payload.

### "TLS directly encrypts every QUIC packet."

TLS 1.3 establishes the cryptographic secrets. QUIC uses derived key material for its packet-protection operations.

### "UDP provides the encryption."

No. UDP provides datagram transport. QUIC provides packet protection using TLS-derived cryptographic material.

### "Every QUIC frame is encrypted independently."

No. Frames form the packet payload, which is protected as part of the QUIC packet.

### "Encryption alone guarantees that ACKs cannot be forged."

The important property is authenticated encryption. Integrity/authentication prevents an attacker from modifying protected ACK information without detection.

## Summary

QUIC uses TLS 1.3-derived cryptographic material to protect packets. The payload is protected using AEAD, which provides confidentiality and integrity. QUIC also applies header protection to selected header bits, including the packet number bytes.

The packet-protection key, IV and header-protection key are derived from the relevant QUIC/TLS cryptographic state. The IV is combined with the packet number to construct the per-packet AEAD nonce. QUIC can transmit truncated packet numbers to reduce overhead, with the receiver reconstructing the full value using connection state.

The sender encrypts the QUIC payload, generates the header-protection mask and sends the protected packet over UDP. The receiver removes header protection, reconstructs the packet number, constructs the nonce and then authenticates and decrypts the payload.

## Key Takeaways

1. QUIC payload protection uses AEAD.
2. AEAD provides confidentiality and integrity/authentication.
3. Header protection is separate from payload encryption.
4. Header protection masks selected first-byte bits and packet-number bytes.
5. TLS 1.3 provides the cryptographic secrets from which QUIC derives packet-protection material.
6. QUIC derives a packet-protection key, IV and header-protection key for the relevant encryption level.
7. The IV is a base cryptographic value used with the packet number to construct the AEAD nonce.
8. The packet number makes the nonce packet-specific.
9. QUIC can transmit truncated packet numbers and reconstruct them at the receiver.
10. The receiver removes header protection before constructing the AEAD nonce and decrypting the payload.
11. ACK frames are protected because forged transport signals could disrupt QUIC's transport behavior.
12. QUIC encryption protects content but does not hide all network metadata.

## Reflection Questions

1. Why does QUIC need both AEAD payload protection and header protection?
2. What security properties does AEAD provide?
3. What is the difference between an IV and a nonce?
4. Why is the packet number involved in nonce construction?
5. Why is nonce reuse dangerous for AEAD encryption?
6. Why can QUIC transmit only part of a packet number?
7. How does the receiver recover the full packet number?
8. Why does QUIC protect packet numbers instead of simply leaving them visible?
9. Why are ACK frames included in authenticated packet payloads?
10. What cryptographic material does TLS provide to QUIC?
11. Why does the receiver remove header protection before decrypting the payload?
12. What network information can remain visible even when QUIC payloads are encrypted?

## What's Next

### Lesson 38 - QUIC Header Protection & Packet Numbers

Next we will go deeper into the two mechanisms introduced here:

```text
Ciphertext sample
       +
Header Protection Key
       |
       v
Mask generation
       |
       v
Header protection
```

and:

```text
Truncated packet number
       |
       v
Packet number reconstruction
       |
       v
Full packet number
```

We will reason through the packet-number reconstruction process with concrete examples and examine exactly how header protection is removed at the receiver.
