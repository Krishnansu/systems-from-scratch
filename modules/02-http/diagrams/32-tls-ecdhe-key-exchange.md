# TLS 1.3 ECDHE Key Exchange

```text
Browser                                      Server

Private A                                    Private B
    |                                            |
    |                                            |
Public A -------------------------------------> |
    |                                            |
    | <------------------------------------- Public B
    |                                            |
    v                                            v
Calculate Shared Secret                  Calculate Shared Secret
    |                                            |
    +------------------- SAME ------------------+
```

**Key Points**
- Private ephemeral keys remain local to each endpoint.
- Public key-share information is exchanged.
- Both endpoints independently calculate the same shared secret.
- The shared secret is not sent directly across the network.
- Ephemeral keys provide the basis for forward secrecy.