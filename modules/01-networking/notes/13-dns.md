# Lesson 13: Domain Name System (DNS)

## Concepts Covered
- Purpose of DNS
- Domain names vs IP addresses
- DNS resolution process
- Recursive vs Iterative queries
- DNS hierarchy (Root, TLD, Authoritative servers)
- DNS caching
- Time To Live (TTL)
- Common DNS record types

## Key Learnings
- DNS translates human-readable domain names into IP addresses.
- Before making any TCP or HTTP connection, a client must first resolve the destination domain using DNS.
- DNS resolution first checks the browser cache, then the operating system cache, and finally queries a recursive resolver.
- Recursive resolvers query Root, TLD, and Authoritative DNS servers to obtain the final answer.
- DNS caching and TTL reduce lookup latency and improve scalability.
- A domain may resolve to different IP addresses based on load balancing, CDNs, or geographic location.

## Important Terms
- DNS
- Domain Name
- Recursive Resolver
- Authoritative Name Server
- Root Server
- TLD Server
- DNS Cache
- TTL
- A Record
- AAAA Record
- CNAME
- MX
- NS
- TXT

## Real-world Applications
- Website access
- Email delivery
- CDN routing
- Cloud services
- Service discovery

## Next Lesson
Transmission Control Protocol (TCP)