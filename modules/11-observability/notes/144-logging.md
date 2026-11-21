# Lesson 144 — Logging

## Objectives
- Understand why logging is essential for production debugging.
- Distinguish log levels and structured vs unstructured logging.
- Design useful contextual log events.
- Understand centralized logging and Kubernetes log collection.
- Apply safe, cost-conscious logging practices.

## Concept Summary
Logging records events occurring within an application or system. Production logging captures structured, contextual events that help engineers investigate failures, understand behavior, and audit operations.

## Core Ideas
- **Log levels:** DEBUG (diagnostic detail), INFO (normal events), WARN (unexpected/recoverable), ERROR (operation failure), FATAL/CRITICAL (severe system failure; framework-dependent).
- **Structured logging:** Prefer machine-readable fields such as timestamp, level, service, event, request ID, trace ID, error code, and duration over a single unstructured string.
- **Context:** Include relevant request, workflow, and entity identifiers to help connect events. Propagate correlation context across service and messaging boundaries.
- **Distributed logging:** A request may produce events across multiple services. Correlation identifiers allow related logs to be searched together.
- **Centralized collection:** Applications commonly emit to stdout/stderr; runtime captures logs; collectors forward them to centralized storage/search systems.
- **Kubernetes:** Node-level collectors are often deployed as DaemonSets to collect container logs and forward them centrally.
- **Common tools:** Fluent Bit, Fluentd, Vector, Elasticsearch, OpenSearch, Loki, Kibana, Grafana.
- **Log quality:** Useful logs should describe what happened, where, why, and with relevant context—without excessive noise.
- **Security:** Avoid secrets, tokens, passwords, payment data, and unnecessary sensitive personal information. Apply access controls and retention.
- **Operational trade-offs:** Too little logging reduces evidence; too much increases cost, noise, and privacy risk.
- **Error handling:** Avoid silently swallowing exceptions. Log where useful context or handling decisions are added; avoid duplicate logging at every layer.
- **Observability signals:** Logs explain individual events; metrics quantify behavior; traces show request paths and time spent across operations.

## Practical Example
A payment failure log should include relevant fields such as service, event, order ID, payment attempt ID, request/trace IDs, duration, and error code rather than only `Payment failed`.

## Production Perspective
Treat logging as a production feature. Design consistent event schemas, propagate correlation context, collect centrally, control access and retention, and ensure log volume remains useful and affordable.

## Common Mistakes
- Logging vague messages without context.
- Using inconsistent or incorrect log levels.
- Logging sensitive data or secrets.
- Excessive logging that creates noise and cost.
- Swallowing exceptions silently.
- Logging the same error redundantly at every layer.
- Assuming local container logs provide sufficient long-term centralized observability.

## Key Takeaways
- Logs are evidence of events in a running system.
- Structured, contextual logs make production investigation faster.
- Centralized collection is essential across distributed infrastructure.
- Correlation IDs connect activity across services.
- Logging must balance usefulness, volume, security, and retention.
- Logs, metrics, and traces complement one another.

## Reflection Questions
1. Why are logs important if metrics are already available?
2. What is the difference between INFO, WARN, and ERROR?
3. Why is structured logging preferable to a formatted string?
4. How can you trace a request across five microservices using logs?
5. What is a correlation ID? Is it the same as a trace ID?
6. Why do containers commonly emit logs to stdout/stderr?
7. What role does a DaemonSet play in Kubernetes logging?
8. Why is logging full request payloads dangerous?
9. Why can logging the same exception at every layer be harmful?
10. How would you improve logs that report an API failure without identifying the downstream service?

## Related Lessons
- Lesson 123 — API Gateway
- Lesson 126 — Service Mesh
- Lesson 140 — Kafka
- Lesson 141 — Event-Driven Architecture

## What's Next
Lesson 145 — Metrics.
