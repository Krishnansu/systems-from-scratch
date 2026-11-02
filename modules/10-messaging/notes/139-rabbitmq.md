# Lesson 139 — RabbitMQ

## Objectives
- Explain exchanges, queues, bindings, and routing keys.
- Compare direct, fanout, topic, and headers exchanges.
- Distinguish publisher confirms from consumer acknowledgments.
- Understand durability, redelivery, prefetch, and competing consumers.
- Compare RabbitMQ's work-queue model with Kafka's log model.

## Prerequisites
- Lesson 138 — Why Messaging?

## Concept Summary
RabbitMQ is a message broker that routes published messages through exchanges into queues. Consumers process queued messages independently. Reliable operation requires deliberate publishing, persistence, acknowledgment, retry, idempotency, and capacity decisions.

## Core Ideas
- **Flow:** producer → exchange → binding/routing rule → queue → consumer.
- **Direct exchange:** routing key exactly matches the binding key.
- **Fanout exchange:** routes to every bound queue; routing keys are ignored.
- **Topic exchange:** dot-separated routing patterns; `*` matches one word and `#` matches zero or more words.
- **Headers exchange:** routes using message headers and binding arguments.
- **Default exchange:** unnamed direct exchange; a queue name can be used as its routing key.
- **Separate subscribers:** independent subscribers normally need separate queues; workers sharing one queue compete for its messages.
- **Publisher confirms:** broker confirms responsibility for a publish; this does not mean a consumer processed it.
- **Consumer acknowledgments:** consumers acknowledge completed work. A crash after a database commit but before `ack` can cause redelivery.
- **Durability:** durable queue definitions, persistent messages, publisher confirms, replication, and storage configuration address different failure concerns.
- **Manual acknowledgments:** allow acknowledgment after processing but do not eliminate duplicates.
- **Negative acknowledgment/rejection:** messages may be requeued or dead-lettered according to flags and queue configuration. Avoid unbounded rapid retry loops.
- **Prefetch:** limits outstanding unacknowledged deliveries; tune for processing latency, fairness, and throughput.
- **Idempotency:** use durable deduplication and commit it atomically with database effects where possible. External side effects need their own idempotency or reconciliation strategy.

## Practical Example
A topic exchange `events` has queues bound with `order.created`, `order.#`, and `inventory.*`. An `order.created` event routes to the first two queues; `order.payment.failed` routes to `order.#`; and `inventory.reserved` routes to `inventory.*`.

## Production Perspective
Monitor queue depth, oldest-message age, publish and delivery rates, unacknowledged deliveries, consumer health, redeliveries, dead-letter rates, memory, disk alarms, and connection counts. Add consumers only when downstream dependencies and broker capacity can support the extra load.

## Commands
See `modules/10-messaging/commands/139-rabbitmq.md` for a disposable local Docker lab and cleanup steps.

## Common Mistakes
- Treating a publisher confirm as proof of completed processing.
- Assuming durable queues alone make every message durable.
- Assuming manual acknowledgment prevents duplicate processing.
- Binding independent subscribers to one shared queue when each needs its own copy.
- Increasing prefetch or consumer count without checking bottlenecks.

## Key Takeaways
- Exchanges route messages; queues retain work; consumers process deliveries.
- Routing type determines which queues receive a message.
- Publisher confirms and consumer acknowledgments cover different stages.
- Redelivery and at-least-once processing require duplicate-safe consumers.
- RabbitMQ emphasizes flexible routing and work distribution; Kafka emphasizes retained, partitioned logs and replay.

## Reflection Questions
1. Why does RabbitMQ use exchanges?
2. Which exchange routes related event keys using patterns?
3. How do publisher confirms differ from consumer acknowledgments?
4. How can a crash after a database commit lead to duplicate effects?
5. What trade-offs does prefetch introduce?
6. When might RabbitMQ be a better fit than Kafka?

## Related Lessons
- Lesson 132 — Transactions
- Lesson 137 — Redis
- Lesson 138 — Why Messaging?

## What's Next
Lesson 140 — Kafka.
