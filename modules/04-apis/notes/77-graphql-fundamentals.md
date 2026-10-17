# Lesson 77 — GraphQL Fundamentals

## Objectives
- Explain GraphQL's purpose and how it differs from REST.
- Understand schemas, types, fields, queries, and mutations.
- Trace GraphQL validation and field execution.
- Recognize production concerns around performance, security, and caching.

## Concept Summary
GraphQL is a query language for APIs and a runtime for executing queries against data. The server defines a typed schema; clients select the fields they need. Resolvers obtain field values from databases, caches, and downstream services. GraphQL commonly runs over HTTP but is not a database or transport protocol.

## Core Ideas
- Over-fetching means receiving unnecessary data; under-fetching means needing additional requests to obtain related data.
- GraphQL allows clients to select fields and nested relationships in an operation.
- The schema defines object types, fields, arguments, and nullability. `!` means non-null; `[Task!]!` means a non-null list of non-null tasks.
- `Query` defines read operations; `Mutation` defines state-changing operations.
- Variables make operations reusable and keep input values separate from query text.
- The server parses and validates an operation against the schema before executing it.
- Resolvers determine field values and can call different data sources. Request context commonly carries identity and service dependencies.
- GraphQL can reduce client round trips without reducing backend work.
- The N+1 problem occurs when a collection fetch is followed by a separate query for each item's related data. Batching and request-scoped caching, often with DataLoader, can reduce redundant calls.
- Schema validation does not replace authorization, safe data access, or input validation.
- Deep or broad nested queries can be expensive. Production systems may enforce query depth/complexity limits, pagination, timeouts, concurrency limits, and rate limits.
- HTTP caching is often less straightforward for POST-based GraphQL operations than for resource-oriented REST GET requests; GET queries and specialized caches are possible.
- Useful observability includes operation names, execution time, resolver/dependency latency, database query counts, and error rates.

## Practical Example
```graphql
query GetTask($taskId: ID!) {
  task(id: $taskId) {
    title
    completed
    owner {
      name
    }
  }
}
```

Variables:
```json
{"taskId": "42"}
```

Illustrative schema:
```graphql
type Task {
  id: ID!
  title: String!
  completed: Boolean!
}

type Query {
  task(id: ID!): Task
}
```

## System Mental Model
```text
Client operation + variables
  -> parse and validate against schema
  -> execute fields through resolvers
  -> databases, caches, and downstream services
  -> assemble requested response shape
```

## Production Perspective
- Enforce authorization for requested resources and nested fields.
- Prevent N+1 access patterns with batching and appropriate data-access design.
- Bound query complexity, list sizes, execution time, and concurrency.
- Apply cache policies that respect user identity and data freshness.
- Instrument operations and dependencies without indiscriminately logging sensitive variables or responses.
- REST and GraphQL can coexist; choose based on client needs, caching, complexity, and operational trade-offs.

## Common Misconceptions
- GraphQL is a database or transport protocol.
- Every GraphQL request causes one database query.
- GraphQL always outperforms REST.
- Schema validation automatically makes an API secure.
- GraphQL completely eliminates over-fetching and under-fetching.

## Key Takeaways
1. The schema defines the API contract, not the storage architecture.
2. Queries read data; mutations change state.
3. Resolvers connect requested fields to their underlying data sources.
4. Flexible client selection shifts important responsibilities to server execution and query-cost management.
5. Authorization, caching, and observability remain essential in production.

## Reflection Questions
1. Why is the GraphQL schema independent of the database schema?
2. What happens when a query selects a field not defined by the schema?
3. How can one GraphQL request still trigger many backend queries?
4. Why is authorization needed for nested fields?
5. What factors influence choosing REST versus GraphQL for a public API?

## Related Lessons
- Lesson 74 — API Fundamentals
- Lesson 75 — REST Fundamentals
- Lesson 76 — REST API Design in Practice
- Next: Lesson 78 — GraphQL Execution, Resolvers & DataLoader
