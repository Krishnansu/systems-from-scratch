# Lesson 89 — NGINX Fundamentals

## Objectives
- Explain NGINX's roles as a web server, reverse proxy, and load balancer.
- Understand `listen`, `server_name`, `location`, `proxy_pass`, and `upstream`.
- Trace a request through NGINX to an application.
- Identify common proxy failures and configuration pitfalls.

## Prerequisites
- HTTP request/response fundamentals
- Lesson 88 — Reverse Proxy Fundamentals
- Basic Linux and networking knowledge

## Theory
NGINX is software commonly used to serve HTTP content, proxy requests to applications, and distribute traffic across backend instances.

```text
Client → NGINX (port 80/443) → Application (e.g. port 3000)
```

A minimal reverse-proxy configuration:

```nginx
server {
    listen 80;
    server_name localhost;

    location / {
        proxy_pass http://127.0.0.1:3000;
    }
}
```

- `listen`: network endpoint where NGINX accepts connections.
- `server_name`: hostname used to select a virtual server.
- `location`: matches request URIs and applies rules.
- `proxy_pass`: forwards matched requests to an upstream destination.
- `upstream`: names a group of backend servers for proxying or load balancing.

## Real World Example
An online store exposes one public domain. NGINX routes `/api/` to an API service on port 4000 and other paths to a frontend on port 3000. Clients use a stable endpoint without knowing backend addresses.

## Deep Dive
- NGINX can serve static files directly or proxy requests to applications.
- `server` selection and `location` matching are separate decisions.
- URI forwarding with `proxy_pass` depends on whether the directive includes a URI. A trailing slash can replace the matched location prefix.
- `proxy_set_header` can pass the original host, client IP information, and request scheme to the backend.
- Forwarded headers must be sanitized and trusted only from known proxy hops.
- An `upstream` group lets NGINX distribute requests across backend instances.
- `nginx -t` checks configuration syntax and basic validity; it does not prove upstream availability.
- `502 Bad Gateway` often indicates an invalid or unavailable upstream response; `504 Gateway Timeout` often indicates an upstream timeout. Logs and connectivity tests are needed to diagnose the cause.

## Hands-on Exercise
1. Route `/api/*` to port 4000 and other paths to port 3000.
2. Explain which directives control the listening endpoint and URI matching.
3. Compare `proxy_pass http://127.0.0.1:4000;` with `proxy_pass http://127.0.0.1:4000/;` inside `location /api/`.
4. Test a configuration using `nginx -t` and inspect a proxied request with `curl -v`, if NGINX is installed.
5. Diagnose possible causes of a 502 response.

## Common Misconceptions
- NGINX is not only a reverse proxy.
- `listen` does not select the backend for a request path.
- `server_name` and `location` match different parts of request handling.
- Forwarding headers do not automatically establish trustworthy client identity.
- A successful syntax check does not prove the application is reachable.

## Summary
NGINX is a web server and proxy whose configuration controls listening endpoints, virtual servers, URI matching, and upstream forwarding. It can proxy to a single application or distribute traffic across an upstream group. Correct operation requires valid configuration, reachable backends, careful header handling, and monitoring.

## Key Takeaways
- `listen`, `server_name`, `location`, and `proxy_pass` have distinct responsibilities.
- `upstream` groups backend instances.
- `proxy_pass` URI handling depends on its configuration.
- NGINX and the application are separate processes with separate failure modes.
- Configuration validation is necessary but not sufficient for end-to-end correctness.

## Reflection Questions
1. Why expose NGINX on port 80 while keeping an application on port 3000?
2. How does NGINX route requests to different ports?
3. What is the difference between `location` and `upstream`?
4. Why might a backend need `X-Forwarded-Proto`?
5. What would you investigate if configuration validation succeeds but clients receive 502 errors?

## What's Next
Lesson 90 — Load Balancing Fundamentals: distribution strategies, backend health, and instance failures.
