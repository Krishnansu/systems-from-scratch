# Lesson 95 — VPN Fundamentals

## Objectives
- Explain VPN tunnels, encapsulation, and encryption.
- Compare remote-access and site-to-site VPNs.
- Understand routing, full tunnels, and split tunnels.
- Distinguish VPNs from proxies and firewalls.
- Troubleshoot common VPN connectivity failures.

## Prerequisites
- Lesson 87 — Forward Proxy Fundamentals
- Lesson 88 — Reverse Proxy Fundamentals
- Lesson 91 — SSL/TLS Termination
- Lesson 94 — Firewall Fundamentals

## Theory
A Virtual Private Network (VPN) creates a protected logical communication path over an existing network. It combines tunneling with appropriate authentication and cryptographic protection. Encapsulation carries an inner packet inside an outer packet addressed to a VPN endpoint.

## Real World Example
A remote employee connects a laptop to a company VPN gateway, then accesses an internal Git server. The tunnel protects traffic between VPN endpoints, while routing and firewall rules determine whether the Git server is reachable.

## Deep Dive
- Remote-access VPNs connect individual devices; site-to-site VPNs connect networks through gateways.
- Full-tunnel routing sends most or all IP traffic through the VPN; split-tunnel routing sends only selected destinations through it.
- VPN operation depends on authentication, routes, DNS, tunnel configuration, firewall rules, and a valid return path.
- VPN tunnel encryption generally protects traffic between endpoints; it does not automatically encrypt later network hops.
- VPN connectivity does not imply application authorization or complete anonymity.
- WireGuard, IPsec, and OpenVPN are common VPN technologies with different design and operational characteristics.
- Troubleshoot in layers: routing, DNS, tunnel delivery, firewall policy, return path, listening socket, and application behavior.

## Hands-on Exercise
1. Diagnose three possible causes when the tunnel connects but an internal server is unreachable.
2. Explain why VPN access should not automatically grant database access.
3. Diagnose a server reply routed through the wrong gateway.
4. Describe a split-tunnel security and performance trade-off.
5. Explain what protects traffic after it leaves the VPN gateway.

## Common Misconceptions
- A connected VPN does not guarantee destination reachability.
- A VPN does not automatically make users anonymous.
- Not all traffic necessarily enters the tunnel.
- VPN access is not application authorization.
- Encryption may end at the VPN gateway.
- Tunneling and encryption are distinct mechanisms.

## Summary
VPNs provide protected logical connectivity across existing networks. Their behavior depends on endpoint authentication, cryptographic protection, encapsulation, routing, DNS, and firewall policy. Remote-access and site-to-site VPNs serve different connectivity needs, while full and split tunnels trade centralized control against direct traffic efficiency.

## Key Takeaways
- A VPN tunnel carries traffic between defined endpoints.
- Routes decide which traffic enters the tunnel.
- Network reachability, authentication, and authorization are separate.
- Tunnel encryption does not guarantee encryption on every subsequent hop.
- Diagnose VPN failures layer by layer.

## Reflection Questions
1. What is encapsulation, and why does a VPN use an outer packet?
2. How does a remote-access VPN differ from a site-to-site VPN?
3. What are the trade-offs between full-tunnel and split-tunnel routing?
4. Why can a VPN connect while an internal application remains unreachable?
5. What protects traffic between the VPN gateway and an internal service?

## What's Next
Lesson 96 — Why Containers? Begin Module 06 by examining the problems containers solve and how they differ from virtual machines and ordinary processes.
