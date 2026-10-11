# Lesson 72 — Linux Networking Tools: Commands

```bash
ip link show
ip addr show
ip route show
ip route get DESTINATION
ss -lnt
ss -lnu
ss -tn state established
sudo ss -lntp
ping -c 4 DESTINATION
curl -v --connect-timeout 3 http://HOST:PORT/
```

- `ip` inspects interfaces, addresses, and routing decisions.
- `ss` inspects listening sockets and connections; `-p` may require elevated privileges to show process details.
- `ping` tests ICMP, not TCP or HTTP availability. `curl` tests the request path it actually makes.
- `0.0.0.0` is a wildcard IPv4 bind address, not a destination clients normally connect to.
