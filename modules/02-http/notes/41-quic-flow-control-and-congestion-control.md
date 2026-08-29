# Lesson 41 - QUIC Flow Control & Congestion Control

## Objectives

- Understand why QUIC needs flow control.
- Understand stream-level and connection-level flow control.
- Understand `MAX_STREAM_DATA` and `MAX_DATA`.
- Understand why flow control and congestion control solve different problems.
- Understand the congestion window (`cwnd`).
- Understand in-flight data at a high level.
- Understand how loss detection interacts with congestion control.

## Concept Summary

QUIC must limit sending for two independent reasons:

1. The receiver may not have enough buffering or processing capacity.
2. The network may not be able to handle the current sending rate.

Flow control protects the receiver. Congestion control protects the network.

```text
                 QUIC Sender
                      |
             +--------+--------+
             |                 |
             v                 v
       Flow Control      Congestion Control
             |                 |
             v                 v
      Receiver limit      Network limit
```

## Core Ideas

### Stream-Level Flow Control

A receiver can limit how much data may be sent on an individual stream.

```text
Receiver
   |
   | MAX_STREAM_DATA
   | "Stream 4 may reach offset X"
   v
Sender
```

`MAX_STREAM_DATA` advertises the maximum amount of data permitted for a particular stream.

### Connection-Level Flow Control

The receiver can also limit the total amount of stream data that may be sent across the entire connection.

```text
Stream 4  ──┐
Stream 8  ──┼──> QUIC Connection
Stream 12 ──┘
                 |
                 v
             MAX_DATA
```

`MAX_DATA` controls the connection-level data limit.

### Two Flow-Control Levels

```text
             Flow Control
                  |
          +-------+-------+
          |               |
          v               v
   Stream-level      Connection-level
   MAX_STREAM_DATA      MAX_DATA
```

### Flow-Control Window Growth

The receiver can consume data and then increase the permitted limit.

```text
Receiver                         Sender
   |                               |
   | MAX_STREAM_DATA = 100 KB      |
   |------------------------------>|
   |                               |
   |       data arrives            |
   |<------------------------------|
   |                               |
   | consume data                  |
   |                               |
   | MAX_STREAM_DATA = 200 KB      |
   |------------------------------>|
```

The sender can continue once additional credit is advertised.

### Congestion Control

Congestion control limits how much data the sender should have outstanding in the network.

```text
Sender
   |
   v
+----------------+
| congestion     |
| window         |
|     cwnd       |
+----------------+
   |
   v
Packets in flight
```

The congestion window (`cwnd`) is a sender-side estimate of how much congestion-controlled data can be outstanding without causing excessive congestion.

### In-Flight Data

Data is approximately in flight when it has been sent but has not yet been acknowledged.

```text
Sender                         Receiver
   |                              |
   |------ Packet 1 ------------->|
   |------ Packet 2 ------------->|
   |------ Packet 3 ------------->|
   |                              |
   |       unacknowledged          |
```

### Slow Start

At the beginning of a connection, the sender does not know the available network capacity. Congestion control therefore begins with a relatively small sending window and probes the path by increasing the amount of traffic.

```text
Small window
     |
     v
Larger window
     |
     v
Larger window
     |
     v
Detect network limits
```

### Loss and Congestion Control

Loss detection identifies packets that are likely lost. Congestion control uses loss and other signals to adjust the sending rate.

```text
Packet sent
    |
    v
ACK / loss signal
    |
    v
Loss detection
    |
    v
Congestion-control response
```

Loss detection and congestion control are related but are not the same mechanism.

## Multiple Constraints

The sender must respect both receiver limits and network limits.

```text
                 Sender
                    |
          +---------+---------+
          |                   |
          v                   v
   Receiver capacity     Network capacity
          |                   |
          v                   v
    Flow control         Congestion control
          |                   |
          +---------+---------+
                    |
                    v
              Actual sending
```

Conceptually:

```text
Actual send capacity
≈ min(
    stream flow-control capacity,
    connection flow-control capacity,
    congestion-control capacity
)
```

## Practical Example

Suppose:

```text
Stream available        = 500 KB
Connection available    = 800 KB
Congestion window       = 300 KB
```

The sender's practical limit is approximately:

```text
min(500, 800, 300) = 300 KB
```

If instead the stream limit were only 50 KB, then flow control would be the bottleneck even if the network could handle more.

## Flow Control vs Congestion Control

| Mechanism | Protects | Main limit |
|---|---|---|
| Stream flow control | Receiver | Per-stream data |
| Connection flow control | Receiver | Total connection data |
| Congestion control | Network | Data in flight / sending capacity |

## Production Perspective

Flow control prevents a fast sender from overwhelming receiver-side buffers. Congestion control prevents senders from aggressively filling network queues and causing widespread congestion and packet loss.

Production QUIC implementations must coordinate these mechanisms because an application can have available receiver credit while the network is currently congested, or the network can have capacity while the receiver has exhausted its flow-control window.

## Common Mistakes

- Flow control and congestion control are not the same thing.
- `MAX_STREAM_DATA` controls an individual stream.
- `MAX_DATA` controls connection-level stream data.
- A large flow-control window does not mean the network can handle unlimited traffic.
- `cwnd` is not a receiver buffer size.
- Packet loss detection and congestion control are separate mechanisms.

## Key Takeaways

1. Flow control protects the receiver.
2. QUIC has stream-level and connection-level flow control.
3. `MAX_STREAM_DATA` controls one stream.
4. `MAX_DATA` controls total connection-level stream data.
5. Congestion control protects the network.
6. `cwnd` limits congestion-controlled data in flight.
7. The sender must obey both flow-control and congestion-control constraints.
8. Loss detection provides signals that congestion control can react to.

## Reflection Questions

1. Why does QUIC need flow control if congestion control already limits sending?
2. What is the difference between `MAX_STREAM_DATA` and `MAX_DATA`?
3. What does the congestion window represent?
4. Why is a missing packet not automatically evidence that the network is congested?
5. What happens if flow control is the bottleneck but congestion control has plenty of capacity?
6. What happens if congestion control is the bottleneck but the receiver has plenty of available buffer capacity?

## Related Lessons

- Lesson 39 - QUIC Reliability, Loss Detection & ACKs
- Lesson 40 - QUIC Streams & Multiplexing
- Lesson 42 - QUIC Connection Migration & Final Architecture
