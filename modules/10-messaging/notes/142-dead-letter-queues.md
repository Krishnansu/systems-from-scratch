# Lesson 142 — Dead Letter Queues

## Objectives
- Explain poison messages and dead-letter queues.
- Design bounded retry policies with backoff and jitter.
- Understand RabbitMQ DLX/DLQ routing and Kafka retry topics/DLTs.
- Understand ordering, duplicate delivery, and safe reprocessing.
- Identify production monitoring and recovery requirements.

## Prerequisites
- Lesson 138 — Why Messaging?
- Lesson 139 — RabbitMQ
- Lesson 140 — Kafka
- Lesson 141 — Event-Driven Architecture

## Concept Summary
A Dead Letter Queue (DLQ) isolates messages that cannot be processed successfully under a defined failure policy. It prevents poison messages from repeatedly consuming resources and provides a place for investigation and controlled recovery. Kafka commonly implements the equivalent pattern with retry topics and Dead Letter Topics (DLTs).

## Core Ideas
- **Poison message:** A message that repeatedly fails because of invalid data, incompatible schema, or a persistent processing defect.
- **Failure classification:** Transient failures (timeouts, temporary outages) may be retried. Permanent data errors should generally be isolated. Valid business rejections should produce business outcome events rather than be treated as technical failures.
- **Immediate retry:** Can create tight loops and retry storms.
- **Exponential backoff:** Increases delay between attempts, commonly doubling up to a maximum.
- **Jitter:** Randomizes retry delays to prevent synchronized retry bursts.
- **Retry limit:** Bound attempts; after exhaustion, route to a DLQ/DLT or another explicit recovery path.
- **RabbitMQ DLX:** An exchange to which a queue dead-letters messages. Configure the DLX, bindings, and destination DLQ. Common dead-letter conditions include rejection with `requeue=false`, expiration, queue length limits, and quorum queue delivery limits.
- **RabbitMQ retry queue:** A queue with TTL and a DLX can delay a message before routing it back to the main exchange. Multiple queues can provide different delay levels. Requeueing or delayed retries can change processing order.
- **RabbitMQ reliability:** Dead-letter transfer guarantees depend on queue type and configuration. Quorum queues support an at-least-once dead-lettering mode with additional configuration and resource costs. A DLX alone is not a universal no-loss guarantee.
- **Kafka DLT:** Kafka has no equivalent automatic DLX behavior. Applications or frameworks publish failed records to retry topics or a DLT.
- **Kafka retry flow:** Publish the failed record to a retry topic, then advance the original offset only with a safe publication/commit strategy. Kafka transactions can coordinate Kafka-to-Kafka operations within their transaction boundary, not arbitrary databases or external APIs.
- **Ordering:** Retry topics and delayed RabbitMQ queues can allow later messages to complete first. Preserve per-entity ordering explicitly if the business requires it.
- **Failure metadata:** Preserve original topic/partition/offset or queue, event ID, key, payload, attempt count, failure reason, timestamp, correlation/trace context, and relevant headers. Protect sensitive data.
- **Safe replay:** Diagnose and fix the cause before replaying. Use durable idempotency/deduplication and reconcile ambiguous external side effects, especially payments.
- **Operations:** Monitor DLQ depth, oldest-message age, dead-letter rate, retry count, failure categories, consumer lag, and retry success. Assign ownership, retention, alerting, and controlled replay procedures.

## Practical Example
A payment consumer receives `OrderCreated`. A temporary provider 503 may be retried with backoff and jitter. An invalid currency field should be isolated for investigation. A card decline is a valid business outcome and should publish a payment-failure event. A timeout with an ambiguous payment result requires provider idempotency and reconciliation before retrying.

## Production Perspective
A DLQ is a quarantine and recovery mechanism, not an automatic repair system. Define retryable versus permanent errors, cap attempts, avoid retry storms, preserve diagnostic metadata, and provide controlled replay tooling. Ensure replay cannot duplicate business effects. Protect DLQ payloads with appropriate access control, encryption, and retention policies.

## Common Mistakes
- Retrying every failure indiscriminately.
- Requeueing poison messages immediately forever.
- Assuming a DLQ automatically retries or repairs messages.
- Assuming RabbitMQ DLX transfer is loss-proof in every configuration.
- Assuming Kafka has native RabbitMQ-style dead-letter routing.
- Ignoring ordering changes introduced by delayed retries.
- Replaying payment or other side-effecting messages without idempotency and reconciliation.
- Treating a valid business rejection as a technical processing failure.
- Creating a DLQ without monitoring, ownership, and a recovery process.

## Key Takeaways
- Classify failures before choosing retry or dead-letter behavior.
- Use bounded retries with backoff and jitter.
- RabbitMQ uses DLX routing; Kafka commonly uses retry topics and DLTs.
- Retry mechanisms can affect ordering and create duplicates.
- Idempotency and controlled replay are essential for safe recovery.
- A DLQ is useful only when failures are monitored, investigated, and resolved.

## Reflection Questions
1. What is a poison message, and why is immediate requeue dangerous?
2. Explain exponential backoff and jitter.
3. Compare RabbitMQ `requeue=true`, `requeue=false`, and DLX routing.
4. How does a TTL-based RabbitMQ retry queue work?
5. How do Kafka retry topics and DLTs work?
6. What can happen if a Kafka consumer publishes to a retry topic and crashes before committing the original offset?
7. Why can retry topics break per-key processing order?
8. How would you safely retry and replay a payment whose provider request timed out ambiguously?

## Related Lessons
- Lesson 138 — Why Messaging?
- Lesson 139 — RabbitMQ
- Lesson 140 — Kafka
- Lesson 141 — Event-Driven Architecture

## What's Next
Lesson 143 — Saga Pattern.
