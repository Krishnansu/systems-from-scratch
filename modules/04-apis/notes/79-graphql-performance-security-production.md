# Lesson 79 — GraphQL Performance, Security & Production Design

## Objectives
- Identify expensive GraphQL query patterns and bound request cost.
- Apply authorization at resource and field boundaries.
- Design safe caching and useful production observability.

## Concept Summary
GraphQL production safety requires controlling the work each operation can trigger, enforcing authorization independently of schema validation, managing cache correctness, and instrumenting resolvers and dependencies.

## Core Ideas
- Depth, breadth, and complexity limits address different query-cost risks.
- Enforce server-side pagination caps, deterministic ordering, and suitable indexes.
- Aliases and nested lists can increase work within a single HTTP request.
- Authentication identifies the caller; authorization determines permitted actions and data. Schema validation does not grant access.
- Apply tenant scoping and field-level permissions where required.
- DataLoader helps compatible key-based batching but does not eliminate all expensive data access.
- Cache keys, scope, freshness, and invalidation must reflect authorization and correctness requirements.
- Timeouts must be supported by execution and downstream layers; an HTTP timeout alone may not cancel backend work.
- Observe operation latency, resolver timings, database queries, batch efficiency, response size, errors, and resource saturation.
- Persisted queries and introspection policies are not substitutes for authorization or resource limits.

## Practical Example
```graphql
query {
  product(id: "p1") {
    reviews(first: 20, after: null) {
      edges {
        node { id }
      }
    }
  }
}
```
Validate page sizes on the server, authorize access, use bounded and indexed retrieval, and instrument resolver and database behavior.

## Production Perspective
- Combine query-cost limits with page caps, timeouts, concurrency controls, and rate limits.
- Avoid shared-cache leaks across users or tenants.
- Do not log sensitive variables or credentials.
- Diagnose bottlenecks using traces and metrics before scaling infrastructure.

## Common Mistakes
- Assuming fewer HTTP requests means less backend work.
- Relying on depth limits alone.
- Treating authentication as authorization.
- Assuming caches are always safe or fresh.
- Assuming a request timeout automatically cancels downstream work.

## Key Takeaways
1. Bound work per operation, not just request volume.
2. Enforce authorization independently of query validation.
3. Treat caching as a correctness and security decision.
4. Use observability to locate real bottlenecks.

## Reflection Questions
1. Why can a shallow query still be expensive?
2. How do authentication and authorization differ?
3. When can shared caching leak data across tenants?
4. Why might a timeout leave backend work running?
5. Which metrics distinguish N+1 behavior from slow dependencies?

## Related Lessons
- Lesson 77 — GraphQL Fundamentals
- Lesson 78 — GraphQL Execution, Resolvers & DataLoader
- Next: Lesson 80 — API Rate Limiting, Quotas & Abuse Prevention
