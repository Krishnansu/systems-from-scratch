# Lesson 84 — Authorization Fundamentals

## Objectives

- Distinguish authentication from authorization.
- Understand how authorization decisions are made.
- Compare RBAC, ABAC, and ReBAC.
- Recognize object-level authorization vulnerabilities.
- Understand where authorization belongs in production systems.

## Prerequisites

- API fundamentals and REST
- Lesson 83 — Authentication Fundamentals

## Theory

Authorization determines whether an authenticated identity may perform a particular action on a resource. Decisions commonly consider the subject, resource, action, and sometimes contextual attributes.

- **RBAC:** Grants permissions through roles, such as `support-agent` or `admin`.
- **ABAC:** Uses attributes of the subject, resource, and environment to make decisions.
- **ReBAC:** Uses relationships such as ownership, membership, and sharing.
- **Least privilege:** Grant only the permissions required.
- **Deny by default:** Do not grant access when permission cannot be established.

Authentication establishes identity; authorization determines what that identity may do. A valid token does not automatically grant access to every resource.

## Real World Example

Alice has a valid access token but requests Bob's order. The API must check whether Alice is allowed to access that specific order, rather than trusting the supplied order ID.

## Deep Dive

### Authorization boundaries

The API gateway can enforce coarse-grained policies, while the backend service should enforce resource-level permissions and business rules. Authorization must be enforced server-side and protected against paths that bypass the gateway.

### Object-level authorization

IDOR (Insecure Direct Object Reference) and BOLA (Broken Object Level Authorization) occur when an application accesses a resource using a client-supplied identifier without checking whether the caller may access it. Making identifiers difficult to guess is not a substitute for authorization checks.

### Production practices

- Check permissions for each sensitive resource and operation.
- Separate read, update, delete, and administrative permissions where appropriate.
- Re-evaluate permissions when ownership or access can change.
- Audit sensitive actions and access denials without logging credentials or secrets.
- Use `401` for missing or invalid authentication and commonly `403` for authenticated callers lacking permission. Some systems return `404` to avoid revealing resource existence.
- A workload's identity does not automatically authorize access to every downstream service or resource.

## Hands-on Exercise

1. Explain why a valid token does not authorize access to every order.
2. Compare RBAC, ABAC, and ReBAC using an example.
3. Explain how an API can be vulnerable to BOLA.
4. Identify which authorization checks belong in a gateway and which belong in a backend service.

## Common Misconceptions

- Authentication and authorization are interchangeable.
- Hiding a resource in the frontend protects it.
- Hard-to-guess identifiers prevent object-level authorization bugs.
- A gateway check always eliminates the need for backend authorization.
- An authenticated service identity automatically has access to every downstream resource.

## Summary

Authorization controls which actions an identity can perform on specific resources. RBAC, ABAC, and ReBAC provide different ways to express access rules. Production systems must enforce permissions server-side, especially at resource and operation boundaries.

## Key Takeaways

- Authentication answers who the caller is; authorization answers what the caller may do.
- Authorization should consider the specific resource and requested action.
- RBAC, ABAC, and ReBAC can be combined.
- Prevent IDOR/BOLA by checking access to every relevant resource.
- Enforce authorization at trusted server-side boundaries.

## Reflection Questions

1. Why is a valid access token insufficient to authorize access to a particular order?
2. When might RBAC alone be insufficient?
3. Why should a backend enforce resource-level authorization even when the API gateway performs checks?

## What's Next

Lesson 85 — OAuth Fundamentals.
