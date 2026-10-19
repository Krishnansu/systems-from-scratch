# Lesson 94 — Firewall Fundamentals

## Objectives
- Explain firewall responsibilities and placement.
- Compare stateful and stateless filtering.
- Understand inbound and outbound rules.
- Distinguish firewalls, reverse proxies, WAFs, and application authorization.
- Apply least privilege to network access.

## Prerequisites
- Lesson 72 — Linux Networking Tools
- Lesson 83 — Authentication Fundamentals
- Lesson 84 — Authorization Fundamentals
- Lesson 88 — Reverse Proxy Fundamentals
- Lesson 93 — Health Checks and Backend Availability

## Theory
A firewall permits or blocks network traffic according to rules. It helps restrict which sources can reach which destinations, protocols, and ports. Network reachability does not establish user identity or application permission.

## Real World Example
A production architecture exposes HTTPS on the reverse proxy while keeping application servers and the database private. The proxy may reach application servers on TCP 8080, and application servers may reach the database on TCP 5432. Public clients cannot directly reach those internal ports.

## Deep Dive
- Firewalls can operate at network boundaries, on individual hosts, in cloud networks, or in workload networking systems.
- Stateless filtering evaluates packets independently. Stateful filtering tracks connections and can recognize return traffic associated with an allowed connection.
- Inbound and outbound describe direction relative to a particular enforcement point. Restricting outbound traffic can reduce lateral movement and data exfiltration after compromise.
- Default-deny policies block unspecified traffic unless explicitly permitted. Rules should document source, destination, protocol, port, purpose, and owner.
- A firewall controls network reachability; a reverse proxy routes application requests; a WAF inspects web traffic for suspicious patterns; application authorization decides which identities may perform operations.
- A connection timeout alone does not prove a firewall is responsible. Check the listening socket, addressing, routing, firewall rules, connectivity from the actual source, and application logs.

## Hands-on Exercise
1. Design minimum allow rules for public clients, a reverse proxy, two application servers, and a database.
2. Diagnose a proxy timeout when the backend listens on the expected port.
3. Explain how stateful filtering handles return traffic.

## Common Misconceptions
- A firewall rule allowing a connection does not authorize database queries or application actions.
- A reverse proxy does not replace network-level controls.
- Internal traffic is not automatically trustworthy.
- A timeout can have causes other than firewall filtering.
- Default deny still requires correct rules and documented dependencies.

## Summary
Firewalls enforce network access boundaries. Stateful and stateless filtering differ in connection tracking, while inbound and outbound policies restrict traffic direction. Firewalls work alongside reverse proxies, WAFs, and application authorization rather than replacing them.

## Key Takeaways
- Allow only required source-to-destination communication.
- Restrict inbound and outbound traffic deliberately.
- Segment public, application, and data tiers.
- Network permission is not application authorization.
- Diagnose connectivity layer by layer instead of broadly opening ports.

## Reflection Questions
1. Why is allowing public traffic only to the reverse proxy safer than exposing application servers directly?
2. What is the practical difference between stateful and stateless firewall filtering?
3. Why should a production application server have outbound firewall restrictions?
4. If a firewall allows access to a database port, why can a query still fail with a permission error?
5. A reverse proxy times out while connecting to a backend. What evidence would help you determine whether the firewall, routing, or application is responsible?

## What's Next
Lesson 95 — VPN Fundamentals: understand encrypted tunnels, VPN endpoints, routing, and how VPNs differ from proxies.
