# Lesson 82 — gRPC Fundamentals

## Objectives

- Explain RPC and the purpose of gRPC.
- Understand Protobuf contracts, field numbers, and generated code.
- Trace a gRPC call over HTTP/2.
- Distinguish unary and streaming RPC patterns.
- Compare gRPC with REST and identify production concerns.

## Prerequisites

- HTTP request/response and HTTP/2 streams
- API contracts and service-to-service communication
- Timeouts, retries, and circuit breakers

## Theory

gRPC is a remote procedure call framework that lets services invoke defined operations on other services. It commonly uses Protocol Buffers (Protobuf) for service and message definitions and binary serialization, with HTTP/2 as its transport. Generated client and server code reduces manual contract and serialization work.

## Real World Example

An Order service calls `InventoryService.CheckStock` with a typed request. The generated client stub serializes the request and sends it through gRPC over HTTP/2. The Inventory service decodes it, executes the implementation, and returns a serialized response. The client receives the decoded result.

## Deep Dive

### Protobuf contracts

- `.proto` files define services, RPC methods, request messages, and response messages.
- Protobuf field numbers identify fields in the wire format; they are not source-code positions or default values.
- Renaming a field while preserving its number and wire type is normally wire-compatible, though generated source APIs and semantic meaning may change.
- Never reuse a removed field number for an unrelated field. Reserve removed field numbers and names when appropriate.
- Generated stubs provide typed client calls; they do not execute remote business logic locally.

### HTTP/2 request flow

1. Application invokes the generated stub.
2. Protobuf encodes the request; gRPC adds message framing.
3. HTTP/2 carries the RPC on a stream. Headers identify the method and metadata; DATA frames carry gRPC message bytes.
4. The server decodes the request and dispatches to the implementation.
5. The server sends response messages and final gRPC status; the client decodes the response.

One HTTP/2 connection can carry multiple independent streams. A stream can carry multiple gRPC messages, particularly for streaming RPCs. A gRPC message may span multiple HTTP/2 DATA frames. HTTP/2 multiplexing does not eliminate TCP-level head-of-line blocking.

### Four RPC patterns

- **Unary:** one request, one response.
- **Server streaming:** one request, multiple responses.
- **Client streaming:** multiple requests, one response.
- **Bidirectional streaming:** both sides exchange multiple messages on one RPC stream.

### gRPC and REST

REST commonly models resources and representations, often using JSON. gRPC models named service methods and typed messages, commonly using Protobuf. gRPC is often useful for typed internal service communication and streaming; REST is often convenient for public APIs and browser clients. They are complementary choices, not universal replacements for one another.

### Production perspective

- Set deadlines and propagate cancellation where possible.
- Retry only suitable operations and failures, with bounded attempts, backoff, jitter, and idempotency when needed.
- A deadline expiring does not prove that a remote side effect failed. Use idempotency keys and reconciliation for uncertain payment outcomes.
- Secure channels with TLS as appropriate and enforce authentication and authorization explicitly.
- Monitor RPC latency, status codes, deadline failures, cancellations, and dependency health.
- Bound concurrency and message sizes; streaming calls can hold resources for long periods.

## Hands-on Exercise

1. Explain what a generated client stub does and why it does not execute remote business logic locally.
2. Distinguish a field rename that preserves its number and wire type from unsafe reuse of a removed field number.
3. Explain the relationship between an HTTP/2 connection, streams, DATA frames, and gRPC messages.
4. Choose the server-streaming pattern for one subscription request followed by ongoing server updates.
5. Explain why a timed-out payment request may have succeeded and how an idempotency key prevents duplicate charges.

## Common Misconceptions

- gRPC replaces HTTP; it commonly uses HTTP/2.
- Protobuf and gRPC are the same thing; Protobuf defines messages and encoding, while gRPC provides the RPC framework.
- A remote call behaves like a local function call; network failures and deadlines still apply.
- HTTP/2 multiplexing removes every form of head-of-line blocking; TCP loss can still delay bytes on a connection.
- gRPC is always faster than REST; actual performance depends on workload and implementation.
- A timeout means the remote operation did not happen; the outcome can be unknown.

## Summary

gRPC combines explicit service contracts, generated code, Protobuf serialization, and HTTP/2 transport to support typed remote calls and four communication patterns. It improves consistency and supports efficient service communication, but production systems still need compatibility discipline, deadlines, safe retries, security, and observability.

## Key Takeaways

- RPC invokes operations across process boundaries; gRPC is one RPC framework.
- Protobuf field numbers are part of wire compatibility and should never be casually reused.
- HTTP/2 streams multiplex RPC traffic over a connection; gRPC messages are carried in DATA frames.
- Unary, server-streaming, client-streaming, and bidirectional-streaming patterns support different needs.
- Deadlines, cancellation, idempotency, authorization, and monitoring remain essential.

## Reflection Questions

1. Why is renaming a Protobuf field different from reusing its field number?
2. Why can multiple RPCs share an HTTP/2 connection without sharing a stream?
3. Why is a deadline exceeded result not proof that a payment failed?

## What's Next

Lesson 83 — Authentication Fundamentals (proposed continuation).
