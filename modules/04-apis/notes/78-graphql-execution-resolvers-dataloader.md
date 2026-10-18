# Lesson 78 — GraphQL Execution, Resolvers & DataLoader

## Objectives
- Trace GraphQL field execution and understand resolver arguments.
- Explain the N+1 problem and batching with DataLoader.
- Understand request-scoped caching, execution order, and null propagation.

## Concept Summary
GraphQL executes a validated operation by resolving its requested fields. Resolvers obtain values from databases, caches, services, parent objects, or calculations. Naive nested resolvers can trigger the N+1 problem; batching and request-scoped caching reduce redundant data access.

## Core Ideas
- Resolver arguments commonly include `parent`, `args`, `context`, and `info`.
- Parent values connect nested field resolution; context often carries authenticated identity and service dependencies.
- A collection query followed by one related lookup per item causes N+1 behavior.
- DataLoader batches keys and caches repeated loads within its instance, commonly one instance per request.
- Batch functions must return one result per requested key in the same order, accounting for missing records.
- Query sibling fields may execute in parallel; top-level mutation fields execute serially. Serial execution does not guarantee a transaction.
- A null result for a non-null field propagates to the nearest nullable boundary and can invalidate parent objects or list results.
- DataLoader is not authorization, a database index, or a universal solution for every query pattern.

## Practical Example
```javascript
const resolvers = {
  Query: {
    tasks: (_, args, context) => context.taskRepository.findAll()
  },
  Task: {
    owner: (task, args, context) =>
      context.loaders.userById.load(task.ownerId)
  }
};
```

## System Mental Model
```text
Operation + variables
  -> parse and validate
  -> root resolver loads collection
  -> nested resolvers request related values
  -> DataLoader batches keys
  -> data sources return values
  -> GraphQL assembles response and execution errors
```

## Production Perspective
- Prefer bulk queries, joins, or DataLoader when they fit the data-access pattern.
- Create request-scoped loaders when cached data may depend on identity or authorization.
- Preserve key-to-result ordering and handle missing records consistently.
- Enforce authorization in the relevant resolver/service/data-access boundary.
- Monitor resolver latency, database query counts, batching efficiency, and errors.

## Common Mistakes
- Assuming one GraphQL request equals one database query.
- Returning batch results in database order rather than requested-key order.
- Sharing authorization-sensitive loader caches across requests.
- Assuming serial mutation execution implies transactionality.
- Forgetting how non-null declarations affect error propagation.

## Key Takeaways
1. Resolvers connect fields to data sources and parent values.
2. N+1 is a data-access pattern, not an inherent requirement of GraphQL.
3. DataLoader batches and caches key-based lookups.
4. Correctness, authorization, nullability, and observability remain application responsibilities.

## Reflection Questions
1. When might a SQL join be preferable to DataLoader?
2. Why must batch results preserve key order?
3. Why are request-scoped loaders often safer?
4. How does non-null affect error propagation?
5. How would you diagnose high database load on a GraphQL endpoint?

## Related Lessons
- Lesson 77 — GraphQL Fundamentals
- Next: Lesson 79 — GraphQL Performance, Security & Production Design
