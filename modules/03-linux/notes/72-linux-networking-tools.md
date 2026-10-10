# Lesson 72 — Linux Networking Tools

## Objectives
- Inspect network interfaces and addresses with `ip`.
- Understand route selection with `ip route`.
- Inspect listening sockets and connections with `ss`.
- Use `ping` and `curl` while understanding their limitations.

## Concept Summary
Linux networking troubleshooting requires separating interface state, IP addressing, routing, sockets, packet filtering, and application behavior. No single command proves end-to-end connectivity.

## Core Ideas
- `ip link show` displays network interfaces and link state.
- `ip addr show` displays addresses assigned to interfaces.
- `ip route show` displays routing entries; `ip route get DEST` shows the kernel's route decision for a destination.
- Linux generally prefers the longest matching route prefix, subject to policy routing and other rules.
- `ss -lnt` displays listening TCP sockets; `ss -lnu` displays listening UDP sockets; `ss -tn state established` displays established TCP connections.
- `127.0.0.1` is IPv4 loopback. A service bound only to loopback generally cannot accept connections addressed to the host's network IP.
- `0.0.0.0` is the IPv4 wildcard bind address, not a destination clients should normally connect to.
- `ping` tests ICMP Echo reachability. Failure does not prove TCP or application traffic is unavailable.
- `curl -v` can test an actual HTTP request and reveal where it fails.

## Troubleshooting Sequence
```text
Interface/address -> Route -> Listening socket
        -> Network path/firewall -> Application response
```
This is a diagnostic guide, not a rigid sequence; start from the symptom and available evidence.

## Practical Commands
```bash
ip link show
ip addr show
ip route show
ip route get 8.8.8.8
ss -lnt
ss -lnu
ss -tn state established
sudo ss -lntp
ping -c 4 8.8.8.8
curl -v http://127.0.0.1:8000/
```

## Production Perspective
- A running process does not guarantee that the expected port is listening.
- A listening socket does not guarantee remote reachability; inspect its bind address, routes, firewall rules, and network path.
- Host and container network namespaces may expose different interfaces, addresses, and sockets.
- Use multiple observations to isolate a failure rather than treating one command as proof of overall health.

## Common Mistakes
- Assuming interface `UP` means internet access works.
- Treating failed ping as proof that a host or service is down.
- Assuming a listener bound to `127.0.0.1` is remotely accessible.
- Treating `ip route get` as a connectivity test.
- Assuming a single successful HTTP request proves overall application health.

## Key Takeaways
1. `ip` reveals interface, address, and routing information.
2. `ss` reveals socket state and listening ports.
3. `ping` tests ICMP, not application availability.
4. `curl` tests an HTTP path but only for the request performed.
5. Network debugging is evidence-driven, layer by layer.

## Reflection Questions
1. What is the difference between an interface, an IP address, and a route?
2. Why might an API work through localhost but fail from another machine?
3. Why can ping fail while an HTTP service remains reachable?

## Related Lessons
- Lesson 63 — Linux Architecture
- Lesson 64 — Processes
- Lesson 68 — File Systems
- Lesson 71 — Linux Services
- Earlier networking lessons: IP Addressing, Subnets, Routing, TCP, and UDP
