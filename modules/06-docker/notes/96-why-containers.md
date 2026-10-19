# Lesson 96 — Why Containers?

## Objectives
- Explain why application environments must be reproducible.
- Distinguish processes, containers, images, and virtual machines.
- Understand the roles of namespaces, cgroups, filesystem isolation, and security controls.
- Identify container benefits and limitations.

## Prerequisites
- Linux processes, memory, and filesystems
- Networking and firewall fundamentals

## Theory
Containers package application files and user-space dependencies into a consistent deployment artifact and run processes with configured isolation. Typical Linux containers share the host kernel rather than booting a separate guest kernel.

## Real World Example
A service with a particular language runtime and library set can be built into an image and deployed across development, testing, and production. Configuration, networking, secrets, and external services must still be managed separately.

## Deep Dive
- Images are packaged templates; containers are runtime instances; processes execute programs.
- Namespaces isolate views of system resources; cgroups account for and limit resource use.
- Filesystem isolation and security controls contribute to workload boundaries.
- Virtual machines run guest operating systems; typical Linux containers share the host kernel.
- Images improve deployment consistency but do not guarantee identical runtime behavior or automatic security.
- Container writable layers should not be treated as durable storage; use appropriate persistent storage for data that must survive replacement.
- Production concerns include resource limits, network access, secrets, observability, image provenance, and least privilege.

## Hands-on Exercise
1. Diagnose why copying source code alone may not resolve a missing-library deployment error.
2. Explain how separate containers help with conflicting dependency versions.
3. Identify where data should live if it must survive container removal.
4. Choose between containers and virtual machines for workloads with different kernel requirements.

## Common Misconceptions
- A container is not simply a small virtual machine.
- Images and running containers are different things.
- Containers do not eliminate all environment differences.
- Containers are not automatically secure.
- Container writable-layer data is not guaranteed to survive container removal.

## Summary
Containers package applications and user-space dependencies while using operating-system mechanisms to isolate running processes. They improve deployment consistency and efficiency, but persistent storage, networking, security, and operations remain separate concerns.

## Key Takeaways
- Runtime dependencies are part of deployment.
- Images are templates; containers are runtime instances.
- Typical Linux containers share the host kernel.
- Containers and VMs offer different isolation and compatibility trade-offs.
- Reproducible packaging is useful but does not solve every production problem.

## Reflection Questions
1. Why is source code alone not always enough to deploy an application?
2. What is the key architectural difference between containers and VMs?
3. How can containers use different dependencies while sharing a kernel?
4. Why can a correctly packaged container still fail in production?
5. What happens to data stored only in a container's writable filesystem when it is removed?

## What's Next
Lesson 97 — Images. Learn how container images are built, tagged, stored, and distributed.
