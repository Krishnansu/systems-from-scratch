# Diagram 35-02 - Packet Number vs Stream Offset

```text
QUIC Connection

Packet #200
   |
   +-- STREAM frame
          |
          +-- Stream ID = 4
          +-- Offset = 100
          +-- Data = "hello"
```

The numbers have different meanings:

```text
200 -> packet number
100 -> offset inside Stream 4
```

They are separate namespaces.
