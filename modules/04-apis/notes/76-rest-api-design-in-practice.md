# Lesson 76 — REST API Design in Practice

## Objectives
- Design resource-oriented REST endpoints.
- Choose appropriate HTTP status codes and error formats.
- Understand filtering, pagination, and cursor-based navigation.
- Recognize backward-compatibility risks in API evolution.
- Connect API design decisions to production reliability and security.

## Concept Summary
REST API design translates domain concepts into stable HTTP contracts. Good APIs use predictable resource identifiers, clear method semantics, consistent errors, validated query parameters, and explicit compatibility rules. Production quality also depends on authorization, observability, and efficient data access.

## Core Ideas
- Model domain resources, not implementation actions: prefer `/api/tasks/42` over `/api/getTask/42`.
- Use collection routes such as `/api/tasks` and item routes such as `/api/tasks/42`.
- Use nested routes when the relationship matters, e.g. `/api/users/7/tasks`; avoid excessive nesting that couples clients to internal structure.
- Use query parameters for filtering, sorting, and pagination. Validate values and allowlist sortable fields.
- Common status codes: `200 OK`, `201 Created`, `204 No Content`, `400 Bad Request`, `401 Unauthorized`, `403 Forbidden`, `404 Not Found`, `409 Conflict`, `422 Unprocessable Content`, `500 Internal Server Error`, and `503 Service Unavailable`.
- A successful creation commonly returns `201 Created` and may include a `Location` header.
- Use a consistent, machine-readable error contract. RFC 9457 Problem Details (`application/problem+json`) is one standard option. Never expose stack traces, secrets, or internal database details.
- Offset pagination (`limit` and `offset`) is simple but can become expensive for deep pages and can shift as records change.
- Cursor pagination uses a server-issued opaque cursor to continue from a stable position. Use deterministic ordering, often with a unique tie-breaker. Cursor pagination alone does not guarantee snapshot consistency.
- Validate page sizes and cursors; use parameterized queries and appropriate indexes.
- API versioning can help manage incompatible changes, but does not replace backward-compatible contract design and a deprecation plan.
- Additive response fields are often compatible, but strict clients may still break. Removing fields, changing types or semantics, or making optional request fields required can be breaking changes.
- Knowing a resource ID does not grant permission to access it. Enforce authorization on the server; `404` may be used instead of `403` when concealing resource existence is intentional.

## Practical Example
List a user's incomplete tasks:
```http
GET /api/v1/users/7/tasks?completed=false&limit=20
```

Continue with a server-issued cursor:
```http
GET /api/v1/users/7/tasks?completed=false&limit=20&cursor=opaque-token
```

Create a task:
```http
POST /api/v1/tasks
Content-Type: application/json

{"title": "Learn REST API design"}
```

A successful creation can return:
```http
HTTP/1.1 201 Created
Location: /api/v1/tasks/43
Content-Type: application/json
```

## System Mental Model
```text
Client
  -> optional gateway/proxy
  -> authentication and authorization
  -> request validation and API handler
  -> database or downstream dependency
  -> status code, headers, and response body
```

## Production Perspective
- Define status codes and error schemas consistently across endpoints.
- Apply authorization at the resource/action boundary, not merely in the UI.
- Use deterministic ordering and suitable indexes for paginated queries.
- Track request IDs, latency, error rates, and dependency failures.
- A timeout does not prove a write failed; design retry and idempotency behavior deliberately.
- Document versioning, compatibility, and deprecation policies.

## Common Mistakes
- Designing action-centric URLs instead of resource-oriented routes.
- Using deeply nested URLs that expose unnecessary internal relationships.
- Treating `401` and `403` as interchangeable.
- Returning inconsistent error bodies or leaking internal exception details.
- Using unbounded page sizes or arbitrary user-controlled sort expressions.
- Assuming offset pagination remains stable while records change.
- Assuming API versioning automatically prevents breaking changes.

## Key Takeaways
1. URLs identify resources; HTTP methods describe intended operations.
2. Status codes and error bodies are part of the public API contract.
3. Cursor pagination is useful for large or frequently changing collections when designed with stable ordering.
4. Validation, authorization, observability, and database performance are part of API design.
5. Compatibility requires deliberate evolution and deprecation, not just version numbers.

## Reflection Questions
1. When would you choose a nested route instead of a top-level resource route?
2. When should an API return `400`, `401`, `403`, `404`, or `409`?
3. Why can offset pagination skip or repeat records when data changes?
4. What makes a cursor opaque, and why should ordering be deterministic?
5. Which API changes can break existing clients even if the endpoint URL stays the same?

## Related Lessons
- Lesson 74 — API Fundamentals
- Lesson 75 — REST Fundamentals
- Next: Lesson 77 — GraphQL Fundamentals
