# Lesson 123 — API Gateway Command Reference

Use these read-only commands only in a Kubernetes context you are authorized to inspect. Resource types and permissions vary by cluster.

## Confirm Context

```bash
kubectl config current-context
kubectl get namespaces
```

## Inspect Existing Ingress Resources

```bash
kubectl get ingress -A
kubectl get ingress <name> -n <namespace> -o yaml
kubectl describe ingress <name> -n <namespace>
```

An Ingress resource describes routing rules; an Ingress controller must implement them. Check the configured class and controller-specific documentation before interpreting behavior.

## Inspect Gateway API Resources (if installed)

```bash
kubectl get gatewayclasses
kubectl get gateways -A
kubectl get httproutes -A
kubectl describe gateway <name> -n <namespace>
```

These resource types may be unavailable if Gateway API CRDs are not installed or your identity lacks permission. Missing resources do not prove that no gateway exists; the environment may use another implementation.

## Inspect Candidate Upstream Services

```bash
kubectl get services -n <namespace>
kubectl get endpointslices -n <namespace>
kubectl get pods -n <namespace> -o wide
```

Compare route destinations with Service names, ports, and endpoint state. This is inspection only; it does not establish that a request can successfully reach the backend.

## Optional HTTP Inspection

If you already have an authorized gateway URL and a safe endpoint, a request can be inspected with:

```bash
curl -i --max-time 5 https://<gateway-host>/<safe-path>
```

This sends a real request. Use only a known safe endpoint; avoid state-changing routes and do not include credentials in shell history. A response status alone does not identify the complete failure cause.

## Troubleshooting Sequence

1. Confirm the target environment and gateway hostname.
2. Inspect the configured route and destination.
3. Check gateway logs and metrics using approved access; treat output as potentially sensitive.
4. Verify the upstream Service, ports, and EndpointSlices.
5. Separate gateway policy rejection, upstream connection errors, timeouts, and application errors.
6. For state-changing requests with ambiguous outcomes, verify operation state before retrying.

## Safety

- Commands are intended for inspection; the optional curl command sends a request.
- Do not apply, delete, expose, or modify cluster resources for this exercise.
- Do not send credentials or sensitive payloads to unverified endpoints.
- Do not create debug workloads in shared or production clusters without authorization.

## Related Lessons

- [121 — Service Discovery](../notes/121-service-discovery.md)
- [122 — Internal DNS](../notes/122-internal-dns.md)
- [123 — API Gateway](../notes/123-api-gateway.md)
