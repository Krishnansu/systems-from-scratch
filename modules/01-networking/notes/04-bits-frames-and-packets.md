# Lesson 04 - Bits, Frames, and Packets: The Units of Network Communication

## Objectives
- Understand the differences between bits, frames, and packets.
- Learn encapsulation and decapsulation.
- Understand how networking layers wrap data.

## Theory
Bits are the smallest unit of information and represent physical signals on the communication medium. Packets are used for communication across interconnected networks, while frames are used for communication across a single network link. As data moves down the networking stack, each layer adds its own headers (and sometimes trailers), a process called encapsulation. At the receiver, these layers are removed through decapsulation.

## Key Takeaways
- Bits are the physical representation of data.
- Frames operate on local network links.
- Packets enable communication across multiple networks.
- Encapsulation wraps data at each networking layer.
- Frames are recreated at every network hop.

## Reflection
1. Why can't raw bits be transmitted without structure?
2. Why are frames recreated at every hop?
3. What is the difference between a frame and a packet?
4. What is the order of encapsulation from application to physical medium?
