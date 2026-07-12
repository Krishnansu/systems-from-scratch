# Network Address Translation (NAT)

```text
               Internet

          Public IP
        49.37.120.10
               ▲
               │
        +----------------+
        | Home Router    |
        | NAT Table      |
        +----------------+
          ▲          ▲
          │          │
192.168.1.10   192.168.1.20
 Laptop            Phone
```

### NAT Table

| Private Address | Public Address |
|-----------------|----------------|
|192.168.1.10:54321|49.37.120.10:60001|
|192.168.1.20:54322|49.37.120.10:60002|

**Key Points**
- Multiple private devices share a single public IP.
- PAT differentiates connections using port numbers.
- The NAT table maintains mappings for return traffic.