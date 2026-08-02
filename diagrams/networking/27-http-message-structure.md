# HTTP Request and Response Structure

## HTTP Request

```text
┌──────────────────────────────────────────────┐
│              HTTP REQUEST                    │
│                                              │
│ POST /orders HTTP/1.1                        │
│ Host: shop.example.com                       │
│ Content-Type: application/json               │
│ Authorization: Bearer abc123                 │
│ Cookie: session_id=xyz                       │
│                                              │
│ {                                            │
│   "product_id": 123                          │
│ }                                            │
└──────────────────────────────────────────────┘
```

Structure:

```text
HTTP Request
      │
      ├── Request Line
      │     ├── Method
      │     ├── Path
      │     └── HTTP Version
      │
      ├── Headers
      │     ├── Host
      │     ├── Content-Type
      │     ├── Accept
      │     ├── Authorization
      │     └── Cookie
      │
      └── Body (optional)
```

## HTTP Response

```text
┌──────────────────────────────────────────────┐
│              HTTP RESPONSE                   │
│                                              │
│ HTTP/1.1 201 Created                         │
│ Content-Type: application/json               │
│ Cache-Control: no-cache                      │
│                                              │
│ {                                            │
│   "order_id": 9876                           │
│ }                                            │
└──────────────────────────────────────────────┘
```

Structure:

```text
HTTP Response
      │
      ├── Status Line
      │     ├── HTTP Version
      │     ├── Status Code
      │     └── Reason Phrase
      │
      ├── Headers
      │
      └── Body (optional)
```

## Content-Type vs Accept

```text
Client
   │
   │ Accept: application/json
   │
   │ "I prefer JSON in the response."
   ▼
Server
   │
   │ Content-Type: application/json
   │
   │ "The response body is JSON."
   ▼
Client
```

`Accept` expresses a preference.

`Content-Type` describes the actual body representation being sent.

If the server cannot provide an acceptable representation, it may respond with:

```text
406 Not Acceptable
```
