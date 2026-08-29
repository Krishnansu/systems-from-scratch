# Lesson 25 - Inspecting HTTPS with Python

## Objectives

- Observe the HTTPS connection process using Python.
- Connect DNS, TCP, TLS and HTTP into one concrete flow.
- Inspect the negotiated TLS version and cipher.
- Inspect the server certificate.
- Send a raw HTTP request through a TLS connection.
- Understand where HTTP sits relative to TLS and TCP.

## Concept Summary

HTTPS is not a replacement for HTTP. It is HTTP carried through a secure TLS connection.

```text
HTTP
  ↓
TLS
  ↓
TCP
  ↓
IP
  ↓
Network
```

A simplified HTTPS journey is:

```text
DNS
  ↓
TCP connection
  ↓
TLS handshake
  ↓
Secure TLS connection
  ↓
HTTP request
  ↓
HTTP response
```

## Core Ideas

### 1. DNS Comes First

A hostname must be resolved before a connection can normally be established.

```text
example.com
     ↓
    DNS
     ↓
IP Address
```

Python's `socket.getaddrinfo()` can be used to observe the address resolution performed through the operating system's resolver machinery.

### 2. TCP Creates the Transport Connection

Python can explicitly create a TCP connection using:

```python
socket.create_connection((host, 443))
```

Conceptually:

```text
Client                         Server

SYN -------------------------->
     <------------------- SYN-ACK
ACK -------------------------->

      TCP Connection
```

At this point there is a reliable ordered TCP byte stream, but there is not yet an encrypted HTTPS session.

### 3. TLS Runs Over TCP

Python's SSL library can wrap the TCP socket:

```python
context = ssl.create_default_context()

tls_sock = context.wrap_socket(
    sock,
    server_hostname=host
)
```

This initiates the TLS handshake.

```text
TCP Connection
      ↓
TLS Handshake
      ↓
Certificate
      ↓
Certificate Verification
      ↓
Key Exchange
      ↓
Traffic Keys
      ↓
Secure TLS Connection
```

### 4. Certificate

The server certificate allows the client to authenticate the server's identity and obtain the server's public key information.

Python can inspect the peer certificate using:

```python
tls_sock.getpeercert()
```

A certificate contains information such as:

- Subject
- Issuer
- Validity period
- Subject alternative names
- Public key information

### 5. TLS Version and Cipher

The negotiated TLS version can be inspected with:

```python
tls_sock.version()
```

The negotiated cipher information can be inspected with:

```python
tls_sock.cipher()
```

The exact values depend on what the client and server support and negotiate.

### 6. HTTP Is Sent Through TLS

Once TLS is established, the application can send an HTTP request:

```python
request = (
    "GET / HTTP/1.1\r\n"
    "Host: example.com\r\n"
    "Connection: close\r\n"
    "\r\n"
)

tls_sock.sendall(request.encode())
```

The important relationship is:

```text
HTTP Request
     ↓
TLS Encryption
     ↓
TCP Byte Stream
     ↓
IP Packets
     ↓
Network
```

TCP does not understand that the bytes represent an HTTP request. TLS protects the bytes, while TCP transports them reliably.

### 7. Receiving the Response

The response can be read from the TLS socket:

```python
response = b""

while True:
    data = tls_sock.recv(4096)

    if not data:
        break

    response += data
```

The conceptual reverse path is:

```text
Network
   ↓
IP
   ↓
TCP
   ↓
TLS Decryption
   ↓
HTTP Response
   ↓
Python Program
```

## Practical Example

A minimal HTTPS inspection program can combine all of these steps:

```python
import socket
import ssl

host = "example.com"
port = 443

sock = socket.create_connection((host, port))

context = ssl.create_default_context()
tls_sock = context.wrap_socket(
    sock,
    server_hostname=host
)

print("TLS version:", tls_sock.version())
print("Cipher:", tls_sock.cipher())
print("Certificate:")
print(tls_sock.getpeercert())

request = (
    "GET / HTTP/1.1\r\n"
    "Host: example.com\r\n"
    "Connection: close\r\n"
    "\r\n"
)

tls_sock.sendall(request.encode())

while True:
    data = tls_sock.recv(4096)

    if not data:
        break

    print(data.decode(errors="replace"), end="")

tls_sock.close()
```

## Production Perspective

In production applications, developers normally do not manually perform these steps. Libraries and operating-system networking stacks handle DNS, TCP and TLS details.

For example, a high-level HTTP client can hide the entire process behind a simple request such as:

```python
requests.get("https://example.com")
```

The lower-level experiment is valuable because it exposes what the abstraction is actually doing.

## Important Boundary

Keep these responsibilities separate:

```text
HTTP
 │
 │ Application semantics
 │ - GET
 │ - POST
 │ - Headers
 │ - Status codes
 │
 ▼
TLS
 │
 │ Security
 │ - Encryption
 │ - Authentication
 │ - Integrity
 │
 ▼
TCP
 │
 │ Transport
 │ - Ordered bytes
 │ - Reliability
 │ - Retransmission
 │
 ▼
IP
 │
 │ Routing
 │ - Source IP
 │ - Destination IP
 │
 ▼
Network
```

## Common Mistakes

### Mistake 1: Thinking TCP provides HTTPS security

TCP provides reliable byte transport. TLS provides encryption and authentication.

### Mistake 2: Thinking TLS replaces HTTP

TLS protects application traffic. HTTP remains the application protocol being transported.

### Mistake 3: Thinking `recv()` returns one HTTP response

TCP is still a byte stream. A response can arrive across multiple `recv()` calls.

### Mistake 4: Thinking Python implements TCP

Python exposes socket APIs. The operating system implements the TCP/IP networking stack underneath.

## Key Takeaways

- DNS resolves the hostname before connection establishment.
- TCP establishes the underlying reliable byte stream.
- TLS establishes a secure authenticated channel over TCP.
- HTTP requests are sent through the established TLS connection.
- TLS encrypts HTTP data before it is transported by TCP.
- Python's `ssl` module allows us to inspect the TLS connection directly.
- The certificate provides server identity information.
- TLS version and cipher are negotiated between client and server.
- HTTP, TLS, TCP and IP have different responsibilities.

## Reflection Questions

- Why must TCP be established before TLS in traditional HTTPS?
- What information does the certificate allow the client to verify?
- Does TCP know that the encrypted bytes originally represented HTTP?
- Why can one HTTP response require multiple `recv()` calls?
- What changes when HTTP/3 uses QUIC instead of TCP?

## Related Lessons

- Lesson 16 - How the Web Works: DNS, TCP, TLS and HTTP
- Lesson 18 - HTTP Request Journey Across All Layers
- Lesson 19 - Building a TCP/HTTP Server in Python
- Lesson 21 - HTTP/1.1 Persistent Connections and Buffer Management
- Lesson 22 - TLS Fundamentals
- Lesson 23 - TLS Handshake
