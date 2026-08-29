# Encapsulation Overview

```text
Application Data
        │
        ▼
+----------------+
| TCP Segment    |
+----------------+
        │
        ▼
+----------------+
| IP Packet      |
+----------------+
        │
        ▼
+----------------+
| Ethernet Frame |
+----------------+
        │
        ▼
Bits
```

Each layer wraps the data from the layer above.
