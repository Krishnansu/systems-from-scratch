# DNS Resolution Process

```text
Browser
   │
   ▼
Browser Cache
   │ miss
   ▼
OS Cache
   │ miss
   ▼
Recursive Resolver
   │
   ├────────► Root Server
   │             │
   │◄────────────┘
   │
   ├────────► .com TLD Server
   │             │
   │◄────────────┘
   │
   ├────────► Authoritative DNS Server
   │             │
   │◄────────────┘
   ▼
IP Address
142.250.x.x
```

**Key Points**
- Browser and OS caches are checked first.
- The recursive resolver performs iterative queries.
- Resolution follows Root → TLD → Authoritative hierarchy.
- The resolved IP is cached based on its TTL.