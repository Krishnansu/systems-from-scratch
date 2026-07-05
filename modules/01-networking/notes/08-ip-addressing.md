# Lesson 08 - IP Addressing: How Devices Are Identified on a Network

## Objectives
- Understand why IP addresses exist.
- Differentiate IP addresses from MAC addresses.
- Learn the structure of IPv4 addresses.
- Understand public vs private IP addresses.
- Learn how routers use IP addresses for routing.

## Big Picture
A packet travelling across the Internet needs a globally understandable destination. MAC addresses only identify devices within a local network, so the Internet uses logical addresses called IP addresses. Routers examine destination IP addresses to determine where packets should be forwarded.

## What is an IP Address?
An IP address is a logical address assigned to a network interface. Unlike a MAC address, it is assigned by the network and may change when a device joins a different network.

Example:

```text
192.168.1.10
```

## IPv4 Structure
An IPv4 address consists of four octets.

```text
192.168.1.10
```

Each octet contains 8 bits.

```text
11111111₂ = 255₁₀
```

Therefore:

```text
4 octets × 8 bits = 32 bits
```

## Binary Representation

```text
192.168.1.10
=
11000000
10101000
00000001
00001010
```

Computers store addresses in binary while humans use dotted-decimal notation.

## MAC Address vs IP Address

| MAC Address | IP Address |
|-------------|------------|
| Physical address | Logical address |
| Link Layer | Internet Layer |
| Local communication | Communication across networks |
| Usually fixed | Assigned by the network |
| Changes rarely | Often changes when switching networks |

A useful analogy:

- MAC Address = Apartment number
- IP Address = Street address

## Public vs Private IP Addresses

### Private IP Ranges

```text
10.0.0.0      - 10.255.255.255
172.16.0.0    - 172.31.255.255
192.168.0.0   - 192.168.255.255
```

Private IP addresses are reusable because they are never routed over the public Internet.

### Public IP Addresses
Public IP addresses are globally unique and are assigned by Internet Service Providers.

Example:

```text
142.250.183.110
```

## Home Network Example

```text
                 Internet
                     │
            Public IP
          49.204.10.20
                     │
              Home Router
         ┌───────────┴───────────┐
         │                       │
192.168.1.10              192.168.1.20
  Laptop                    Phone
```

The router connects a private network to the public Internet.

## Routing
Routers inspect only the destination IP address when deciding the next hop.

Routers do not normally inspect:
- HTTP
- HTML
- JSON
- Images

## Deep Dive
Private IP addresses can be reused because they never leave their local network. When traffic reaches the router, Network Address Translation (NAT) converts private addresses into public addresses before packets are forwarded onto the Internet.

For example, two homes can both have a laptop with IP address `192.168.1.10` without conflict because each router translates its private network to a different public IP address.

## Production Perspective
Cloud virtual machines, Kubernetes nodes, home routers, load balancers and enterprise servers all use IP addresses for communication. Understanding logical addressing is essential before learning routing, subnets, DNS and NAT.

## Common Misconceptions
- IP addresses do not permanently identify a computer.
- MAC addresses cannot replace IP addresses for Internet routing.
- Private IP addresses are not globally unique.

## Hands-On

Linux/macOS:

```bash
ip addr
```

or

```bash
ifconfig
```

Windows:

```powershell
ipconfig
```

Identify:
- IPv4 address
- Default gateway
- Whether your address is public or private

## Related Diagrams
- diagrams/networking/03-data-travel.md
- diagrams/networking/05-bits-packets-frames.md
- diagrams/networking/11-ip-addressing.md

## Key Takeaways
- IP addresses are logical addresses.
- IPv4 addresses are 32 bits long.
- Routers forward packets using destination IP addresses.
- MAC addresses are only meaningful on the local network.
- Private IP addresses are reused across different networks.
- NAT allows private networks to communicate with the public Internet.

## Reflection
1. Why are IP addresses required in addition to MAC addresses?
2. Why can multiple homes use the same private IP addresses?
3. Why does a router need both a public and a private IP address?
4. Why do routers inspect IP headers instead of HTTP requests?
