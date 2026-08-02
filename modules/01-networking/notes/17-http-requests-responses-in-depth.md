# HTTP Requests and Responses in Depth

HTTP is an application-layer protocol used to exchange messages between clients and servers.

A typical HTTP interaction looks like:

```text
Client
   │
   │ HTTP Request
   ▼
Server
   │
   │ HTTP Response
   ▼
Client
```

An HTTP request and response are both HTTP messages.

```text
HTTP Message
      │
      ├── Start Line
      │
      ├── Headers
      │
      └── Body (optional)
```

---

## 1. HTTP Request Structure

Example:

```http
POST /users HTTP/1.1
Host: api.example.com
Content-Type: application/json
Authorization: Bearer abc123
Accept: application/json

{
    "name": "Krishnansu",
    "age": 24
}
```

An HTTP request contains:

```text
Request
   │
   ├── Request Line
   │
   ├── Headers
   │
   └── Body (optional)
```

### Request Line

```text
POST /users HTTP/1.1
 │      │       │
 │      │       └── HTTP Version
 │      │
 │      └── Resource Path
 │
 └── HTTP Method
```

The request line contains:

- HTTP method
- Resource path
- HTTP version

---

## 2. HTTP Methods

HTTP methods describe the intended operation.

### GET

Used to retrieve a resource.

```http
GET /users
```

or:

```http
GET /users/123
```

Meaning:

> Give me the users or user 123.

---

### POST

Usually used to create a new resource or trigger an operation.

```http
POST /users
```

Body:

```json
{
    "name": "Krishnansu",
    "age": 24
}
```

The server may respond:

```http
HTTP/1.1 201 Created
```

---

### PUT

Generally used to replace the representation of a resource.

```http
PUT /users/123
```

Body:

```json
{
    "name": "Krishnansu",
    "age": 25
}
```

Conceptually:

> Make resource 123 look like this.

PUT is generally idempotent.

---

### PATCH

Used to partially modify a resource.

```http
PATCH /users/123
```

Body:

```json
{
    "age": 25
}
```

Conceptually:

> Change only the specified parts.

PATCH is not necessarily idempotent.

---

### DELETE

Used to delete a resource.

```http
DELETE /users/123
```

DELETE is generally idempotent.

---

## 3. HTTP Headers

Headers carry metadata about an HTTP request or response.

Common request headers include:

```text
Host
Content-Type
Accept
Authorization
Cookie
```

### Host

```http
Host: api.example.com
```

Identifies the host the client wants to communicate with.

Multiple websites can share the same IP address, so the hostname helps the server determine which site the request is intended for.

---

### Content-Type

```http
Content-Type: application/json
```

Describes the format of the body that is actually being sent.

Examples:

```text
application/json
text/html
text/plain
application/xml
image/png
```

Important distinction:

```text
Content-Type
      │
      └── What format is the body actually in?
```

---

### Accept

```http
Accept: application/json
```

Expresses the client's preferred response representation.

Important:

> Accept is a preference, not an absolute command.

A server may:

1. Return JSON if it supports it.
2. Return another representation.
3. Return `406 Not Acceptable` if it cannot provide an acceptable representation.

The actual response format is described by the response's `Content-Type` header.

```text
Client
   │
   │ Accept: application/json
   ▼
Server
   │
   │ Content-Type: application/json
   ▼
Client
```

---

### Authorization

Example:

```http
Authorization: Bearer abc123
```

Used to send authentication credentials or tokens.

The server can use the token to determine:

- Who the user is.
- Whether the credential is valid.
- What permissions the user has.

---

### Cookie

Example:

```http
Cookie: session_id=abc123
```

Cookies allow the client to carry information between otherwise independent HTTP requests.

---

## 4. HTTP Request Body

The request body contains the data being sent to the server.

Example:

```http
POST /users HTTP/1.1
Content-Type: application/json

{
    "name": "Krishnansu",
    "age": 24
}
```

The body is:

```json
{
    "name": "Krishnansu",
    "age": 24
}
```

Request bodies are commonly used with:

- POST
- PUT
- PATCH

GET requests generally do not require a request body.

---

## 5. HTTP Response Structure

Example:

```http
HTTP/1.1 201 Created
Content-Type: application/json
Location: /users/123

{
    "id": 123,
    "name": "Krishnansu",
    "age": 24
}
```

An HTTP response contains:

```text
Response
   │
   ├── Status Line
   ├── Headers
   └── Body (optional)
```

The status line contains:

```text
HTTP/1.1 201 Created
    │      │      │
    │      │      └── Reason Phrase
    │      │
    │      └── Status Code
    │
    └── HTTP Version
```

---

## 6. HTTP Status Codes

Status codes communicate the result of a request.

```text
2xx → Success
3xx → Redirection
4xx → Client Error
5xx → Server Error
```

Common examples:

### 200 OK

The request was successfully processed.

### 201 Created

A new resource was successfully created.

### 400 Bad Request

The request was invalid or malformed.

### 401 Unauthorized

Authentication is missing or invalid.

Think:

> Who are you?

### 403 Forbidden

The client is authenticated but does not have permission to perform the operation.

Think:

> I know who you are, but you cannot do this.

### 404 Not Found

The requested resource does not exist.

### 406 Not Acceptable

The server cannot provide a representation acceptable according to the client's `Accept` header.

### 429 Too Many Requests

The client has sent too many requests in a given period.

Often associated with rate limiting.

### 500 Internal Server Error

The server encountered an unexpected error while processing the request.

---

## 7. Cookies and HTTP Statelessness

HTTP itself is stateless.

This means that each HTTP request is conceptually independent. HTTP does not automatically remember that two requests came from the same user.

However, applications often need state.

For example:

```text
User logs in
     │
     ▼
GET /profile
     │
     ▼
GET /orders
     │
     ▼
GET /cart
```

The server needs a way to associate these requests with the same user.

One common mechanism is cookies.

After login, the server may send:

```http
Set-Cookie: session_id=abc123
```

The browser stores the cookie.

Later:

```http
GET /profile
Cookie: session_id=abc123
```

The server can use the session ID to find the associated session.

```text
Session ID
    │
    ▼
abc123
    │
    ▼
Session Store
    │
    ▼
User = Krishnansu
```

Important distinction:

> Cookies do not make HTTP stateful. Cookies carry state between otherwise independent HTTP requests.

A common server-side session architecture is:

```text
Browser
    │
    │ Cookie: session_id=abc123
    ▼
Server
    │
    │ Lookup session
    ▼
Session Store
    │
    ▼
User Information
```

The browser may only store the session identifier while the actual session data remains on the server.

---

## 8. Authentication vs Authorization

These are different concepts.

### Authentication

Answers:

> Who are you?

Example:

```text
Bearer Token
     │
     ▼
Is it valid?
     │
     ▼
User = Krishnansu
```

### Authorization

Answers:

> What are you allowed to do?

Example:

```text
User
 │
 ├── Read Posts       ✓
 ├── Create Posts     ✓
 └── Delete Users     ✗
```

Summary:

```text
Authentication
      │
      └── Who are you?

Authorization
      │
      └── What are you allowed to do?
```

---

## 9. JSON and Content Types

Modern APIs commonly exchange JSON.

Example:

```json
{
    "id": 123,
    "name": "Krishnansu",
    "skills": [
        "C++",
        "Python",
        "Go"
    ]
}
```

HTTP itself does not require JSON.

HTTP can transport:

- HTML
- JSON
- XML
- Images
- Videos
- PDFs
- Binary data

HTTP transports bytes.

`Content-Type` tells the receiver how to interpret those bytes.

---

## 10. Content Negotiation

A client can express a preferred response format using `Accept`.

Example:

```http
Accept: application/json
```

The server may respond:

```http
Content-Type: application/json
```

The important distinction is:

```text
Accept
   │
   └── Client preference for response format

Content-Type
   │
   └── Actual format of the body being sent
```

`Accept` does not guarantee that the server must return that format.

If the server cannot provide an acceptable representation, it may return:

```http
406 Not Acceptable
```

Real-world APIs may also ignore the `Accept` header or return a default representation depending on their implementation.

---

## 11. Safe HTTP Methods

A safe method is one where the client does not request a state-changing operation.

Common safe methods include:

```text
GET
HEAD
OPTIONS
```

For example:

```http
GET /users
```

should retrieve users rather than intentionally:

- Creating users.
- Modifying users.
- Deleting users.

Safe does not mean that the server cannot have side effects internally. It means the method's defined semantics do not request a state-changing operation.

---

## 12. Idempotency

An operation is idempotent if performing it multiple times has the same intended effect on the resource state as performing it once.

It does not mean that every response must be identical.

### PUT

Suppose:

```http
PUT /users/123
```

with:

```json
{
    "name": "Krishnansu",
    "age": 24
}
```

The intended state becomes:

```text
User 123
    │
    ├── Name = Krishnansu
    └── Age = 24
```

Repeating the request still produces the same intended final state.

Therefore PUT is generally idempotent.

Conceptually:

```text
PUT
 │
 └── Set resource /users/123 to state X

Repeat
 │
 └── Set resource /users/123 to state X
```

Final state is still X.

---

### POST

Suppose:

```http
POST /orders
```

creates an order.

First request:

```text
Create Order #1001
```

Retry:

```text
Create Order #1002
```

The final state is different from performing the operation once.

Therefore POST is generally not idempotent.

Conceptually:

```text
PUT
 │
 └── Make this resource have this state

POST
 │
 └── Perform an operation / create something new
```

This distinction becomes extremely important when dealing with retries in distributed systems.

For example, imagine:

```text
Client
   │
   │ POST /payment
   ▼
Server
   │
   │ Payment processed
   ▼
Network Failure
```

The client does not know whether the payment was processed.

If it blindly retries, the payment might be processed twice.

Payment APIs therefore often use idempotency keys to make retrying certain operations safe.

---

## 13. Safe vs Idempotent

These concepts are different.

```text
Safe
 │
 └── Method semantics do not request state changes

Idempotent
 │
 └── Repeating the operation has the same intended effect
```

Typical properties:

| Method | Safe | Idempotent |
|--------|------|------------|
| GET | Yes | Yes |
| POST | No | Generally No |
| PUT | No | Yes |
| PATCH | No | Not necessarily |
| DELETE | No | Yes |

DELETE is a good example of an operation that is generally idempotent but not safe.

First:

```text
DELETE /users/123
→ User deleted
```

Second:

```text
DELETE /users/123
→ User already absent
```

The final intended state remains:

```text
User 123 does not exist
```

The responses can still differ, for example `204` followed by `404`.

---

## 14. HTTP Caching

HTTP caching allows clients and intermediate systems to reuse previously fetched responses.

For example:

```http
GET /logo.png
```

The server might respond:

```http
Cache-Control: max-age=3600
```

The browser can reuse the cached response for the specified period.

Instead of:

```text
Browser
   │
   │ Request
   ▼
Server
```

Every time, it can use:

```text
Browser
   │
   ▼
Browser Cache
   │
   ▼
Cached Response
```

Caching can reduce:

- Network traffic.
- Latency.
- Server load.

A production architecture may contain multiple caching layers:

```text
Browser Cache
      │
      ▼
CDN Cache
      │
      ▼
Reverse Proxy Cache
      │
      ▼
Application
      │
      ▼
Database
```

---

## 15. Complete HTTP Request Journey

Consider visiting:

```text
https://shop.example.com/products/123
```

The browser needs product 123.

The complete high-level journey is:

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

The request travels down the protocol stack:

```text
HTTP
  │
  ▼
TLS (HTTPS)
  │
  ▼
TCP
  │
  ▼
IP
  │
  ▼
Network / Link Layer
```

At the destination, the data is processed back up the stack:

```text
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
Application
```

The response follows the reverse path back to the browser.

---

## 16. Detailed End-to-End Example

Suppose the browser sends:

```http
GET /products/123 HTTP/1.1
Host: shop.example.com
Accept: application/json
Cookie: session_id=abc123
```

The browser first resolves:

```text
shop.example.com
       │
       ▼
142.250.x.x
```

A TCP connection is established:

```text
Client                         Server

   SYN ──────────────────────────►

       ◄──────────────────── SYN-ACK

   ACK ──────────────────────────►
```

Because HTTPS is being used, a TLS handshake establishes an encrypted channel.

The HTTP request is then passed to TCP.

TCP treats HTTP as a stream of bytes and adds its TCP header.

Conceptually:

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

The packet is carried through the network in link-layer frames.

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

Routers forward the packet toward the destination IP.

At the server, the stack processes the data in reverse:

```text
Network Frame
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
```

The HTTP server finally sees:

```http
GET /products/123 HTTP/1.1
Host: shop.example.com
Accept: application/json
Cookie: session_id=abc123
```

The application may perform:

```text
HTTP Request
      │
      ▼
Authentication
      │
      ▼
Authorization
      │
      ▼
Cache Check
      │
      ├── Cache Hit ──────► Return Product
      │
      ▼
Database
      │
      ▼
Product 123 Found
```

The server creates:

```http
HTTP/1.1 200 OK
Content-Type: application/json

{
    "id": 123,
    "name": "Laptop",
    "price": 75000
}
```

The response travels back through TCP, IP, and the network.

The browser receives the response and can use the JSON data.

---

## 17. HTTP vs HTTPS

For plain HTTP:

```text
HTTP
  │
  ▼
TCP
  │
  ▼
IP
  │
  ▼
Network
```

For HTTPS:

```text
HTTP
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
```

HTTPS is HTTP carried through a TLS-secured channel.

TLS provides properties such as:

- Encryption.
- Server authentication.
- Integrity protection.

---

## 18. HTTP/3 and QUIC

The exact transport stack depends on the HTTP version.

Traditional HTTP/1.1 and HTTP/2 commonly use TCP:

```text
HTTP/1.1 or HTTP/2
       │
       ▼
      TLS
       │
       ▼
      TCP
       │
       ▼
       IP
```

HTTP/3 uses QUIC over UDP:

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
```

QUIC provides transport features such as reliability, congestion control, and stream multiplexing while using UDP as its underlying datagram transport.

Therefore, the detailed journey described in this note is primarily the traditional HTTP-over-TCP model.

---

## 19. Inspecting HTTP with curl

Run:

```bash
curl -v https://example.com
```

Request lines are shown with `>`:

```text
> GET / HTTP/1.1
> Host: example.com
> User-Agent: curl/...
> Accept: */*
```

Response lines are shown with `<`:

```text
< HTTP/1.1 200 OK
< Content-Type: text/html
```

To inspect only response headers:

```bash
curl -I https://example.com
```

To inspect a JSON API:

```bash
curl -v https://jsonplaceholder.typicode.com/posts/1
```

To explicitly request JSON:

```bash
curl -H "Accept: application/json" \
     https://jsonplaceholder.typicode.com/posts/1
```

---

## 20. Browser DevTools

Browser DevTools provide a direct view of HTTP traffic.

Open DevTools with:

```text
F12
```

Then open:

```text
Network
```

Reload the page.

You can inspect:

- Request URL.
- Request Method.
- Status Code.
- Request Headers.
- Response Headers.
- Request Payload.
- Response Body.
- Cookies.

This provides a practical way to connect the HTTP theory to real network traffic.

---

# Key Mental Model

The most important model from this lesson is:

```text
                  APPLICATION
                      │
                      │ HTTP
                      ▼
                 HTTP Message
                      │
                      │ TLS (HTTPS)
                      ▼
                 Secure Channel
                      │
                      │ TCP
                      ▼
                 TCP Segments
                      │
                      │ IP
                      ▼
                  IP Packets
                      │
                      │ Network
                      ▼
                 Physical Journey
```

On the receiving side, the process is reversed:

```text
Network
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
Application
```

The exact transport depends on the HTTP version:

```text
HTTP/1.1 or HTTP/2
       │
       ▼
      TLS
       │
       ▼
      TCP
       │
       ▼
       IP
```

versus:

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
```

---

# Key Takeaways

1. An HTTP message contains a start line, headers, and an optional body.
2. HTTP methods communicate the intended operation.
3. `Content-Type` describes the body actually being sent.
4. `Accept` expresses the client's preferred response format; it does not guarantee that format.
5. Cookies carry state between otherwise independent HTTP requests.
6. Authentication answers: "Who are you?"
7. Authorization answers: "What are you allowed to do?"
8. PUT is generally idempotent because repeating it has the same intended effect on resource state.
9. POST is generally not idempotent because repeating it may create multiple resources or repeat an operation.
10. Safe and idempotent are different concepts.
11. HTTP caching reduces latency, network traffic, and server load.
12. HTTP messages are carried through lower networking layers such as TLS, TCP, IP, and the network/link layer.
13. For HTTPS over TCP, the conceptual stack is HTTP → TLS → TCP → IP → Network.
14. HTTP/3 uses HTTP → QUIC → UDP → IP.
15. Browser DevTools and `curl` allow direct inspection of HTTP requests and responses.

---

# Reflection Questions

1. What is the difference between `Content-Type` and `Accept`?
2. Why does HTTP need cookies if HTTP itself is stateless?
3. Why is PUT generally idempotent while POST is generally not?
4. Explain the complete journey of `GET /products/123` from browser to server and back through HTTP, TLS, TCP, IP, and the network layers.
5. What is the difference between a TCP segment and an IP packet?
6. Why does a router need the destination IP address but not the HTTP method?
7. How does the server know that `GET /products/123` is an HTTP request after the data reaches the server?
8. What changes in the protocol stack when moving from HTTP/2 over TCP to HTTP/3 over QUIC?

---

# Next Lesson

## Building an HTTP Server From Scratch

We will move from understanding HTTP conceptually to implementing a minimal HTTP server.

The basic flow will be:

```text
Client
   │
   │ TCP Connection
   ▼
Our Server
   │
   │ Read Raw Bytes
   ▼
Parse HTTP Request
   │
   ▼
Generate HTTP Response
   │
   ▼
Send Response
   │
   ▼
Client
```

The goal is to stop treating HTTP as a magical abstraction and understand what an HTTP server actually does internally.
