# Lesson 16 — How the Web Works: HTTP

## Objectives

- Understand what HTTP is and why it exists.
- Understand the client-server request-response model.
- Understand where HTTP fits relative to TCP and IP.
- Understand HTTP request and response structure.
- Understand HTTP methods and status codes.
- Understand why HTTP is stateless.
- Understand the difference between HTTP and HTTPS.
- Understand HTTP/1.1, HTTP/2, and HTTP/3 at a high level.
- Understand the relationship between HTTP/3, QUIC, and UDP.

## Prerequisites

- IP addressing
- DNS
- TCP
- UDP
- Ports
- Client-server communication
- Encapsulation

## Theory

HTTP (Hypertext Transfer Protocol) is an application-layer protocol used for communication between clients and servers.

HTTP defines the meaning and structure of application messages, while TCP provides reliable transport for those messages in HTTP/1.1 and HTTP/2.

A useful mental model is:

- HTTP = What are we saying?
- TCP = How do we reliably transport what we are saying?
- IP = Where are we sending it?
- Network = How does it physically travel?

When a browser accesses `http://example.com`, the browser first resolves the domain using DNS, establishes a TCP connection, creates an HTTP request, and sends the HTTP request bytes through TCP. TCP segments the bytes, IP packets carry them across the network, and the server reverses the process to reconstruct and interpret the HTTP request.

## Real World Example

Opening `http://example.com` can be understood as:

1. The browser parses the URL and identifies HTTP as the protocol and port 80 as the default port.
2. DNS resolves `example.com` to an IP address.
3. The browser establishes a TCP connection using the three-way handshake.
4. The browser creates an HTTP request such as `GET / HTTP/1.1`.
5. The HTTP request bytes are given to TCP.
6. TCP transports the bytes using TCP segments.
7. IP carries the packets through the network.
8. The server receives the packets and TCP reassembles the byte stream.
9. The web server interprets the HTTP request and processes it.
10. The server creates an HTTP response.
11. The response travels back through TCP, IP, and the network.
12. The browser receives the response and renders the page.

A single web page may trigger many additional HTTP requests for CSS, JavaScript, images, fonts, and other resources.

## Deep Dive

### HTTP Request

An HTTP request generally contains:

- Request line
- Headers
- Optional body

Example:

`POST /users HTTP/1.1`

`Host: api.example.com`

`Content-Type: application/json`

`Authorization: Bearer TOKEN`

The request body may contain application data such as JSON.

### HTTP Response

An HTTP response generally contains:

- Status line
- Headers
- Optional body

Example:

`HTTP/1.1 200 OK`

`Content-Type: application/json`

The response body may contain JSON, HTML, or other content.

### HTTP Methods

- GET — retrieve data.
- POST — submit data or create a resource.
- PUT — replace a resource representation.
- PATCH — partially modify a resource.
- DELETE — delete a resource.

### HTTP Status Codes

- 1xx — Informational
- 2xx — Success
- 3xx — Redirection
- 4xx — Client Error
- 5xx — Server Error

Important examples:

- 200 OK
- 201 Created
- 204 No Content
- 301 / 302 Redirection
- 400 Bad Request
- 401 Unauthorized
- 403 Forbidden
- 404 Not Found
- 429 Too Many Requests
- 500 Internal Server Error
- 502 Bad Gateway
- 503 Service Unavailable

### HTTP Is Stateless

HTTP itself is stateless. Each request is independent and HTTP does not inherently remember that two requests came from the same user.

Applications build state and identity mechanisms using cookies, sessions, tokens, or JWTs.

### HTTP and TCP

Traditional HTTP/1.1 and HTTP/2 use TCP as their transport:

`HTTP → TCP → IP`

HTTP defines the application message. TCP reliably transports the message as a byte stream. IP handles addressing and routing.

### HTTP and HTTPS

HTTPS is HTTP secured using TLS.

Conceptually:

`HTTP → TLS → TCP → IP`

TLS provides encryption, authentication, and integrity. TLS will be studied in greater depth in a dedicated future lesson.

### HTTP Versions

HTTP/1.1 uses persistent TCP connections to reduce connection overhead.

HTTP/2 introduces binary framing and multiplexing, allowing multiple streams to share one TCP connection.

HTTP/3 uses QUIC instead of TCP. QUIC runs over UDP and provides reliability, congestion control, encryption, and multiplexed streams at the transport layer.

Conceptually:

`HTTP/3 → QUIC → UDP → IP`

QUIC does not simply make UDP reliable in the same way TCP is. It is a modern transport protocol that uses UDP as its underlying packet transport and implements its own transport mechanisms.

## Hands-on Exercise

Use `curl` to observe real HTTP traffic.

```bash
curl -v http://example.com
```

Inspect only response headers:

```bash
curl -I http://example.com
```

Observe HTTPS:

```bash
curl -v https://example.com
```

The goal is to identify the HTTP request, response status, headers, and body, and to observe the difference between HTTP and HTTPS communication.

## Common Misconceptions

- HTTP is not the Internet; it is an application-layer protocol.
- HTTP does not itself transport packets across the network.
- TCP does not understand HTTP semantics; it transports bytes.
- HTTP does not require a browser; any HTTP client can communicate with an HTTP server.
- HTTP requests are not limited to GET.
- A 404 usually means the resource was not found, not that the server is down.
- UDP is not inherently unreliable at the application level; higher-level protocols such as QUIC can implement reliability and other transport features above UDP.

## Summary

HTTP is an application-layer protocol that defines how clients and servers communicate using requests and responses.

When a browser accesses a traditional HTTP URL, DNS resolves the hostname, TCP establishes a connection, the browser creates an HTTP request, and the HTTP bytes are transported through TCP/IP to the server. The server processes the request and sends an HTTP response back through the same networking layers.

HTTP/1.1 and HTTP/2 traditionally use TCP. HTTP/3 uses QUIC over UDP, combining UDP's lightweight packet transport with a modern transport protocol that provides reliability, congestion control, encryption, and multiplexed streams.

## Key Takeaways

1. HTTP is an application-layer protocol.
2. HTTP defines the meaning and structure of requests and responses.
3. TCP provides reliable byte transport for traditional HTTP/1.1 and HTTP/2.
4. HTTP requests contain methods, paths, headers, and optionally a body.
5. HTTP responses contain status codes, headers, and optionally a body.
6. HTTP is stateless by itself.
7. HTTPS is HTTP secured with TLS.
8. HTTP/2 provides multiplexing over TCP.
9. HTTP/3 uses QUIC over UDP.
10. A web page usually requires multiple HTTP requests.

## Reflection Questions

1. What is the difference between an HTTP request and a TCP connection?
2. Why does HTTP need status codes if TCP already provides reliable delivery?
3. Why is HTTP called stateless?
4. Explain the complete journey of `http://example.com` from browser to server and back.
5. Why might HTTP/3 use QUIC over UDP instead of TCP?

## What's Next

Lesson 17 — HTTP Requests and Responses in Depth

We will inspect HTTP messages in detail and study headers, cookies, content negotiation, request bodies, authentication, caching, idempotency, and safe HTTP methods using practical tools such as `curl` and browser developer tools.
