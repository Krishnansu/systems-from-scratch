# Lesson 48 — HTTP/3 Push & Prioritization

## Objectives

- Understand HTTP/3 Server Push and `PUSH_PROMISE`.
- Understand why Server Push became uncommon in modern browser deployments.
- Understand preload as a client-controlled resource-loading hint.
- Understand HTTP/3 prioritization and `PRIORITY_UPDATE`.
- Distinguish Server Push, prioritization, and QUIC flow control.

## Concept Summary

HTTP/3 inherited Server Push from HTTP/2. A server can proactively promise and send a resource before the client explicitly requests it. Although useful in theory, Server Push is difficult to use efficiently because the server may not know whether the client already has the resource cached. Modern browser deployments therefore generally rely more on client-driven discovery, preload hints, and browser scheduling.

HTTP/3 also supports priority signaling. Priority communicates scheduling intent, but does not guarantee delivery order because the server, QUIC flow control, congestion control, CPU, and network conditions all constrain transmission.

## Core Ideas

### Server Push

`PUSH_PROMISE` allows a server to announce a resource it intends to push proactively.

```text
Client                         Server

GET /index.html
----------------------------->

PUSH_PROMISE /style.css
<-----------------------------

HTML
<-----------------------------

CSS
<-----------------------------
```

### Why Server Push Is Difficult

The server may not know the client's cache state.

```text
Client cache

style.css  ✓
app.js     ✓
logo.png   ✓

Server pushes them again
        |
        v
Wasted bandwidth / resources
```

Push can also compete with genuinely important requested data for available network capacity.

### Preload

`<link rel="preload">` is a web-platform resource-loading hint, not an HTTP/3-specific feature. It can be used over HTTP/1.1, HTTP/2, or HTTP/3.

```text
HTML
  |
  +---- preload hint
  |
  v
Browser decides to fetch early
  |
  v
HTTP request
```

The browser has better knowledge of cache state, existing requests, page state, and resource importance, making this approach more informed than unconditional server push.

### Prioritization

Prioritization answers:

> Among available work, what should receive attention first?

HTTP/3 uses `PRIORITY_UPDATE` to communicate priority information. The important mental model is urgency rather than a guarantee of transmission order.

```text
HTML       → high urgency
CSS        → high urgency
Hero image → medium urgency
Analytics  → low urgency
```

## Push vs Priority vs Flow Control

```text
Server Push
    |
    v
What should I send proactively?

Priority
    |
    v
What should receive attention first?

Flow Control
    |
    v
How much am I currently allowed to send?
```

These operate at different levels of the system.

## Production Perspective

Modern browser deployments generally do not depend on Server Push as the primary way to accelerate page loading. Client-side resource discovery, preload hints, browser scheduling, and priority signaling provide better awareness of the receiver's state.

Server Push remains important to understand because it demonstrates a general distributed-systems lesson: a sender cannot always make optimal decisions when it lacks information about receiver state.

## Common Mistakes

- Thinking Server Push is mandatory in HTTP/3.
- Thinking preload is a QUIC or HTTP/3 transport feature.
- Assuming priority guarantees delivery order.
- Confusing priority with flow control.
- Assuming the server knows exactly what the browser already has cached.

## Key Takeaways

1. HTTP/3 inherited Server Push and `PUSH_PROMISE` from HTTP/2.
2. Server Push lets a server proactively send a resource.
3. Server Push became uncommon in modern browser deployments because cache state and resource scheduling make unconditional pushing difficult to use efficiently.
4. Preload is a client-side resource-loading hint and is independent of HTTP/3.
5. `PRIORITY_UPDATE` communicates scheduling intent.
6. Priority is not a delivery guarantee.
7. QUIC flow control and congestion control still constrain what can actually be transmitted.

## Reflection Questions

- Why can a server's knowledge of the page still be insufficient to use Server Push efficiently?
- Why does preload give the browser more control than Server Push?
- Why can a low-priority resource still consume network capacity?

## Related Lessons

- Lesson 43 — HTTP/3 Fundamentals
- Lesson 45 — QPACK: HTTP/3 Header Compression
- Lesson 47 — HTTP/3 Error Handling & Connection Shutdown
- Lesson 49 — HTTP/3 ↔ QUIC Integration
