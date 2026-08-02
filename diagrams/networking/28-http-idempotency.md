# HTTP Safe Methods and Idempotency

## PUT Is Generally Idempotent

```text
PUT /users/123
{
  "name": "Krishnansu"
}
```

First request:

```text
Resource 123
     │
     ▼
Name = Krishnansu
```

Repeat the same request:

```text
Resource 123
     │
     ▼
Name = Krishnansu
```

Repeat again:

```text
Resource 123
     │
     ▼
Name = Krishnansu
```

The intended final state is the same.

```text
PUT
 │
 ├── Request 1 → State X
 ├── Request 2 → State X
 └── Request 3 → State X
```

Therefore PUT is generally idempotent.

---

## POST Is Generally Not Idempotent

```text
POST /orders
{
  "product_id": 123
}
```

First request:

```text
POST
 │
 ▼
Order #1001 Created
```

Retry:

```text
POST
 │
 ▼
Order #1002 Created
```

The final state is different from executing the operation once.

```text
POST
 │
 ├── Request 1 → Create Order #1001
 └── Request 2 → Create Order #1002
```

Therefore POST is generally not idempotent.

---

## Safe vs Idempotent

```text
Safe
 │
 └── Does not request a state-changing operation

Idempotent
 │
 └── Repeating has the same intended effect on resource state
```

Typical properties:

| Method | Safe | Idempotent |
|--------|------|------------|
| GET | Yes | Yes |
| POST | No | Generally No |
| PUT | No | Yes |
| PATCH | No | Not necessarily |
| DELETE | No | Yes |
```

## Important Example: Payment Retry

A client sends:

```text
Client
   │
   │ POST /payment
   ▼
Server
   │
   │ Payment processed
   ▼
Network Failure
```

The client does not know whether the server processed the payment.

If it retries:

```text
Client
   │
   │ POST /payment
   ▼
Server
   │
   │ Payment processed again
```

The customer could potentially be charged twice.

This is why payment APIs commonly use idempotency keys or other mechanisms to make retries safe.
