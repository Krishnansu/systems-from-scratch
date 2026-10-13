# Lesson 74 — API Fundamentals

## Objectives
- Explain APIs as interfaces between software components.
- Distinguish an API, HTTP, a backend service, and a client.
- Understand endpoints, resources, requests, responses, and API contracts.
- Trace a basic API call through a backend.

## Concept Summary
An API (Application Programming Interface) defines how software components interact. A web API commonly uses HTTP to exchange requests and responses, while its contract describes available operations, inputs, outputs, errors, and compatibility expectations.

## Core Ideas
- An API exposes a defined interaction boundary without requiring clients to know the internal implementation.
- HTTP is a protocol often used by web APIs; it is not synonymous with API.
- A backend service implements functionality exposed through an API.
- A client may be a browser, mobile app, partner integration, or another service.
- An endpoint is commonly described by an HTTP method and path.
- A resource is a domain concept, such as an order or task.
- The API contract describes operations, input validation, response formats, errors, and compatibility expectations.
- API consumers should not need direct access to the backend's database schema.
- API boundaries do not automatically provide security; authentication, authorization, and input validation are still necessary.

## Example
```http
GET /api/orders/123 HTTP/1.1
Host: shop.example.com
Accept: application/json
```

Possible response:
```http
HTTP/1.1 200 OK
Content-Type: application/json
```

```json
{
  "id": 123,
  "status": "shipped",
  "total": 1499
}
```

The client requests an order through the API. The backend validates the request, checks authorization, obtains the data, and returns a representation. The internal database and implementation remain hidden behind the interface.

## System Mental Model
```text
Client
  -> API contract (operation and expected behavior)
  -> HTTP request/response (web API transport)
  -> Backend implementation
  -> Database or other dependencies
  -> Response
```

This is a conceptual flow; real systems may involve gateways, caches, and multiple services.

## Production Perspective
- Multiple clients can use the same API contract.
- Backend internals can change while the API remains compatible.
- Renaming fields or changing error behavior can break existing clients.
- Contract tests and clear documentation help teams develop independently.
- A successful network connection does not guarantee a successful API operation.

## Common Mistakes
- Treating API and HTTP as the same thing.
- Confusing an API contract with its backend implementation.
- Assuming an endpoint is defined by a path alone, without its method and expected behavior.
- Assuming an API is secure merely because internal details are hidden.
- Making incompatible response changes without considering existing consumers.

## Key Takeaways
1. An API is an agreed interface between software components.
2. HTTP is one common protocol for exposing APIs.
3. Endpoints expose operations over resources or capabilities.
4. The contract enables independent implementation and evolution.
5. Security and compatibility must be designed explicitly.

## Reflection Questions
1. What does HTTP contribute when building a web API?
2. Why should a mobile app use an Orders API rather than connect directly to its database?
3. What can break if a response field is renamed?
4. How does an endpoint differ from a resource?
5. Does HTTP 404 necessarily mean the server is down? Why or why not?

## Related Lessons
- Lessons 1–62 — Networking and HTTP foundations
- Lessons 63–73 — Linux foundations
- Next: Lesson 75 — REST Fundamentals
