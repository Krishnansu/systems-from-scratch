# HTTP Request Journey Across All Layers

## Objectives

- Trace an HTTP request from browser to server and back.
- Understand how HTTP, TCP, IP and the network interact.
- Understand the role of TLS in HTTPS.
- Connect application-layer requests to lower-level networking.

## Concept Summary

When a browser requests a resource, multiple layers cooperate. The browser creates an HTTP request. TCP provides a reliable byte stream. IP provides routing between networks. Link-layer technologies such as Ethernet or Wi-Fi deliver packets across individual network links.

## Complete Journey

For a request such as `GET /products/123`, the conceptual journey is:

```text
Browser
   |
   | https://shop.example.com/products/123
   v
DNS Resolution
   |
   v
IP Address Found
   |
   v
TCP Three-Way Handshake
   |
   v
TLS Handshake
   |
   v
Secure Connection Established
   |
   v
Browser Creates HTTP Request
   |
   | GET /products/123
   v
HTTP
   |
   v
TCP
   |
   v
IP
   |
   v
Network / Wi-Fi
   |
   v
Routers
   |
   v
Server
   |
   v
IP
   |
   v
TCP
   |
   v
HTTP Server
   |
   v
Application
   |
   v
Database / Cache
   |
   v
Product 123 Found
   |
   v
HTTP 200 OK
   |
   v
TCP
   |
   v
IP
   |
   v
Network
   |
   v
Browser
   |
   v
HTTP Response
   |
   v
JSON Data
```

## Layered View

The request is encapsulated as it travels down the sender's stack and decapsulated as it travels up the receiver's stack.

```text
Client Application
      |
      | HTTP Request
      v
HTTP
      |
      | HTTP bytes
      v
TCP
      |
      | TCP segments
      v
IP
      |
      | IP packets
      v
Ethernet / Wi-Fi
      |
      | Frames / signals
      v
Network
```

At the destination:

```text
Network
   |
   v
Ethernet / Wi-Fi
   |
   v
IP
   |
   v
TCP
   |
   v
HTTP
   |
   v
Application
```

## Important Distinction

TCP does not understand HTTP semantics. TCP sees an ordered byte stream.

HTTP does not understand routing. IP and routers handle packet forwarding.

The browser and server application understand HTTP.

```text
HTTP
  |  Understands requests and responses
  v
TCP
  |  Provides reliable ordered byte stream
  v
IP
  |  Provides logical addressing and routing
  v
Link Layer
  |  Delivers frames across local links
  v
Physical Network
```

## Production Perspective

A real request may involve many additional components:

```text
Browser
   |
   v
DNS Resolver
   |
   v
CDN / Edge
   |
   v
Load Balancer
   |
   v
Reverse Proxy
   |
   v
Application Server
   |
   v
Cache / Database
```

The logical HTTP request remains the same even though many infrastructure components may process or forward it.

## Key Takeaways

- HTTP is the application protocol.
- TCP transports HTTP/1.1 and HTTP/2 bytes reliably.
- IP routes packets between networks.
- Routers forward IP packets and rebuild link-layer frames at each hop.
- TLS protects HTTP traffic when HTTPS is used.
- The response follows the reverse layered path back to the client.

## Reflection Questions

- Which layers change at every router hop?
- Which information remains logically associated with the end-to-end connection?
- Why can a router forward an IP packet without understanding HTTP?

## Related Lessons

- Lesson 16 - How the Web Works
- Lesson 17 - HTTP Fundamentals
- Lesson 19 - Building a TCP/HTTP Server in Python
