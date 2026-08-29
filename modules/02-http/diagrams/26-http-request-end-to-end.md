# HTTP Request End-to-End Journey

This is the most important diagram for understanding the complete journey of an HTTP request across the networking stack.

```text
Browser
   │
   │ https://shop.example.com/products/123
   ▼
DNS Resolution
   │
   ▼
IP Address Found
   │
   ▼
TCP Three-Way Handshake
   │
   ▼
TLS Handshake
   │
   ▼
Secure Connection Established
   │
   ▼
Browser Creates HTTP Request
   │
   │ GET /products/123
   ▼
HTTP
   │
   ▼
TCP
   │
   ▼
IP
   │
   ▼
Network / Wi-Fi
   │
   ▼
Routers
   │
   ▼
Server
   │
   ▼
IP
   │
   ▼
TCP
   │
   ▼
HTTP Server
   │
   ▼
Application
   │
   ▼
Database / Cache
   │
   ▼
Product 123 Found
   │
   ▼
HTTP 200 OK
   │
   ▼
TCP
   │
   ▼
IP
   │
   ▼
Network
   │
   ▼
Browser
   │
   ▼
HTTP Response
   │
   ▼
JSON Data
```

## Layer-by-Layer View

The request travels down the stack:

```text
Browser Application
       │
       │ HTTP Request
       ▼
     HTTP
       │
       │ HTTPS
       ▼
      TLS
       │
       ▼
      TCP
       │
       ▼
       IP
       │
       ▼
Network / Link Layer
       │
       ▼
Physical Network
```

At the destination, the server processes the data back up the stack:

```text
Physical Network
       │
       ▼
Network / Link Layer
       │
       ▼
       IP
       │
       ▼
      TCP
       │
       ▼
      TLS
       │
       ▼
     HTTP
       │
       ▼
Application Server
```

## Encapsulation

The HTTP request starts as application data:

```text
GET /products/123 HTTP/1.1
Host: shop.example.com
Accept: application/json
```

TCP treats it as bytes and adds a TCP header:

```text
┌───────────────────────────────┐
│ TCP Header                    │
├───────────────────────────────┤
│ HTTP Request Bytes            │
└───────────────────────────────┘
```

IP then encapsulates the TCP segment:

```text
┌───────────────────────────────┐
│ IP Header                     │
├───────────────────────────────┤
│ TCP Header                    │
├───────────────────────────────┤
│ HTTP Request Bytes            │
└───────────────────────────────┘
```

The network/link layer carries the IP packet in a frame:

```text
┌───────────────────────────────┐
│ Link / Wi-Fi Header           │
├───────────────────────────────┤
│ IP Header                     │
├───────────────────────────────┤
│ TCP Header                    │
├───────────────────────────────┤
│ HTTP Request Bytes            │
└───────────────────────────────┘
```

At the receiving server, the layers process the data in reverse.

```text
Frame
  │
  ▼
Remove Link Header
  │
  ▼
Process IP
  │
  ▼
Process TCP
  │
  ▼
Process TLS
  │
  ▼
HTTP Server Receives HTTP Bytes
```

## Response Journey

After the application finds product 123:

```http
HTTP/1.1 200 OK
Content-Type: application/json

{
    "id": 123,
    "name": "Laptop",
    "price": 75000
}
```

The response travels back through the stack:

```text
Application
    │
    ▼
HTTP Response
    │
    ▼
TLS
    │
    ▼
TCP
    │
    ▼
IP
    │
    ▼
Network
    │
    ▼
Internet Routers
    │
    ▼
Client Network
    │
    ▼
Browser
```

The browser ultimately receives the HTTP response and processes the JSON data.

## Important Note

This diagram represents the traditional HTTPS-over-TCP model used by HTTP/1.1 and HTTP/2.

HTTP/3 uses a different transport stack:

```text
HTTP/3
   │
   ▼
 QUIC
   │
   ▼
 UDP
   │
   ▼
 IP
   │
   ▼
 Network
```

The high-level application flow remains similar, but the transport layer is different.
