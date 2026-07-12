# Lesson 11: Routing

## Concepts Covered
- Purpose of routers and Layer 3 forwarding
- Default gateway
- Routing tables
- Longest Prefix Match (LPM)
- Static vs Dynamic routing
- Hop-by-hop packet forwarding

## Key Learnings
- Switches forward frames using MAC addresses, whereas routers forward packets using IP addresses.
- A host sends packets destined for another network to its default gateway.
- Routers inspect the destination IP, consult their routing table, and forward the packet to the appropriate next hop.
- Ethernet headers are rewritten at every hop, while the IP packet continues towards its destination.
- Routing decisions are made independently at each hop; routers do not know the complete end-to-end path.

## Important Terms
- Router
- Default Gateway
- Routing Table
- Next Hop
- Longest Prefix Match (LPM)
- Static Routing
- Dynamic Routing

## Real-world Applications
- Home Wi-Fi routers
- Enterprise networks
- ISP backbone routers
- Cloud networking

## Next Lesson
Network Address Translation (NAT)