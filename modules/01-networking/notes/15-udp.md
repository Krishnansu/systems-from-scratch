# Lesson 15 — User Datagram Protocol (UDP)

## Objectives

- Understand why UDP exists alongside TCP.
- Understand connectionless communication.
- Understand the UDP header and ports.
- Understand UDP's reliability model and limitations.
- Understand common UDP use cases.
- Understand how reliability can be implemented above UDP.

## Prerequisites

- IP addressing
- Routing
- Ports
- TCP
- Packets and encapsulation

## Theory

UDP (User Datagram Protocol) is a minimal transport-layer protocol. Unlike TCP, it does not establish a connection, guarantee delivery, guarantee ordering, retransmit lost packets, or provide flow and congestion control.

UDP provides source and destination ports, datagram length, and a checksum. Its header is 8 bytes.

UDP is connectionless: applications can send datagrams without a transport-level handshake. Each datagram is independent.

UDP is useful when applications prefer low overhead, low latency, message boundaries, or application-controlled reliability.

## Real World Example

DNS commonly uses UDP for request-response communication. A DNS resolver sends a query to a server such as port 53 and can retry if the request or response is lost.

Real-time applications such as multiplayer games and media systems may prefer UDP because stale data can be less useful than the newest data.

## Deep Dive

TCP provides a reliable ordered byte stream. UDP provides independent datagrams and preserves message boundaries.

UDP does not mean that reliability is impossible. Protocols can build sequence numbers, acknowledgements, retransmissions, encryption, and congestion control above UDP. QUIC is a major example.

A UDP checksum can detect corruption but does not guarantee delivery or repair lost data.

## Hands-on Exercise

Build a UDP client and server using Python's `socket` module. Use `SOCK_DGRAM`, `sendto()`, and `recvfrom()` to exchange a message and acknowledgement.

## Common Misconceptions

- UDP is not automatically faster in every situation.
- UDP does use ports.
- UDP packets can be lost, duplicated, or reordered.
- UDP has a checksum for corruption detection.
- UDP is not limited to gaming.
- Security can be implemented by protocols running over UDP.

## Summary

UDP is a lightweight, connectionless transport protocol that provides datagram delivery with minimal built-in guarantees. Its simplicity allows applications to choose their own reliability and performance mechanisms.

## Key Takeaways

1. UDP is connectionless.
2. UDP uses ports for application multiplexing.
3. UDP preserves datagram boundaries.
4. UDP does not guarantee delivery or ordering.
5. UDP has an 8-byte header.
6. UDP's checksum detects corruption but does not provide reliability.
7. Applications can implement reliability above UDP.
8. UDP is useful for DNS, real-time communication, games, and protocols such as QUIC.

## Reflection Questions

1. If TCP already provides reliable communication, why might a multiplayer game prefer UDP?
2. What is the difference between a UDP checksum and TCP retransmission?
3. Why is UDP's datagram-oriented model useful for DNS?
4. How could you design a reliable protocol on top of UDP?
5. Why might retransmitting an old game position make the system worse?

## What's Next

Lesson 16 — How the Web Works: HTTP
