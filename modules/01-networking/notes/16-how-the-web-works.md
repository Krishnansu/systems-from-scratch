# How the Web Works - DNS, TCP, TLS and HTTP

## Objectives

- Understand what happens when a user enters a URL in a browser.
- Understand the relationship between DNS, TCP, TLS and HTTP.
- Understand why HTTP operates on top of TCP.
- Understand the basic role of QUIC and HTTP/3.

## Concept Summary

A browser does not immediately send an HTTP request when a URL is entered. The browser first needs to resolve the domain name to an IP address. For traditional HTTP/1.1 and HTTP/2 over TCP, a TCP connection is established before HTTP data is exchanged. For HTTPS, TLS is then established before HTTP data is sent securely.

The simplified flow is:

```text
User enters URL
      |
      v
Browser
      |
      | DNS lookup
      v
IP Address Found
      |
      v
TCP Three-Way Handshake
      |
      v
TCP Connection Ready
      |
      v
TLS Handshake (HTTPS)
      |
      v
Secure Connection Ready
      |
      v
HTTP Request
      |
      v
HTTP Response
      |
      v
Browser Renders Page
```

## Core Ideas

- DNS resolves domain names to IP addresses.
- TCP provides a reliable ordered byte stream for HTTP/1.1 and HTTP/2.
- TLS provides encryption, authentication and integrity for HTTPS.
- HTTP defines the application-level request and response protocol.
- HTTP is not responsible for establishing the TCP connection.
- The browser creates the HTTP request and gives its bytes to the underlying transport connection.
- QUIC runs over UDP and provides transport features such as reliability, ordering and multiplexing at the QUIC layer.
- HTTP/3 uses QUIC instead of TCP.

## Request Journey

When a user enters `http://example.com`, the conceptual flow is:

```text
You type:

http://example.com
        |
        v
     Browser
        |
        | DNS lookup
        v
  IP Address Found
        |
        v
 TCP Three-Way Handshake
        |
        v
  TCP Connection Ready
        |
        v
  Browser creates
    HTTP Request
        |
        | HTTP bytes given to TCP
        v
    TCP Segments
        |
        v
    IP Packets
        |
        v
      Network
        |
        v
      Server
        |
        v
 TCP reassembles bytes
        |
        v
 Web Server sees
   HTTP Request
        |
        v
  Processes Request
        |
        v
  Creates HTTP Response
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
   Renders Web Page
```

## QUIC + UDP

UDP itself does not provide reliable delivery, ordering or congestion control. QUIC implements these transport features in user space while using UDP as the underlying packet transport.

```text
HTTP/3
  |
  v
QUIC
  |
  | Reliability
  | Encryption integration
  | Multiplexed streams
  | Congestion control
  v
UDP
  |
  v
IP
  |
  v
Network
```

This allows HTTP/3 to avoid some limitations of TCP, particularly TCP-level head-of-line blocking between independent streams.

## Production Perspective

A modern browser may use different protocol stacks depending on the server and network:

```text
HTTP/1.1 -> TCP -> TLS (HTTPS) -> IP
HTTP/2   -> TCP -> TLS (HTTPS) -> IP
HTTP/3   -> QUIC -> UDP -> IP
```

The exact sequence also depends on connection reuse, DNS caching, TLS session resumption, HTTP version negotiation and other optimizations.

## Key Takeaways

- DNS usually comes before connecting to the server by hostname.
- HTTP is an application-layer protocol.
- TCP is a transport-layer protocol that carries HTTP/1.1 and HTTP/2 bytes.
- HTTPS is HTTP protected by TLS.
- HTTP/3 uses QUIC over UDP.
- The browser is responsible for creating HTTP requests, while lower layers transport the resulting bytes.

## Reflection Questions

- Why can HTTP exist independently of TCP as a protocol concept?
- What does TLS add between HTTP and TCP?
- Why can QUIC use UDP while still providing reliable transport features?

## Related Lessons

- Lesson 13 - DNS
- Lesson 14 - TCP
- Lesson 15 - UDP
- Lesson 17 - HTTP Fundamentals
