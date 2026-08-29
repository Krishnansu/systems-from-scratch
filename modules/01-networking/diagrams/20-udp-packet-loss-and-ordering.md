# UDP Packet Loss and Ordering

## Packet Loss

```text
Sender                         Receiver

  A ────────────────────────────► A
  B ────────────────X
  C ────────────────────────────► C
  D ────────────────────────────► D

             Packet B Lost

  UDP does NOT automatically retransmit B.
```

## Packet Reordering

```text
Sender                         Receiver

  A ────────────────────────────► A
  B ────────────────────────────►
  C ────────────────────────────► C

       Network reorders packets

  Receiver may observe:

             A → C → B

  UDP does NOT restore packet ordering.
```

**Key Points**
- UDP does not guarantee packet delivery.
- UDP does not guarantee packet ordering.
- Packets may be lost, duplicated, or reordered.
- UDP does not automatically retransmit lost packets.
- Applications can implement their own reliability mechanisms when required.