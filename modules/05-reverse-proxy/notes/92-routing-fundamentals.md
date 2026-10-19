# Lesson 92 — Routing Fundamentals

## Objectives
- Explain host-based and path-based routing.
- Understand NGINX virtual server and location selection.
- Identify location matching precedence and the role of `^~`.
- Understand upstream selection and URI forwarding behavior.

## Prerequisites
- Lesson 88 — Reverse Proxy Fundamentals
- Lesson 89 — NGINX Fundamentals
- Lesson 90 — Load Balancing Fundamentals
- Lesson 91 — SSL/TLS Termination

## Theory
Routing selects a destination for an incoming request using attributes such as hostname and URI path. Host-based routing separates applications by hostname; path-based routing separates services under a hostname. Routing selects a service or upstream group, while load balancing selects an instance within that group.

## Real World Example
A reverse proxy can route `shop.example.com` to a store frontend, `blog.example.com` to a blog, and `shop.example.com/api/` to a product API. Host-based and path-based routing can be combined.

## Deep Dive
- NGINX first selects an applicable `server` block using the listening address, port, and hostname. SNI can help select the TLS certificate during the handshake; the HTTP Host header is available when the HTTP request is processed.
- NGINX then selects a matching `location`.
- `location = /health` is an exact match and takes precedence immediately.
- Ordinary prefix locations compete by longest prefix.
- `location ^~ /assets/` prevents regex locations from overriding that selected longest prefix.
- Otherwise, NGINX evaluates regex locations in configuration order; the first matching regex wins. If none matches, it uses the longest prefix.
- A route can target a direct backend or a named `upstream` group. Load balancing then selects an instance from that group.
- `proxy_pass` URI behavior matters: with `location /api/`, `proxy_pass http://product_api;` generally preserves `/api/products`, while `proxy_pass http://product_api/;` replaces the matching `/api/` prefix, forwarding `/products`.
- A correct backend selection does not guarantee success. Incorrect URI rewriting, missing backend routes, authorization, or application behavior can still cause errors.
- Debug routing by checking the hostname, selected server, matching location, forwarded URI, upstream, and backend logs.

## Hands-on Exercise
Given an NGINX configuration with exact, prefix, `^~`, and regex locations:
1. Predict the selected location for `/health`.
2. Predict the destination for `/api/products`.
3. Explain why `/assets/logo.png` matches an `/assets/` location using `^~` instead of a matching image regex.
4. Explain the URI difference between `proxy_pass http://product_api;` and `proxy_pass http://product_api/;` in `location /api/`.
5. Diagnose why a request might return 404 even when the expected backend is selected.

## Common Misconceptions
- NGINX does not simply choose the longest-looking rule across all location types; exact, prefix, and regex matching have distinct precedence.
- `^~` does not mean regex matching. It prevents regex evaluation after that longest prefix is selected.
- Host-based routing does not automatically guarantee tenant isolation.
- Routing and load balancing are related but separate decisions.
- Selecting the right backend does not guarantee the forwarded URI is correct or that the backend will return success.
- SNI is used during TLS setup, while HTTP Host is available when processing the HTTP request.

## Summary
A reverse proxy can expose multiple applications through one endpoint. NGINX selects a virtual server, matches a location according to defined precedence rules, and forwards the request to a backend or upstream group. URI rewriting and backend behavior must also be checked when debugging routing failures.

## Key Takeaways
- Host-based routing uses hostnames; path-based routing uses URI paths.
- NGINX location matching follows explicit precedence rules.
- `^~` prevents regex locations from overriding the selected longest prefix.
- Routing chooses the destination group; load balancing chooses an instance.
- Debug the selected server, location, forwarded URI, upstream, and backend response separately.

## Reflection Questions
1. Why might a company combine host-based and path-based routing?
2. What is the difference between `location /api/` and `location ^~ /api/`?
3. Why can correct backend selection still result in a 404?
4. How do SNI and HTTP Host differ in request processing?
5. What would you inspect if a request unexpectedly matches an image regex instead of an assets prefix?

## What's Next
Lesson 93 — Health Checks and Backend Availability: detecting unavailable instances, avoiding unhealthy backends, and handling recovery.
