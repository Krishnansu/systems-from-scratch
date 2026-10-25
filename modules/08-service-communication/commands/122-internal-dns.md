# Lesson 122 — Internal DNS Command Reference

Use these read-only commands only against a Kubernetes cluster you are authorized to inspect. Replace example names and namespaces with actual values.

## Confirm Context and Service

```bash
kubectl config current-context
kubectl get pods -n <namespace>
kubectl get services -n <namespace>
kubectl get service <service-name> -n <namespace> -o yaml
kubectl get endpointslices -n <namespace>
```

Inspect the Service name, namespace, type, `clusterIP`, ports, selectors, and EndpointSlices. A normal ClusterIP Service and a headless Service can have different DNS answers.

## Test DNS from an Existing Client Pod

```bash
kubectl exec -n <namespace> <client-pod> -- nslookup <service-name>
kubectl exec -n <namespace> <client-pod> -- nslookup <service-name>.<namespace>
kubectl exec -n <namespace> <client-pod> -- nslookup <service-name>.<namespace>.svc.cluster.local
```

The full name assumes the conventional `cluster.local` domain. Confirm the actual cluster domain if necessary. `nslookup` must be installed in the client container. Do not create a debug Pod in a shared cluster without authorization.

## Inspect Resolver Configuration

```bash
kubectl exec -n <namespace> <client-pod> -- cat /etc/resolv.conf
```

Inspect the `nameserver`, `search`, and `options` entries. Search suffixes and `ndots` can influence which names are queried and in what order. Exact behavior depends on the resolver implementation.

## Inspect CoreDNS (if authorized)

```bash
kubectl get pods -n kube-system -l k8s-app=kube-dns
kubectl get service -n kube-system kube-dns
kubectl logs -n kube-system -l k8s-app=kube-dns --tail=100
```

Labels, Service names, permissions, and deployment details vary by cluster. Missing results from these example selectors do not by themselves prove CoreDNS is absent. Logs can contain sensitive information.

## Troubleshooting Sequence

1. Confirm context, Service name, and namespace.
2. Test short and namespace-qualified names from the relevant client environment.
3. Inspect `/etc/resolv.conf`, search suffixes, and the configured nameserver.
4. If lookups fail, investigate CoreDNS health, DNS traffic restrictions, and cluster-specific DNS configuration.
5. If lookups succeed, inspect Service type, ports, selectors, and EndpointSlices.
6. Continue with connectivity, NetworkPolicies, firewall/routing, and application health.

## Interpreting Symptoms

- `NXDOMAIN` or `no such host`: check the name, namespace, search path, and records.
- DNS timeout: check DNS server reachability, CoreDNS health, and traffic restrictions.
- Connection refused after successful lookup: check target port and listener.
- Connection timeout after successful lookup: check routing, policies, firewall rules, and destination responsiveness.
- Application errors after connection: inspect application behavior and dependencies.

These are diagnostic starting points, not definitive causes.

## Safety

- Commands are intended for inspection only.
- Do not apply, delete, scale, expose, or modify workloads for this exercise.
- Do not create debug workloads in shared or production clusters without authorization.
- Treat logs, events, and command output as potentially sensitive.
- DNS resolution does not prove backend reachability or application health.

## Related Lessons

- [109 — Kubernetes Services](../../07-kubernetes/notes/109-services.md)
- [120 — End-to-End Kubernetes Troubleshooting Lab](../../07-kubernetes/notes/120-end-to-end-kubernetes-troubleshooting-lab.md)
- [121 — Service Discovery](../notes/121-service-discovery.md)
- [122 — Internal DNS](../notes/122-internal-dns.md)
