# Lesson 10 - ARP

## Objectives
Understand ARP, ARP cache, requests/replies and local address resolution.

## What is ARP?
Maps IPv4 addresses to MAC addresses on the local network.

## Flow
1. Check ARP cache.
2. If absent, broadcast ARP request.
3. Target replies with MAC.
4. Cache mapping.
5. Send Ethernet frame.

ARP requests are broadcast.
ARP replies are unicast.

## Remote Hosts
For remote destinations ARP resolves the router's MAC, not the final server's MAC.

## Key Takeaways
- ARP = IP -> MAC
- Local network only
- Cache reduces broadcasts.
