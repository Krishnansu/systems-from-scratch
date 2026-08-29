# Diagram 37-03 - QUIC AEAD Payload Protection

```text
Plaintext QUIC Payload
          +
         Key
          +
 Associated Data
          |
          v
         AEAD
          |
          v
Ciphertext + Authentication Tag
```

At the receiver:

```text
Ciphertext + Tag
      + Key
      + Associated Data
           |
           v
          AEAD
           |
      +----+----+
      |         |
      v         v
   success    failure
      |         |
      v         v
 plaintext   reject
```
