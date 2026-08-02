# HTTP Fundamentals

## Objectives

- Understand HTTP requests and responses.
- Understand methods, status codes and headers.
- Understand statelessness and cookies.
- Understand Accept and Content-Type.
- Understand idempotency of HTTP methods.

## Concept Summary

HTTP is an application-layer protocol used by clients and servers to communicate using structured requests and responses.

```text
Client
  |
  | HTTP Request
  v
Server
  |
  | HTTP Response
  v
Client
```

## HTTP Request

A request contains a request line, headers and optionally a body.

```http
GET /products/123 HTTP/1.1
Host: shop.example.com
Accept: application/json

```

The request line contains:

- Method: `GET`
- Target: `/products/123`
- HTTP version: `HTTP/1.1`

## HTTP Response

```http
HTTP/1.1 200 OK
Content-Type: application/json

{"id":123,"name":"Keyboard"}
```

A response contains:

- Status line
- Headers
- Optional body

## Accept vs Content-Type

`Accept` tells the server which response media types the client prefers.

`Content-Type` describes the media type of the message body being sent.

Sending:

```http
Accept: application/json
```

does not absolutely guarantee that the response will be JSON. The server may return another representation or an error depending on its implementation, content negotiation rules and available representations.

A response should accurately describe its body using `Content-Type`.

## HTTP Statelessness and Cookies

HTTP is stateless because each request can be understood independently at the protocol level. The server does not inherently remember previous requests.

Cookies add stateful application behaviour on top of stateless HTTP.

```text
Request 1
   |
   v
Server
   |
   | Set-Cookie
   v
Browser stores cookie
   |
   v
Request 2 + Cookie
   |
   v
Server identifies session
```

Cookies are commonly used for sessions, authentication and personalization.

## Idempotency

An operation is idempotent if repeating the same request has the same intended effect as performing it once.

`PUT` is generally idempotent because it commonly replaces or sets a resource to a specified representation.

```text
PUT /users/123
name = Alice

Repeat the request:

PUT /users/123
name = Alice

Final state remains the same.
```

`POST` is generally not idempotent because it commonly creates a new resource or triggers an operation each time.

```text
POST /orders
Create order

Repeat request:

POST /orders
Create another order
```

HTTP semantics define these general expectations, but actual application behaviour depends on server implementation. Idempotency keys can be used by APIs to make certain POST operations safely retryable.

## Key Takeaways

- HTTP defines application-level communication.
- `Accept` expresses preferred response formats.
- `Content-Type` describes the actual body representation.
- HTTP is stateless by design.
- Cookies provide a mechanism for maintaining application state across requests.
- PUT is generally idempotent.
- POST is generally non-idempotent.

## Reflection Questions

- Why should a server still validate and enforce the requested representation instead of blindly trusting Accept?
- Why is statelessness useful for scaling web servers?
- How can POST operations be made safe to retry?

## Related Lessons

- Lesson 16 - How the Web Works
- Lesson 18 - HTTP Request Journey Across Layers
