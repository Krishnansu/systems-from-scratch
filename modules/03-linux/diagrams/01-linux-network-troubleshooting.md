# Diagram 01 — Linux Network Troubleshooting

## 1. Follow the Request, Layer by Layer

```text
Client laptop
     |
     v
[Interface and IP]       ip link / ip addr
     |
     v
[Routing decision]       ip route / ip route get
     |
     v
[Listening socket]       ss -lntp
     |
     v
[Firewall and network path]
     |
     v
[Application response]  curl / application logs
```

**Mental model:** Find the last confirmed working boundary, then investigate the next unresolved boundary. This is a reasoning guide, not a mandatory command sequence.

## 2. Ping Succeeds, but Curl Times Out

```text
PING — ICMP
Client ---- Echo Request ----> Server
Client <--- Echo Reply ------- Server
Result: ICMP replies work.

CURL — TCP to port 8000, then HTTP
Client ---- TCP connection --> Server
Result: No timely response; curl times out.
```

ICMP and TCP are different protocols. A firewall may allow ping while dropping TCP traffic to port 8000. A timeout is a clue, not proof of a firewall; routing problems, packet loss, and other failures can produce similar symptoms.

**Remember:** Successful ping does not prove that an application port is reachable.

## 3. The Bind-Address Trap

```text
127.0.0.1:8000
    |
    +--> Local requests may work.
    +--> Listener is bound to loopback only.
    +--> Requests to the server's LAN IP won't match it.

0.0.0.0:8000
    |
    +--> Listener is bound to all local IPv4 interfaces.
    +--> Requests to a local IPv4 address may reach it.
    +--> Routing, firewall rules, and network reachability still matter.
```

`0.0.0.0` is a bind address, not the destination clients should use. A client connects to the server's actual IP, for example `192.168.1.25:8000`.

## 4. Symptoms to the Next Investigation

```text
Remote HTTP request fails
          |
          v
     Check ss -lntp
          |
          +-- Listener only on 127.0.0.1?
          |       |
          |       +--> Configure the intended network bind address.
          |
          +-- Listener on expected address and port?
                  |
                  +--> Test from the remote client with curl.
                         |
                         +-- Timeout
                         |     -> Inspect firewall rules, routes,
                         |        network path, and packet arrival.
                         |
                         +-- Connection refused
                         |     -> Check listener and active rejection rules.
                         |
                         +-- HTTP 500
                               -> Investigate application logs and dependencies.
```

These outcomes are diagnostic clues, not absolute proof of a specific cause. If needed, use packet capture to determine whether TCP connection attempts reach the server.

## Quick Recall

- `ip link` / `ip addr`: interface and address.
- `ip route`: routing decision.
- `ss`: listening sockets and connections.
- `ping`: ICMP reachability, not application availability.
- `curl`: tests the actual HTTP request path.
- A process running does not guarantee a listener; a listener does not guarantee remote reachability.
