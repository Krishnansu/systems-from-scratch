# Lesson 06 - The TCP/IP Model

## Objectives
- Understand the TCP/IP model.
- Compare it with OSI.
- Learn the protocols present in each layer.
- Understand how real Internet communication works.

## TCP/IP Stack

```text
+---------------------------+
| Application               |
+---------------------------+
| Transport                 |
+---------------------------+
| Internet                  |
+---------------------------+
| Link                      |
+---------------------------+
```

## OSI vs TCP/IP

```text
OSI                     TCP/IP
-------------------------------------------
Application   ───────►  Application
Presentation  ───────►  Application
Session       ───────►  Application
Transport     ───────►  Transport
Network       ───────►  Internet
Data Link     ───────►  Link
Physical      ───────►  Link
```

## Common Protocols

| Layer | Examples |
|------|----------|
| Application | HTTP, HTTPS, DNS, SMTP, SSH |
| Transport | TCP, UDP |
| Internet | IP, ICMP |
| Link | Ethernet, Wi-Fi |

## Real Request Journey

```text
Browser
    │
HTTP Request
    │
TCP Segment
    │
IP Packet
    │
Ethernet Frame
    │
Bits
    │
──────── Internet ────────
    │
Bits
    │
Ethernet Frame
    │
IP Packet
    │
TCP Segment
    │
HTTP Request
    │
Web Server
```

## Layer Responsibilities
- Application → User-facing protocols.
- Transport → End-to-end communication.
- Internet → Routing between networks.
- Link → Local delivery and physical transmission.

## OSI vs TCP/IP
- OSI explains networking.
- TCP/IP implements networking.
- TCP/IP combines multiple OSI layers.

## Key Takeaways
- TCP/IP powers the modern Internet.
- Four layers replace the seven-layer OSI model.
- Every Internet protocol belongs to one TCP/IP layer.
- Backend engineers primarily work with Application and Transport layers while understanding lower layers for debugging.

## Reflection
1. Why is TCP/IP more practical than OSI?
2. Which protocols belong to each layer?
3. What is the responsibility of the Internet layer?
4. How does TCP differ from IP?
