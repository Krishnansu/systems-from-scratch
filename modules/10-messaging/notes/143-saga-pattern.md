# Lesson 143 — Saga Pattern

## Objectives
- Explain distributed transaction coordination challenges.
- Understand Saga as local transactions plus compensating transactions.
- Compare choreography and orchestration.
- Design durable, recoverable workflows.
- Handle retries, duplicate messages, ambiguous outcomes, and failed compensations.

## Prerequisites
- Lesson 132 — Transactions
- Lesson 138 — Why Messaging?
- Lesson 139 — RabbitMQ
- Lesson 140 — Kafka
- Lesson 141 — Event-Driven Architecture
- Lesson 142 — Dead Letter Queues

## Concept Summary
A Saga coordinates a business workflow spanning multiple services through a sequence of independently committed local transactions. If a later step cannot complete, compensating transactions counteract the business effects of previously completed steps. Compensation is a new business operation, not a database rollback, and may be partial or require manual intervention.

## Core Ideas
- **Distributed transaction problem:** A local database transaction cannot atomically commit or roll back independent service databases and arbitrary external providers.
- **Forward transaction:** Performs one business operation, such as reserving inventory or capturing payment.
- **Compensating transaction:** Counteracts an earlier operation, such as releasing a reservation or refunding a payment. It does not erase history and can itself fail.
- **Saga lifecycle:** Persist workflow identity, current state, completed steps, pending actions, compensation progress, and terminal outcome.
- **Choreography:** Services react to events and publish subsequent events. Workflow logic is distributed; simple flows are natural, but complex flows can become difficult to trace and change.
- **Orchestration:** A durable coordinator issues commands and consumes results. It centralizes workflow decisions and state. It can communicate asynchronously through a broker; orchestration does not require synchronous HTTP.
- **Failure classification:** Distinguish permanent business/technical failures from transient failures and ambiguous timeouts. Do not compensate until an uncertain operation's outcome is resolved where possible.
- **Idempotency:** Give each logical command/attempt a stable identifier. Enforce deduplication durably and atomically with the local business update. A repeated command should return the recorded outcome rather than repeat the side effect.
- **Durable recovery:** Persist Saga state and transitions. After a crash, resume from recorded state and reconcile operations whose outcome is unknown.
- **Outbox/inbox:** Use a transactional outbox to atomically commit local business changes and outgoing events. Use inbox/deduplication to safely consume duplicates. Outbox relays can publish more than once.
- **Compensation failure:** Keep the Saga in a recoverable state, retry with bounded backoff, query external provider status where possible, and escalate to manual intervention when required.
- **State transitions:** Validate incoming results against current Saga state, correlation ID, and operation/attempt ID. Delayed events must not overwrite newer valid outcomes.
- **2PC comparison:** Two-Phase Commit coordinates atomic commit among participating transaction managers using prepare and commit phases. Saga instead commits local steps independently and manages business compensation. Each service still needs local ACID transactions.

## Practical Example
Order workflow:
1. Create order.
2. Reserve inventory.
3. Capture payment.
4. Create shipment.

If shipment creation permanently fails, compensate in reverse dependency order: refund payment, release inventory, and cancel the order. Track each compensation independently; do not mark the Saga compensated until the required outcomes are confirmed.

## Production Perspective
A Saga is a durable business workflow, not merely a chain of messages. Persist state, use stable command and event IDs, enforce idempotency, correlate all messages, and reconcile ambiguous external outcomes. Model intermediate states such as `PAYMENT_UNKNOWN` and `REFUND_PENDING`. Some effects cannot be perfectly reversed; provide explicit manual recovery paths and observability for stuck workflows.

## Common Mistakes
- Treating compensation as database rollback.
- Assuming every compensation succeeds or restores the exact original state.
- Retrying an ambiguous operation with a new idempotency key.
- Keeping Saga state only in process memory.
- Publishing events without an outbox or equivalent reliability strategy.
- Assuming orchestration requires synchronous HTTP.
- Treating a timeout as proof that the operation failed.
- Marking a Saga complete before all required forward or compensating steps are confirmed.
- Using Saga when one local database transaction is sufficient.

## Key Takeaways
- Saga = sequence of local transactions plus compensating actions.
- Choreography distributes workflow decisions; orchestration centralizes them.
- Compensation is a new business operation and may be imperfect or fail.
- Durable state, idempotency, outbox/inbox, and reconciliation make recovery possible.
- Saga manages intermediate consistency; it does not eliminate distributed failure.
- Local ACID transactions remain essential for each service's invariants.

## Reflection Questions
1. Why can't a normal database transaction roll back changes made by independent microservices?
2. Explain forward and compensating transactions.
3. Why is a refund a compensation rather than a rollback?
4. Compare choreography and orchestration.
5. What if the orchestrator crashes after a service commits but before receiving its result event?
6. Why do Saga commands need idempotency?
7. How does the transactional outbox help a Saga?
8. What should happen if a compensation itself fails?
9. Compare Saga with Two-Phase Commit.
10. When would you avoid using Saga?

## Related Lessons
- Lesson 132 — Transactions
- Lesson 138 — Why Messaging?
- Lesson 141 — Event-Driven Architecture
- Lesson 142 — Dead Letter Queues

## What's Next
Lesson 144 — Logging (Module 11: Observability).
