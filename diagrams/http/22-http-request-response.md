# HTTP Request and Response

```text
Client                                      Server

   │                                           │
   │  GET /users HTTP/1.1                      │
   │  Host: api.example.com                    │
   │  Accept: application/json                 │
   │                                           │
   │──────────────────────────────────────────►│
   │                                           │
   │                  Process Request          │
   │                                           │
   │  HTTP/1.1 200 OK                          │
   │  Content-Type: application/json           │
   │                                           │
   │  {                                        │
   │    "users": [...]                        │
   │  }                                        │
   │                                           │
   │◄──────────────────────────────────────────│
   │                                           │
```

### HTTP Request

```text
Request Line
     │
     ├── Method: GET
     ├── Path: /users
     └── Version: HTTP/1.1

Headers
     │
     ├── Host
     ├── Accept
     └── Authorization

Optional Body
```

### HTTP Response

```text
Status Line
     │
     ├── Version: HTTP/1.1
     ├── Status: 200
     └── Reason: OK

Headers
     │
     └── Content-Type

Optional Body
```

**Key Points**
- HTTP follows a request-response model.
- The request describes what the client wants.
- The response describes the result of processing that request.
- Headers carry metadata.
- Bodies carry optional application data.