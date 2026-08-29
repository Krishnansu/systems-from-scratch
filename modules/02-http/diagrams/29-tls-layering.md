# HTTPS Protocol Layering

```text
+-----------------------------+
| HTTP                        |
| Application Protocol        |
+-----------------------------+
| TLS                         |
| Encryption + Authentication |
+-----------------------------+
| TCP                         |
| Reliable Byte Stream        |
+-----------------------------+
| IP                          |
| Routing                     |
+-----------------------------+
| Network                     |
| Wi-Fi / Ethernet            |
+-----------------------------+
```

**Key Points**
- HTTP is the application protocol.
- TLS provides security for the HTTP data.
- TCP provides reliable byte transport.
- IP provides packet routing.
- Network technologies move frames between directly connected devices.