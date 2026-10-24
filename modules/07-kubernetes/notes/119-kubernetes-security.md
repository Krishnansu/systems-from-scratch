# Lesson 119 — Kubernetes Security: RBAC, Workload Identity, and Network Policies

## Objectives

- Distinguish API authentication from authorization.
- Understand RBAC roles and bindings.
- Explain ServiceAccounts and workload identity.
- Understand how NetworkPolicy restricts Pod traffic.

## Core Concepts

- **RBAC** controls which API actions an identity can perform. A Role is namespaced; a ClusterRole can define cluster-scoped permissions or reusable rules. RoleBinding grants permissions within a namespace; ClusterRoleBinding grants ClusterRole permissions cluster-wide.
- A **ServiceAccount** provides an identity for a workload. It does not automatically grant broad API permissions; RBAC bindings determine authorization.
- **Workload identity** can let applications access external cloud resources through mapped identities instead of long-lived static credentials. The integration is provider-specific.
- **NetworkPolicy** selects Pods and defines allowed ingress and/or egress traffic. Enforcement depends on support from the cluster's network plugin.

## Security Boundaries

```text
Identity -> Authentication -> RBAC authorization -> Kubernetes API
Pod identity -> Kubernetes/cloud permissions -> Protected resources
Pod network -> NetworkPolicy enforcement -> Allowed connections
```

These controls solve different problems. RBAC does not filter ordinary application traffic, and NetworkPolicy does not authenticate application users.

## Practical Checks

```bash
kubectl config current-context
kubectl config view --minify
kubectl get serviceaccounts -n <namespace>
kubectl get roles,rolebindings -n <namespace>
kubectl get clusterroles
kubectl get clusterrolebindings
kubectl get networkpolicies -A
kubectl describe networkpolicy <policy-name> -n <namespace>
kubectl auth can-i get pods -n <namespace>
```

`kubectl auth can-i` checks the command's current identity unless another identity is explicitly tested. Avoid exposing credential-bearing output.

## Common Mistakes

- Creating a Role without a binding does not grant permissions.
- A ServiceAccount is an identity, not a permission set.
- Broad permissions such as `cluster-admin` violate least privilege when workloads need only limited access.
- NetworkPolicy enforcement depends on the networking implementation; policy objects alone do not guarantee traffic isolation.
- NetworkPolicy is not a substitute for application authorization or TLS.

## Key Takeaways

Use least-privilege RBAC for Kubernetes API access, dedicated workload identities for resource access, and NetworkPolicies to limit unnecessary network reachability. Verify each security layer independently.

## Related Lessons

- Lesson 112 — Kubernetes Secrets
- Lesson 109 — Kubernetes Services
- Lesson 120 — End-to-End Kubernetes Troubleshooting Lab
