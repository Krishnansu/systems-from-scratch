# Diagram 112 — HTTP/3 Server Push vs Preload

```text
SERVER PUSH

Client                         Server

GET /index.html
----------------------------->

PUSH_PROMISE /style.css
<-----------------------------

HTML
<-----------------------------

CSS
<-----------------------------

Server decides to send proactively


PRELOAD

Server                         Browser

HTML with preload hint
----------------------------->

<link rel="preload" ...>

Browser checks its own state
         |
         +---- cache
         +---- existing requests
         +---- resource importance
         +---- page state
         |
         v
Browser decides whether to fetch early
```

Key distinction:

```text
Server Push → server proactively sends
Preload     → server hints, browser decides
```
