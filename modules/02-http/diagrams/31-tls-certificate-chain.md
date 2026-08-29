# TLS Certificate Chain of Trust

```text
Browser / Operating System
          |
          | trusts
          v
       Root CA
          |
          | signs
          v
   Intermediate CA
          |
          | signs
          v
 Server Certificate
          |
          | identifies
          v
     example.com
```

**Certificate Validation**

```text
Certificate
     |
     +-- Domain matches?
     |
     +-- Valid date?
     |
     +-- Trusted chain?
     |
     +-- Signatures valid?
     |
     v
   Trusted
```

**Key Point**
- A certificate binds a server identity to a public key.
- The CA chain allows the browser to establish trust in that binding.