
## Lesson 1 – What is the Internet?

**Date:** 2026-07-05

### What I Learned

The Internet is not a single network. It is a collection of independent networks connected using standardized protocols like TCP/IP.

### Key Insight

Understanding systems starts by understanding the problems they were designed to solve.

### Questions

- How do routers know where to send packets?
- What exactly is inside a packet?
- How do computers discover each other?

---

# Lesson 01 - What is the Internet?

**Date:** 2026-07-05

## What I Learned
The Internet is a decentralized network of interconnected networks communicating using TCP/IP.

## Questions
- How do routers forward packets?
- How does DNS work?

---

# Lesson 02 - What is a Network?

**Date:** 2026-07-05

## What I Learned
A network is a collection of devices that communicate using communication media and standardized protocols. The Internet is one example of a network, but networks can also exist independently.

## Questions
- How are devices uniquely identified on a network?
- How does a router decide where to send packets?

---

# Lesson 03 - How Does Data Travel Across a Network?

**Date:** 2026-07-05

## What I Learned
Application data is converted into binary, divided into packets, transmitted as physical signals by the NIC, forwarded by networking devices, and reassembled at the destination.

## Questions
- How does TCP detect lost packets?
- How are packets ordered correctly at the receiver?

---

# Lesson 04 - Bits, Frames, and Packets: The Units of Network Communication

**Date:** 2026-07-05

## What I Learned
Networking uses different units at different layers. Bits represent physical signals, frames move data across a local network, and packets enable communication across multiple networks through encapsulation and decapsulation.

## Questions
- What information is contained in an Ethernet frame?
- How does encapsulation map to the OSI model?

---

# Lesson 05 - The OSI Model

**Date:** 2026-07-05

## What I Learned
The OSI model divides networking into seven conceptual layers, each responsible for one aspect of communication. Layering makes networking modular, scalable and easier to debug.

## Questions
- Why was the OSI model never implemented directly?
- Which OSI layers correspond to modern protocols?

---

# Lesson 06 - The TCP/IP Model

**Date:** 2026-07-05

## What I Learned
The Internet is built on the TCP/IP model rather than the OSI model. The four-layer architecture maps real-world protocols such as HTTP, TCP, IP and Ethernet to different responsibilities.

## Questions
- How does encapsulation happen across TCP/IP layers?
- How do routers process IP packets while ignoring application data?

---

# Lesson 07 - Encapsulation & Decapsulation

**Date:** 2026-07-05

## What I Learned
I now understand how application data is progressively wrapped by TCP, IP and Ethernet before being transmitted as bits. I also learned why routers replace Ethernet frames while forwarding IP packets.

## Questions
- How are TCP headers interpreted by the receiving operating system?
- What happens if an IP packet is larger than the network's MTU?

---

# Lesson 08 - IP Addressing

**Date:** 2026-07-05

## What I Learned
IP addresses provide logical addressing for communication across networks, while MAC addresses are used only within a local network. I also learned why private IP addresses can be reused across millions of networks and how NAT translates them to public IP addresses for Internet communication.

## Questions
- How exactly does NAT maintain mappings for thousands of simultaneous connections?
- How does a router determine the next hop for a given destination IP address?

---

# Lesson 09

**Date:** 2026-07-06

## What I Learned
Subnets, subnet masks and CIDR.

---

# Lesson 10

**Date:** 2026-07-06

## What I Learned
ARP, ARP cache and MAC resolution.

## Lesson 11 - Routing
Completed the study of routing fundamentals including routers, default gateways, routing tables, longest prefix match, and hop-by-hop forwarding. Understood how packets move across multiple networks and why Layer 2 headers are recreated at every hop.

## Lesson 12 - Network Address Translation (NAT)
Learned why NAT was introduced to address IPv4 exhaustion, how private and public IPs interact, the roles of SNAT, DNAT, and PAT, and how routers maintain NAT tables. Also explored port forwarding, Carrier-Grade NAT, and cloud NAT Gateways.

## Lesson 13 - Domain Name System (DNS)
Learned how DNS translates domain names into IP addresses, the complete DNS resolution process, recursive and iterative queries, the DNS hierarchy, caching using TTL, and the role of common DNS record types. Also understood that DNS resolution is the first step before establishing any TCP connection or sending an HTTP request.

## Lesson 14 - Transmission Control Protocol (TCP)
Studied how TCP provides reliable communication over IP through sequence numbers, acknowledgments, retransmissions, and the Three-Way Handshake. Learned how TCP ensures ordered delivery, manages connection establishment and termination, and uses flow control and congestion control to provide efficient and reliable data transfer.
