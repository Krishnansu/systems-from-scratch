# Lesson 141 — Event-Driven Architecture

## Objectives
- Explain Event-Driven Architecture (EDA).
- Distinguish commands from events.
- Understand producers, brokers, channels, and consumers.
- Compare event notification with event-carried state transfer.
- Explain eventual consistency, choreography, and orchestration.
- Understand event contracts, schema evolution, and the transactional outbox.

## Prerequisites
- Lesson 138 — Why Messaging?
- Lesson 139 — RabbitMQ
- Lesson 140 — Kafka

## Concept Summary
Event-Driven Architecture structures communication around business events. Producers publish facts about things that have happened, and independent consumers react to them. Brokers provide routing, buffering, persistence, and delivery capabilities depending on the technology. EDA reduces direct runtime coupling but introduces asynchronous consistency, event-contract, ordering, and operational concerns.

## Core Ideas
- **Event:** A fact that has already happened, usually named in the past tense (`OrderCreated`).
- **Command:** A request to perform an action (`CreateOrder`, `ReserveInventory`). Commands have an intended handler and can be rejected; events describe outcomes.
- **Producer:** Creates and publishes events.
- **Broker/channel:** Distributes events through topics, exchanges, queues, or subscriptions.
- **Consumer:** Independently processes events of interest.
- **Event notification:** Publishes a small event, often an identifier; consumers fetch additional state from the producer. This increases runtime dependency and can expose newer state than existed when the event occurred.
- **Event-carried state transfer:** Includes relevant business data in the event, reducing producer API calls but increasing payload size, duplication, and schema responsibilities.
- **Eventual consistency:** Services may temporarily observe different states and converge after successful processing and recovery. It is not an automatic guarantee of correctness.
- **Choreography:** Services react to events and publish subsequent events; workflow decisions are distributed.
- **Orchestration:** A coordinator explicitly manages workflow steps, results, and failures.
- **Event contract:** The schema and semantics consumers rely on. Prefer additive optional fields, defaults, stable meanings, and compatibility tests. Breaking changes may require versioning.
- **Transactional outbox:** Writes business data and an event record into the same database transaction. A relay or CDC process publishes outbox records to the broker.
- **Duplicate safety:** A relay may publish again after crashing between broker publication and marking an outbox row complete. Consumers need stable event IDs and idempotent processing.
- **Ordering:** Kafka guarantees order within a partition, not across a topic. A stable aggregate key such as `orderId` can preserve per-order order. Concurrent consumers, retries, and requeues can affect processing order elsewhere.
- **Observability:** Propagate correlation IDs or trace context across services and events to reconstruct workflows.

## Practical Example
An Order Service publishes `OrderCreated`. Payment, inventory, notification, and analytics services consume it independently. Each maintains its own processing state. The order workflow may pass through intermediate states such as `CREATED`, `INVENTORY_RESERVED`, `PAYMENT_PENDING`, and `CONFIRMED`.

## Production Perspective
Use synchronous calls when an immediate decision or response is required; use events for independent asynchronous reactions. Identify which business invariants require immediate consistency and which can tolerate eventual consistency. Minimize sensitive event data, evolve schemas compatibly, make consumers idempotent, plan for ordering and replay, and monitor end-to-end processing. Use an outbox or equivalent reliable publication mechanism when database updates and event publication must not diverge.

## Common Mistakes
- Treating commands and events as interchangeable.
- Assuming EDA means all communication must be asynchronous.
- Assuming a broker eliminates all service coupling.
- Assuming eventual consistency automatically guarantees convergence.
- Publishing directly after a database commit without handling the failure gap.
- Assuming an outbox provides exactly-once delivery.
- Making breaking event-schema changes without coordinating consumers.
- Assuming partition ordering creates global ordering across services.

## Key Takeaways
- Events are facts; commands are requests.
- Event-driven communication reduces direct runtime dependencies.
- Event payload design affects coupling and schema responsibilities.
- Eventual consistency must be an explicit business decision.
- Choreography and orchestration are alternative workflow coordination styles.
- The transactional outbox makes business updates and publication intent atomic, while consumers still need duplicate protection.

## Reflection Questions
1. Why is `OrderCreated` an event but `CreateOrder` a command?
2. Compare event notification and event-carried state transfer.
3. Why does EDA introduce eventual consistency?
4. How does choreography coordinate a workflow, and what are its scaling challenges?
5. Compare choreography and orchestration.
6. Why can an event field rename break independent consumers?
7. How does the transactional outbox work, and why can duplicates occur?
8. How can a partition key help preserve per-entity ordering?

## Related Lessons
- Lesson 138 — Why Messaging?
- Lesson 139 — RabbitMQ
- Lesson 140 — Kafka

## What's Next
Lesson 142 — Dead Letter Queues.
