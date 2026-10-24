# Lesson 119 — Kubernetes Security Commands

Read-only inspection for RBAC, workload identities, and NetworkPolicy.

## Context and identity

```bash
kubectl config current-context
kubectl config view --minify
kubectl get serviceaccounts -n <namespace>
kubectl describe serviceaccount <name> -n <namespace>
```

Check which ServiceAccount a Pod specifies by inspecting its Pod specification. Avoid sharing output containing credentials or sensitive configuration.

## RBAC

```bash
kubectl get roles,rolebindings -n <namespace>
kubectl get clusterroles
kubectl get clusterrolebindings
kubectl describe role <name> -n <namespace>
kubectl describe rolebinding <name> -n <namespace>
kubectl auth can-i get pods -n <namespace>
kubectl auth can-i create deployments -n <namespace>
```

`kubectl auth can-i` checks the current command identity unless another identity is explicitly tested. Inspect both the rules and bindings when diagnosing `Forbidden` errors.

## NetworkPolicy

```bash
kubectl get networkpolicies -A
kubectl describe networkpolicy <name> -n <namespace>
kubectl get pods -n <namespace> --show-labels
kubectl get services,endpointslices -n <namespace>
```

Compare selected Pod labels, source selectors, namespaces, ports, DNS, and application listeners. Confirm that the cluster network plugin enforces NetworkPolicy.

## Safety

- Confirm context and namespace before inspection.
- Do not grant broad permissions just to make an error disappear.
- Do not apply or remove policies on shared clusters without authorization and a rollback plan.
- Treat credentials and sensitive configuration as confidential.
