# Service Communication Command References

This directory contains practical command references for Module 08. Use them as quick references; consult lesson notes for concepts and trade-offs.

## Lessons

- [121 — Service Discovery](121-service-discovery.md)
- [122 — Internal DNS](122-internal-dns.md)
- [123 — API Gateway](123-api-gateway.md)
- [124 — Sidecars](124-sidecars.md)
- [125 — Envoy](125-envoy.md)
- [126 — Service Mesh](126-service-mesh.md)
- [127 — Istio](127-istio.md)
- [128 — mTLS](128-mtls.md)

## General Safety Notes

- Confirm the current cluster context and namespace before inspecting Kubernetes resources.
- Prefer read-only commands and local configuration validation for introductory exercises.
- Do not create debug workloads or change shared resources without authorization.
- Treat command output, logs, configuration, and proxy admin data as potentially sensitive.
