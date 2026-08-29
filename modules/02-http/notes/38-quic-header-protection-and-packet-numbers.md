# Lesson 38 - QUIC Header Protection & Packet Numbers

## Objectives

- Understand why QUIC uses packet numbers.
- Understand QUIC packet-number spaces.
- Understand what header protection protects.
- Understand the difference between header protection and AEAD payload protection.
- Understand how QUIC generates a header-protection mask at a high level.
- Understand packet-number truncation.
- Understand packet-number reconstruction.
- Understand how the packet number participates in AEAD nonce construction.

## Prerequisites

- Lesson 35 - QUIC Packets, Frames & Connection IDs
- Lesson 36 - QUIC Connection Establishment & TLS 1.3
- Lesson 37 - QUIC Packet Protection & Encryption

## 1. Why Does QUIC Need Packet Numbers?

Every QUIC packet has a packet number within its packet-number space.

Packet numbers are used for:

- ACK processing
- Loss detection
- RTT measurement
- Duplicate detection
- AEAD nonce construction

A packet number is different from TCP's byte sequence number.

```text
TCP
  |
  v
Sequence Number
  |
  v
Position of bytes in a stream

QUIC
  |
  v
Packet Number
  |
  v
Identifies a QUIC packet
```

## 2. Packet Number Spaces

QUIC maintains separate packet-number spaces for different encryption levels.

```text
QUIC Connection
      |
      +----------------+
      |                |
      v                v
   Initial          Handshake
    space             space
      |                |
      v                v
 Initial PN        Handshake PN

           +
           |
           v
      Application
         space
           |
           v
        1-RTT PN
```

The important point is that packet numbers are not one global counter shared across every QUIC encryption level.

## 3. Why Protect the Packet Number?

Packet numbers are transport metadata, but exposing them directly makes packet progression and other traffic characteristics easier to inspect.

QUIC therefore applies header protection to the packet-number bytes.

Header protection does not encrypt the entire header.

```text
QUIC Header
    |
    +-----------------------+
    |                       |
    v                       v
Selected first-byte bits   Packet-number bytes
          \                  /
           \                /
            +--------------+
                   |
                   v
            Header protection
```

## 4. Header Protection vs Payload Protection

These are separate mechanisms.

```text
Payload
   |
   v
AEAD
   |
   v
Encrypted + authenticated

Header
   |
   v
Header protection
   |
   v
Selected bits masked
```

AEAD provides the main confidentiality and integrity protection for the packet payload. Header protection masks selected header bits.

## 5. How Is the Header-Protection Mask Generated?

QUIC derives a separate header-protection key from its cryptographic state.

A ciphertext sample is used together with this key to generate a mask.

```text
Ciphertext sample
       +
Header Protection Key
       |
       v
Mask generation
       |
       v
     Mask
```

The mask is then applied to selected bits of the first byte and to the packet-number bytes.

The exact cryptographic primitive depends on the negotiated cipher suite. For this lesson, the important concept is the data flow rather than the cryptographic primitive itself.

## 6. Why Use a Ciphertext Sample?

The sender already has ciphertext after protecting the packet payload. A portion of that ciphertext can be used as the sample for header protection.

The receiver can independently locate the same sample and generate the same mask using its copy of the header-protection key.

```text
Sender                         Receiver
  |                               |
  | Ciphertext sample             | Ciphertext sample
  |                               |
  v                               v
HP Key + Sample               HP Key + Sample
  |                               |
  v                               v
Mask                          Same Mask
```

No separate header-protection value has to be transmitted with each packet.

## 7. What Does Header Protection Change?

Conceptually, before protection:

```text
+-----------------------------+
| First byte                  |
+-----------------------------+
| Packet Number               |
+-----------------------------+
| Ciphertext                  |
+-----------------------------+
```

After header protection:

```text
+-----------------------------+
| Protected first byte        |
+-----------------------------+
| Protected Packet Number     |
+-----------------------------+
| Ciphertext                  |
+-----------------------------+
```

The ciphertext is used to generate the mask; header protection does not encrypt the ciphertext itself.

## 8. The Receiver's Problem

The receiver needs the packet number to construct the AEAD nonce.

But the packet number is protected.

```text
Need Packet Number
       |
       v
Construct AEAD Nonce
       |
       v
Decrypt Payload

But...

Packet Number is protected
```

The receiver therefore removes header protection before constructing the AEAD nonce.

## 9. Receiver Processing

The high-level receive path is:

```text
Protected QUIC packet
        |
        v
Locate ciphertext sample
        |
        v
Generate header-protection mask
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
Authenticate + decrypt payload
```

This connects directly to Lesson 37.

## 10. Packet Number Truncation

QUIC does not always transmit the complete packet number.

This saves packet overhead.

For example, conceptually:

```text
Full packet number
123456
      |
      v
Transmit low-order portion
      |
      v
56
```

The transmitted value is not the complete packet number.

## 11. Packet Number Reconstruction

The receiver uses connection state to reconstruct the most likely full packet number.

It knows information such as:

- the largest packet number it has received in the relevant packet-number space
- the number of packet-number bytes that were encoded
- the packet-number reconstruction window

Conceptually:

```text
Largest received PN
        |
        +--------+
                 |
                 v
        Truncated PN received
                 |
                 v
       Candidate full numbers
                 |
                 v
        Select valid candidate
                 |
                 v
         Full packet number
```

The exact arithmetic is specified by QUIC's packet-number decoding rules. For our systems-level understanding, the key idea is that the receiver uses nearby packet-number context rather than guessing arbitrarily.

## 12. Concrete Example

Suppose the sender has:

```text
Full Packet Number = 1057
```

Only a truncated value is transmitted:

```text
Truncated PN = 0x21
```

The receiver previously received:

```text
Largest PN = 1056
```

The receiver removes header protection and obtains the truncated packet number.

It then reconstructs the full value using the packet-number decoding rules:

```text
Largest PN = 1056
Truncated PN = 0x21
        |
        v
Packet-number reconstruction
        |
        v
Full PN = 1057
```

The receiver can then construct the AEAD nonce.

## 13. Packet Number and the AEAD Nonce

From Lesson 37:

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

The packet number therefore connects transport semantics to cryptographic packet protection.

The high-level receiver flow becomes:

```text
Protected Packet
      |
      v
Remove Header Protection
      |
      v
Recover Full Packet Number
      |
      v
IV + Packet Number
      |
      v
AEAD Nonce
      |
      v
Decrypt + Authenticate
```

## 14. Why Header Protection Does Not Replace AEAD

Header protection primarily masks selected header bits.

AEAD provides the packet payload's authenticated encryption.

```text
Header Protection
      |
      v
Mask selected header fields

AEAD
      |
      +--> Confidentiality
      +--> Integrity
      +--> Authentication
```

This distinction is important: masking and authenticated encryption are not the same security mechanism.

## 15. What If an Attacker Modifies the Packet?

An attacker cannot simply change protected packet information and expect the receiver to accept the resulting packet as valid.

The receiver eventually performs AEAD authentication.

```text
Modified Packet
      |
      v
Recover header information
      |
      v
Construct nonce
      |
      v
AEAD verification
      |
      +----------+
      |          |
      v          v
   Success    Failure
      |          |
      v          v
 Process      Reject
 packet       packet
```

## 16. Why This Design Fits QUIC

QUIC packet numbers serve several purposes simultaneously:

```text
                 Packet Number
                       |
        +--------------+--------------+
        |              |              |
        v              v              v
       ACKs       Loss detection   RTT/duplicates
        |
        +--------------+
                       |
                       v
                AEAD nonce input
```

Header protection hides the packet number from being trivially exposed while allowing the endpoint to recover it before payload decryption.

## 17. HTTP/3 Connection

HTTP/3 data eventually becomes QUIC STREAM frames, which are carried inside protected QUIC packets.

```text
HTTP/3
   |
   v
QUIC STREAM frame
   |
   v
QUIC packet
   |
   +------------------+
   |                  |
   v                  v
Header protection   AEAD payload protection
   |                  |
   +--------+---------+
            |
            v
           UDP
```

The HTTP/3 layer does not need to manage packet numbers itself. QUIC handles that transport machinery underneath it.

## Common Misconceptions

### "Header protection encrypts the whole QUIC header."

No. It masks selected bits of the first byte and packet-number bytes.

### "The packet number is part of the encrypted payload."

No. The packet number is in the QUIC header and is protected using QUIC's header-protection mechanism.

### "The packet number is always transmitted in full."

No. QUIC can transmit a truncated packet number to reduce overhead.

### "Packet-number reconstruction is random guessing."

No. The receiver uses previously received packet-number state and the encoded packet-number length to select the appropriate full value.

### "Header protection provides the same security as AEAD."

No. Header protection masks selected header fields. AEAD provides authenticated encryption for the protected payload.

### "The IV itself is transmitted in every packet."

No. The IV is derived cryptographic material known to the endpoints and is combined with the packet number to construct the AEAD nonce.

## Summary

QUIC packet numbers are central to transport operations such as ACK processing and loss detection, and they also participate in AEAD nonce construction. QUIC maintains separate packet-number spaces for different encryption levels.

QUIC uses header protection to mask selected bits of the packet header, including the packet-number bytes. A separate header-protection key and a sample from the ciphertext are used to generate the protection mask.

QUIC can transmit truncated packet numbers to reduce overhead. The receiver reconstructs the full packet number using its packet-number state and the packet-number decoding rules.

Once the full packet number is recovered, it is combined with the IV to construct the AEAD nonce. The receiver can then authenticate and decrypt the packet payload.

## Key Takeaways

1. QUIC packet numbers identify packets and support transport functions such as ACKs and loss detection.
2. QUIC has separate packet-number spaces for different encryption levels.
3. Header protection masks selected bits of the QUIC header.
4. Header protection is separate from AEAD payload protection.
5. A ciphertext sample and a header-protection key are used to generate the header-protection mask.
6. QUIC can transmit truncated packet numbers to reduce overhead.
7. The receiver reconstructs the full packet number using connection state.
8. The packet number participates in AEAD nonce construction.
9. The receiver removes header protection before constructing the AEAD nonce.
10. HTTP/3 relies on QUIC to handle all of this packet-level machinery.

## Reflection Questions

1. Why does QUIC need packet numbers?
2. How are QUIC packet numbers different from TCP sequence numbers?
3. Why does QUIC maintain separate packet-number spaces?
4. What does header protection actually mask?
5. Why is header protection separate from AEAD?
6. Why can QUIC transmit a truncated packet number?
7. How does the receiver reconstruct the full packet number?
8. Why is the packet number involved in nonce construction?
9. What information is needed to generate the header-protection mask?
10. Why does the receiver remove header protection before payload decryption?

## What's Next

### Lesson 39 - QUIC Reliability, Loss Detection & ACKs

We will now look at what happens when QUIC packets are lost:

```text
Packets
   |
   v
ACKs
   |
   v
Missing packet detected
   |
   v
Loss detection
   |
   v
Retransmit data
```

The focus will be on the architecture and mental model rather than reproducing the complete RFC loss-detection algorithm.
