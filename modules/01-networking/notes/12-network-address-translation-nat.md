# Lesson 12: Network Address Translation (NAT)

## Concepts Covered
- IPv4 address exhaustion
- Private vs Public IP addresses
- Source NAT (SNAT)
- Destination NAT (DNAT)
- Port Address Translation (PAT)
- NAT tables
- Port Forwarding
- Carrier-Grade NAT (CGNAT)

## Key Learnings
- Private IP addresses are not routable on the public Internet.
- NAT rewrites packet headers so private devices can communicate externally.
- PAT allows multiple devices to share a single public IPv4 address by translating ports.
- NAT tables maintain mappings so return traffic reaches the correct internal device.
- Cloud NAT Gateways use the same principles to provide outbound Internet access for private resources.

## Important Terms
- NAT
- SNAT
- DNAT
- PAT
- NAT Table
- Port Forwarding
- CGNAT
- Public IP
- Private IP

## Real-world Applications
- Home broadband routers
- Enterprise firewalls
- Cloud NAT Gateways
- ISP Carrier-Grade NAT

## Next Lesson
Domain Name System (DNS)