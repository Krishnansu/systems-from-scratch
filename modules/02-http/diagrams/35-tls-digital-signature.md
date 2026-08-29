# TLS Server Authentication with Digital Signature

```text
                 Server
                    |
                    | Handshake Information
                    v
                  Hash
                    |
                    v
           Sign with Private Key
                    |
                    v
             Digital Signature
                    |
                    +---------------------> Browser
                                               |
                                               | Server Public Key
                                               v
                                             Verify
                                               |
                                      +--------+--------+
                                      |                 |
                                    Valid            Invalid
                                      |                 |
                                      v                 v
                                    Trust             Abort
```

**Key Points**
- The certificate provides the authenticated public key.
- The signature demonstrates possession of the corresponding private key.
- The browser verifies the signature using the public key.