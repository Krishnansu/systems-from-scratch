# TCP-Level Head-of-Line Blocking

```text
HTTP/2 Streams

Stream A: A1 A2 A3 A4
Stream B: B1 B2 B3 B4
Stream C: C1 C2 C3 C4
        │
        ▼
     TCP Stream

A1 A2 A3 A4 B1 B2 B3 B4 C1 C2 C3 C4
        │
        │ A3 packet lost
        ▼
A1 A2 [A3 missing] A4 B1 B2 B3 B4 ...
             │
             ▼
        TCP waits for
        retransmission
```

**Key Point**

Even though HTTP/2 has independent logical streams, they share one TCP connection. TCP's ordered delivery can therefore cause loss affecting one part of the connection to delay delivery of later bytes.