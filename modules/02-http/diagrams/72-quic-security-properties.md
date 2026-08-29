# Diagram 37-08 - QUIC Security Properties

```text
                 QUIC Packet Protection
                          |
             +------------+------------+
             |                         |
             v                         v
       Payload AEAD              Header protection
             |                         |
       +-----+-----+             Masks selected
       |           |             header fields
       v           v
Confidentiality  Integrity
       |
       +-----------------------------+
                                     |
                                     v
                              Protected QUIC
```

A passive observer can still see some network metadata such as IP addresses, UDP ports, packet timing and packet sizes.
