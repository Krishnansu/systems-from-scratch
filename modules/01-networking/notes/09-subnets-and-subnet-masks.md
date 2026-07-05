# Lesson 09 - Subnets and Subnet Masks

## Objectives
- Understand subnets, subnet masks, CIDR.
- Distinguish network and host portions.

## Why Subnets?
Large networks create excessive broadcasts and are hard to manage. Subnets divide a network into smaller logical networks.

## IP Address = Network + Host
Example:
- IP: 192.168.1.25
- Mask: 255.255.255.0 (/24)
- Network: 192.168.1.0
- Host: 25

## CIDR
/8=255.0.0.0
/16=255.255.0.0
/24=255.255.255.0
/32=Single host

## Same vs Different Subnet
Devices in the same subnet communicate directly.
Different subnets require a router.

## Host Decision
If destination is local -> ARP.
Else -> Default gateway.

## Production
Used in VPCs, Kubernetes, Docker and enterprise networks.

## Key Takeaways
- Network + Host portions.
- Mask determines split.
- CIDR is standard.
- Router only for different subnets.
