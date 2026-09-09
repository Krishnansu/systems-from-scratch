# Diagram 132 — WebSocket Frame Structure

```text
┌──────────────────────────────┐
│ FIN / RSV / Opcode           │
├──────────────────────────────┤
│ MASK / Payload Length        │
├──────────────────────────────┤
│ Extended Length (optional)  │
├──────────────────────────────┤
│ Masking Key (client → server)│
├──────────────────────────────┤
│ Payload Data                 │
└──────────────────────────────┘
```
