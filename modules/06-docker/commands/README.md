# Docker Commands Reference

A lesson-wise reference for important commands from Module 06 — Docker. Use these alongside the lesson notes for quick revision and hands-on practice.

## Lessons

- [96 — Why Containers?](96-why-containers.md)
- [97 — Images](97-images.md)
- [98 — Layers](98-layers.md)
- [99 — Dockerfile](99-dockerfile.md)
- [100 — Namespaces](100-namespaces.md)
- [101 — cgroups](101-cgroups.md)
- [102 — Volumes](102-volumes.md)
- [103 — Docker Networks](103-docker-networks.md)

## General notes

- Commands assume Docker is installed and the Docker daemon is running.
- Some commands create containers, networks, volumes, or images; clean up only resources created for the exercise.
- Linux host-level inspection commands may behave differently on Docker Desktop because Docker Desktop runs containers inside a Linux VM.
- Bind-mount examples using `$(pwd)` work in common Linux/macOS shells and Git Bash. PowerShell uses different syntax.
- Be careful with cleanup commands. Removing a container is not the same as removing a volume, and deleting a volume can permanently delete its data.
- Port publishing can expose a service beyond the intended audience. Use an explicit loopback binding when access should be limited to the Docker host, and avoid publishing internal service ports unnecessarily.
