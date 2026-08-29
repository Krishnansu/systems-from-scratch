# Diagram 35-04 - Connection ID and Migration

```text
Before network change:

Client
  |
 Wi-Fi
  |
Internet
  |
Server

Connection ID = ABC123
```

```text
After network change:

Client
  |
Cellular
  |
Internet
  |
Server

Connection ID = ABC123
```

The network path changes while the logical QUIC connection can remain identifiable by its Connection ID.

Path validation and security checks are still required; a Connection ID does not mean arbitrary network paths are automatically trusted.
