# Lesson 07 - Encapsulation & Decapsulation

## Objectives
- Understand encapsulation and decapsulation.
- Learn how each TCP/IP layer wraps data.
- Follow a real HTTP request through the networking stack.
- Understand why routers recreate frames.

## Big Picture
Applications generate data, but that data cannot travel across the network on its own. Each layer of the TCP/IP stack adds information required for its specific responsibility. This process is called encapsulation. At the destination, each layer removes its own information to recover the original application data. This reverse process is called decapsulation.

## Theory

### Step 1 - Application Layer
The browser creates an HTTP request.

```text
GET / HTTP/1.1
Host: google.com
```

### Step 2 - Transport Layer
TCP adds a transport header containing source and destination ports, sequence numbers, acknowledgements and other reliability information.

Result: **TCP Segment**

### Step 3 - Internet Layer
IP adds source and destination IP addresses along with routing information.

Result: **IP Packet**

### Step 4 - Link Layer
Ethernet (or Wi-Fi) adds MAC addresses and error detection information.

Result: **Ethernet Frame**

### Step 5 - Physical Transmission
The Network Interface Card converts the frame into electrical signals, light pulses or radio waves for transmission.

## Complete Encapsulation

```text
HTTP Request
      │
      ▼
TCP Segment
      │
      ▼
IP Packet
      │
      ▼
Ethernet Frame
      │
      ▼
Bits
```

## Router Behaviour
Routers remove the incoming Ethernet frame, inspect the IP packet, determine the next hop and create a brand new Ethernet frame for the outgoing interface.

Therefore:
- Frames are hop-to-hop.
- Packets are end-to-end.

## Decapsulation

```text
Bits
 │
 ▼
Frame
 │
 ▼
Packet
 │
 ▼
TCP Segment
 │
 ▼
HTTP Request
```

## Deep Dive
Each layer only understands its own header.

- Ethernet understands MAC addresses.
- IP understands IP addresses.
- TCP understands ports and reliability.
- HTTP understands web requests.

This separation allows independent evolution of protocols without affecting other layers.

## Production Perspective
Every API request, database query, Kubernetes service call and browser request uses encapsulation.
Understanding which layer owns which responsibility makes debugging production networking significantly easier.

## Common Misconceptions
- Routers generally inspect IP headers, not HTTP requests.
- Frames do not travel across the Internet.
- Encapsulation adds headers; it does not replace application data.

## Hands-On

```bash
curl https://example.com
```

Mentally trace the request through every TCP/IP layer.

## Key Takeaways
- Encapsulation wraps data as it moves down the stack.
- Decapsulation unwraps data at the destination.
- TCP adds transport information.
- IP adds routing information.
- Ethernet adds local delivery information.
- Frames are recreated at every router.

## Reflection
1. Why are frames recreated at every hop?
2. Why does each layer have its own header?
3. Which layer adds MAC addresses?
4. Which layer adds IP addresses?
