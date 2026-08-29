# Lesson 39 - QUIC Reliability, Loss Detection & ACKs

## Objectives

- Understand how QUIC provides reliability above UDP.
- Understand QUIC ACK frames and ACK ranges.
- Understand ACK delay.
- Understand the role of packet numbers in loss detection.
- Understand packet-threshold and time-threshold loss detection at a high level.
- Understand RTT measurement.
- Understand why QUIC retransmits data rather than packets.

## Concept Summary

UDP does not provide reliability, ordering or retransmission. QUIC builds these capabilities above UDP.

QUIC uses packet numbers, ACK frames, RTT measurements and loss-detection rules to identify packets that are likely lost. Reliable data from lost packets can then be sent again in new packets.

## Core Ideas

### ACKs

An ACK frame communicates which packet numbers the receiver has received. ACKs can represent ranges.

```text
Received packets

100 101    103 104 105 106
 |   |      |   |   |   |
 +---+      +---------------+
  range          range

100-101        103-106
```

This is more efficient than acknowledging every packet independently.

### ACK Delay

A receiver can delay acknowledgments briefly so that one ACK can cover multiple packets.

```text
Packet 100 ----->
Packet 101 ----->
Packet 102 ----->

                 |
                 v
             One ACK
```

The sender accounts for acknowledged delay when interpreting timing information.

### Detecting Loss

A missing packet is not automatically lost because it may simply be delayed.

QUIC uses both packet-number evidence and timing.

```text
                     Loss Detection
                           |
              +------------+------------+
              |                         |
              v                         v
       Packet threshold            Time threshold
              |                         |
              +------------+------------+
                           |
                           v
                    Packet likely lost
```

### Packet Threshold

If sufficiently newer packets have been acknowledged while an older packet remains unacknowledged, QUIC can infer that the older packet is probably lost.

```text
100 ✓
101 ✓
102 ?
103 ✓
104 ✓
105 ✓
106 ✓

      |
      v
Enough newer packets acknowledged
      |
      v
102 considered lost
```

### Time Threshold

If a packet remains unacknowledged beyond an RTT-based time threshold, QUIC can consider it lost.

```text
Packet sent
    |
    v
Wait
    |
    v
Expected delivery window
    |
    v
Still no ACK
    |
    v
Packet likely lost
```

### RTT Measurement

QUIC measures the time between sending a packet and receiving corresponding acknowledgment information.

```text
Sender                         Receiver
   |                              |
   |------ Packet --------------->|
   |                              |
   |<------------- ACK -----------|
   |                              |
   +----------- RTT -------------+
```

RTT estimates help determine timing for loss detection and other transport behavior.

## Retransmission Model

QUIC does not generally retransmit an old packet byte-for-byte. Instead, data that needs reliable delivery can be placed into a new packet.

```text
Original
Packet 102
+----------------------+
| STREAM data: ABC     |
+----------------------+
          X
        LOST

Retransmission
Packet 110
+----------------------+
| STREAM data: ABC     |
+----------------------+
```

The packet number changes. The reliable stream data is what matters.

## Reliability Loop

```text
Packet Numbers
      |
      v
ACK Frames
      |
      v
Loss Detection
      |
      v
Lost Data
      |
      v
New Packet
      |
      v
Retransmitted Data
```

## Practical Example

Suppose the sender transmits packets 100 through 104. The receiver reports receipt of 100, 101, 103 and 104. Packet 102 is currently missing.

The sender does not immediately assume that 102 is lost. If later ACK information or elapsed time satisfies the loss-detection rules, the sender marks 102 as lost and retransmits any necessary reliable data from it in a new packet.

## Production Perspective

Loss detection is essential for real networks because packet loss is normal. The sender must distinguish genuine loss from ordinary network delay to avoid unnecessary retransmissions and congestion-control reactions.

ACK ranges also make acknowledgment efficient when packets arrive with gaps or out of order.

## Common Mistakes

- A missing packet number does not immediately mean packet loss.
- ACKs do not imply that the receiver has acknowledged every previous packet.
- QUIC does not simply copy a lost packet and reuse its packet number.
- UDP itself does not provide QUIC's reliability.
- RTT is not a single permanently fixed value.

## Key Takeaways

1. QUIC provides reliability above UDP.
2. ACK frames communicate received packet ranges.
3. ACK delay can reduce unnecessary acknowledgment traffic.
4. Loss detection uses packet-number and time-based evidence.
5. RTT estimation is important for time-based loss detection.
6. QUIC retransmits reliable data in new packets rather than retransmitting old packet identities.

## Reflection Questions

1. Why isn't a missing packet immediately considered lost?
2. Why are ACK ranges useful?
3. What is the purpose of ACK delay?
4. How do packet-threshold and time-threshold loss detection differ?
5. Why does QUIC need RTT estimation?
6. Why does QUIC retransmit data rather than the original packet?

## Related Lessons

- Lesson 38 - QUIC Header Protection & Packet Numbers
- Lesson 40 - QUIC Streams & Multiplexing
