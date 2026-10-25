# Lesson 122 — Internal DNS

## Objectives

- Explain how internal DNS maps service names to DNS answers.
- Understand Kubernetes Service DNS names and search domains.
- Distinguish ClusterIP and headless Service answers.
- Explain CoreDNS's role and DNS caching trade-offs.
- Troubleshoot DNS failures separately from connection failures.

## Prerequisites

- Lesson 109 — Kubernetes Services
- Lesson 120 — End-to-End Kubernetes Troubleshooting Lab
- Lesson 121 — Service Discovery

## Theory

### Internal DNS

Internal DNS provides name resolution within an environment. It lets callers use stable logical names instead of hardcoding replaceable instance IP addresses. DNS resolves names; it does not carry application requests.

### Kubernetes Service DNS

A conventional Service name is `<service>.<namespace>.svc.<cluster-domain>`. For example, `inventory.store.svc.cluster.local`. `cluster.local` is conventional, not universal. Pods commonly use resolver search domains, allowing a same-namespace Service to be reached by its short name, such as `inventory`.

### Resolution and traffic are separate

For a normal ClusterIP Service, DNS typically returns the Service virtual IP. Kubernetes networking forwards traffic to an eligible backend endpoint. A headless Service (`clusterIP: None`) can return endpoint addresses directly, so clients may have more responsibility for endpoint selection and stale-address handling.

### CoreDNS and resolver configuration

CoreDNS commonly serves cluster DNS queries in Kubernetes. Pod resolver configuration may specify a nameserver, search suffixes, and `ndots`. Resolver behavior can expand short names into multiple candidate names; exact behavior depends on resolver implementation and configuration. CoreDNS answers queries but does not sit in the path of every application request.

### Records and transport

- `A`: IPv4 address.
- `AAAA`: IPv6 address.
- `CNAME`: alias to another DNS name.
- `SRV`: service-related information, including port and target.

DNS commonly uses UDP port 53 and can use TCP port 53 when required. Network restrictions or DNS-server failures can prevent resolution even when an application is healthy.

### Caching and freshness

DNS servers, local resolvers, language runtimes, and clients may cache answers. A changed endpoint or record may not immediately replace every cached result. Persistent connections may continue independently of DNS refreshes. TTL is a caching hint/limit for record reuse, not a guarantee of endpoint health.

## Real World Example

A checkout Pod queries `inventory.store.svc.cluster.local`. CoreDNS returns the Service virtual IP for a normal ClusterIP Service. The client then connects to that IP and port; the cluster networking data plane forwards traffic to an eligible inventory endpoint. With a headless Service, DNS can instead return endpoint addresses.

## Deep Dive

```text
Application
    → resolver / cache
    → internal DNS (commonly CoreDNS)
    → DNS answer
    → application connection
    → cluster networking
    → backend
```

These are separate stages. Successful resolution does not prove that a connection succeeds or that the application responds correctly.

## Hands-on Exercise

On a cluster you are authorized to inspect, use the read-only commands in [the Lesson 122 command reference](../commands/122-internal-dns.md). Compare short-name and fully qualified lookups from an existing client Pod, inspect `/etc/resolv.conf`, and compare DNS answers with the Service and EndpointSlices. Do not create debug workloads or modify shared resources without authorization.

## Common Misconceptions

- DNS resolution is not application traffic forwarding.
- A ClusterIP Service normally resolves to its virtual IP, not directly to every Pod IP.
- A headless Service can publish endpoint addresses.
- DNS success does not prove backend reachability or application health.
- DNS changes do not instantly invalidate every cache or persistent connection.
- CoreDNS does not handle every application request.

## Summary

Internal DNS provides stable names for service communication. Kubernetes combines resolver configuration, CoreDNS, Service records, endpoint state, and cluster networking. Diagnose name resolution separately from connection establishment and application behavior.

## Key Takeaways

- Use logical names instead of hardcoded instance addresses.
- Understand Service names, namespaces, search domains, and the cluster domain.
- Distinguish ClusterIP and headless Service DNS answers.
- Account for caching and resolver behavior.
- If DNS succeeds but requests fail, investigate ports, endpoints, routing, policies, and application health.

## Reflection Questions

1. What is the difference between `inventory` and `inventory.store.svc.cluster.local`?
2. Why do ClusterIP and headless Services have different DNS behavior?
3. What roles do CoreDNS, cluster networking, and the application play?
4. How can caching cause problems after an endpoint changes?
5. DNS resolves but a connection times out. What should you investigate next?

## What's Next

Lesson 123 — API Gateway.
