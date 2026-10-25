# Lesson 128 — mTLS Command Reference

Use only clusters and namespaces you are authorized to inspect. These commands are intended for read-only diagnosis.

## Confirm Context

```bash
kubectl config current-context
kubectl get namespaces
```

## Inspect Peer Authentication

```bash
kubectl get peerauthentications -A
kubectl get peerauthentication <name> -n <namespace> -o yaml
```

Review policy scope and mode. Do not assume one resource is the only applicable policy.

## Inspect Destination TLS Policy

```bash
kubectl get destinationrules -n <namespace>
kubectl get destinationrule <name> -n <namespace> -o yaml
```

Review the applicable destination and TLS settings. Effective behavior depends on configuration and policy scope.

## Inspect Workloads and Service Endpoints

```bash
kubectl get pods,services,endpointslices -n <namespace>
```

Check workload readiness and whether the expected destination endpoints exist.

## Optional Istio Diagnostics

```bash
istioctl proxy-status
istioctl analyze -n <namespace>
istioctl proxy-config secret <pod-name> -n <namespace>
```

Command availability and permissions depend on the environment. Proxy configuration and certificate output can contain sensitive information; do not share credential material. A successful diagnostic does not prove end-to-end health.

## Evidence-Based Troubleshooting

1. Scope affected callers, destinations, namespaces, and paths.
2. Identify the policy change and its scope.
3. Determine whether the caller uses mTLS, plaintext, or another TLS configuration.
4. Inspect receiving-side PeerAuthentication and relevant destination TLS settings.
5. Review authorized proxy logs, handshake errors, certificate validity and identity, trust, and active configuration.
6. Check authorization separately if the TLS connection succeeds but access is denied.
7. Follow incident procedures before making changes.

## Safety Notes

- Do not apply or weaken security policies as an exploratory step in a shared cluster.
- Do not restart workloads without evidence and authorization.
- Never expose private keys or sensitive credential material.

## Related Lessons

- [125 — Envoy](../notes/125-envoy.md)
- [126 — Service Mesh](../notes/126-service-mesh.md)
- [127 — Istio](../notes/127-istio.md)
- [128 — mTLS](../notes/128-mtls.md)
