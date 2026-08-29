# TLS Handshake Overview

```text
Browser                                      Server
   |                                            |
   |---------- ClientHello ------------------->|
   |                                            |
   |<--------- ServerHello --------------------|
   |<--------- Certificate --------------------|
   |<--------- CertificateVerify --------------|
   |                                            |
   |     Validate certificate + signature      |
   |     Perform key agreement                 |
   |     Derive traffic keys                   |
   |                                            |
   |=========== Encrypted Traffic =============|
```

**Key Points**
- ClientHello begins TLS negotiation.
- ServerHello selects compatible parameters.
- The certificate authenticates the server identity.
- Key exchange establishes shared cryptographic material.
- Traffic keys are derived before protected application data is exchanged.