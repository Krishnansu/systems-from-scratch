# Lesson 121 — Service Discovery Command Reference

Use these read-only commands only against a Kubernetes cluster you are authorized to inspect. Replace example names and namespaces with actual values.

## Confirm Context and Discover Services

```bash
kubectl config current-context
kubectl get services -A
kubectl get services -n <namespace>
kubectl get service <service-name> -n <namespace> -o yaml
kubectl describe service <service-name> -n <namespace>
```

Confirm the cluster context, namespace, Service name, type, selector, and ports before interpreting results.

## Inspect Backend Endpoints

```bash
kubectl get endpointslices -n <namespace>
kubectl get endpointslices -n <namespace> -o wide
kubectl get pods -n <namespace> -o wide --show-labels
```

Identify the EndpointSlice associated with the Service. Compare endpoint addresses and conditions with the selected Pods. A missing or ineligible endpoint can indicate a selector mismatch, absent Pods, readiness issues, or other endpoint conditions.

## DNS Checks From an Existing Client Environment

From a client Pod or environment that already has appropriate DNS tools:

```bash
nslookup <service-name>
nslookup <service-name>.<namespace>
nslookup <service-name>.<namespace>.svc.cluster.local
```

The fully qualified name assumes the conventional `cluster.local` DNS domain; a cluster can use a different domain. Tool availability and DNS search paths vary by image and environment. Do not create a debug Pod in a shared cluster without authorization.

For a normal ClusterIP Service, DNS typically resolves to the Service IP. A headless Service can resolve to endpoint addresses. Confirm the Service type before interpreting the answer.

## Troubleshooting Sequence

1. Confirm current context and expected namespace.
2. Verify the Service exists and its name is correct.
3. Test name resolution from the relevant client environment.
4. Inspect Service selectors, Pod labels, and EndpointSlices.
5. Confirm Service `port`, `targetPort`, and the application's listening port.
6. If DNS and endpoints look correct but connections fail, inspect routing, NetworkPolicies, firewall rules, and application health.
7. Check events and logs as appropriate, treating output as potentially sensitive.

## Safety

- These examples are read-only.
- Do not apply, delete, scale, expose, or modify workloads as part of this exercise.
- Avoid creating debug workloads in shared or production clusters without authorization.
- DNS resolution does not prove backend reachability or successful application requests.

## Related Lessons

- [109 — Kubernetes Services](../../07-kubernetes/notes/109-services.md)
- [120 — End-to-End Kubernetes Troubleshooting Lab](../../07-kubernetes/notes/120-end-to-end-kubernetes-troubleshooting-lab.md)
- [121 — Service Discovery](../notes/121-service-discovery.md)
