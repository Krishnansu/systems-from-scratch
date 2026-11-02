# Lesson 139 — RabbitMQ Commands and Lab

## Start a disposable local broker

```bash
docker run -d --name sfs-rabbitmq \
  -p 5672:5672 -p 15672:15672 \
  rabbitmq:4-management
```

- AMQP port: `5672`
- Management UI: `http://localhost:15672`
- Typical default local development credentials: `guest` / `guest`. The guest account is restricted to local connections by default.

## Explore

1. Open the management UI.
2. Create a topic exchange named `events`.
3. Create queues named `email`, `analytics`, and `inventory`.
4. Bind `email` with `order.created`, `analytics` with `order.#`, and `inventory` with `inventory.*`.
5. Publish test messages using routing keys `order.created`, `order.payment.failed`, and `inventory.reserved`.
6. Observe which queues receive each message.

Expected routing:
- `order.created` → `email`, `analytics`
- `order.payment.failed` → `analytics`
- `inventory.reserved` → `inventory`

## Cleanup

```bash
docker rm -f sfs-rabbitmq
```

This disposable container is not a persistent production setup. Removing it deletes its container-local state. Do not use production credentials or expose the management UI to untrusted networks.
