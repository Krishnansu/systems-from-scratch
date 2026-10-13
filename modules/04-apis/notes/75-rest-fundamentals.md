# Lesson 75 — REST Fundamentals

## Objectives
- Explain REST as an architectural style.
- Distinguish resources from representations.
- Apply HTTP method semantics to resource-oriented endpoints.
- Understand REST constraints, safety, and idempotency.

## Concept Summary
REST (Representational State Transfer) is an architectural style for distributed systems. Web APIs commonly use HTTP to expose resources through identifiers and exchange resource representations. An HTTP + JSON API is not automatically fully RESTful; REST is defined by architectural constraints.

## Core Ideas
- Resource: a domain concept such as a task, order, or user. It is not necessarily a database row.
- Representation: data describing a resource, commonly JSON.
- Resource-oriented URLs identify collections and individual resources.
- REST constraints: client-server, statelessness, cacheability, uniform interface, layered system, and optional code-on-demand.
- Statelessness means requests carry the context needed to be understood; it does not mean the server stores no application data.
- `GET` reads; `POST` commonly submits data or creates resources; `PUT` replaces or creates state at a target URI; `PATCH` partially modifies; `DELETE` removes a resource.
- Safe methods are intended not to modify resource state. Idempotent operations have the same intended effect when repeated.
- `GET`, `PUT`, and `DELETE` are idempotent by semantics; `POST` is not guaranteed idempotent; `PATCH` depends on the patch operation.
- A repeated `DELETE` can return a different response, such as 404, while remaining idempotent in intended state effect.
- Query parameters commonly express collection filtering, sorting, and pagination.
- REST conventions do not replace authentication, authorization, validation, or careful retry design.

## Practical Example
```http
GET /api/tasks/42
Accept: application/json
```

```json
{
  "id": 42,
  "title": "Learn REST",
  "completed": false
}
```

Partial update:
```http
PATCH /api/tasks/42
Content-Type: application/json

{"completed": true}
```

Collection filtering:
```http
GET /api/tasks?completed=false&limit=20
```

## System Mental Model
```text
Client
  -> resource identifier + HTTP method
  -> API gateway/proxy (optional)
  -> application service
  -> database or other dependencies
  -> response representation + status
```

REST does not require this exact deployment architecture.

## Production Perspective
- Method semantics help caches and clients reason about requests.
- A timeout does not prove a write failed; retries can create duplicate orders or payments unless deduplicated.
- Define filtering, pagination, error formats, and compatibility in the API contract.
- REST-style URL conventions alone do not ensure full REST compliance or security.

## Common Mistakes
- Treating REST as a protocol rather than an architectural style.
- Assuming HTTP + JSON automatically means fully RESTful.
- Confusing statelessness with absence of stored data.
- Treating PUT and PATCH as interchangeable.
- Assuming idempotency requires identical responses.
- Assuming every endpoint must be plain CRUD or that REST provides security automatically.

## Key Takeaways
1. REST organizes interactions around resources and representations.
2. Standard HTTP methods communicate intended behavior.
3. Safe and idempotent are distinct properties (safe describes whether a request intends to change resource state; idempotent describes whether repeating it has the same intended effect on state.)
4. Stateless interactions support independent request handling.
5. API contracts must explicitly define errors, validation, security, and compatibility.

## Reflection Questions
1. How does a resource differ from its JSON representation?
2. Why prefer `GET /api/tasks/42` over `GET /api/getTask/42`?
3. Why can DELETE be idempotent when a repeated request returns 404?
4. Why does statelessness not mean the server stores no data?
5. Why can blindly retrying a timed-out POST create duplicates?

## Related Lessons
- Lesson 74 — API Fundamentals
- Lessons 1–62 — Networking and HTTP foundations
- Next: Lesson 76 — REST API Design in Practice
