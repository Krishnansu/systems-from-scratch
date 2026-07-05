# IP Addressing

## IPv4 Address Structure

```text
192 . 168 . 1 . 10
 │      │    │    │
 │      │    │    └── Octet 4
 │      │    └─────── Octet 3
 │      └──────────── Octet 2
 └─────────────────── Octet 1

4 Octets
=
32 Bits
```

---

## Public vs Private Network

```text
                 Internet
                     │
              Public IP
           49.204.10.20
                     │
                Home Router
          ┌──────────┴──────────┐
          │                     │
192.168.1.10             192.168.1.20
   Laptop                   Phone
```

---

## Packet Routing

```text
Laptop
192.168.1.10
      │
      ▼
Home Router
      │
      ▼
Internet
      │
      ▼
Destination Router
      │
      ▼
Server
142.250.183.110
```

Routers make forwarding decisions using the destination IP address.

---

## MAC vs IP

```text
MAC Address
───────────
Works inside one network.
Changes at every router.

        ▼

IP Address
──────────
Works across multiple networks.
Remains the end-to-end logical address.
```

---

## Private IP Reuse

```text
Home A                     Home B

192.168.1.10              192.168.1.10
      │                         │
Router NAT                Router NAT
      │                         │
203.10.5.8              49.204.10.20
           \           /
            \ Internet/
```

The duplicate private addresses never conflict because each router performs Network Address Translation (NAT).
