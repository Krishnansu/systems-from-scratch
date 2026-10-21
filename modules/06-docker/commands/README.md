# Docker Commands Reference

A lesson-wise reference for important commands from Module 06 — Docker. These commands reinforce the concepts covered in Lessons 96–102.

## Lessons

- [96 — Why Containers?](96-why-containers.md)
- [97 — Images](97-images.md)
- [98 — Layers](98-layers.md)
- [99 — Dockerfile](99-dockerfile.md)
- [100 — Namespaces](100-namespaces.md)
- [101 — cgroups](101-cgroups.md)
- [102 — Volumes](102-volumes.md)

## General notes

- Commands assume Docker is installed and the Docker daemon is running.
- Some commands create containers or images; clean up resources when you no longer need them.
- Linux host-level inspection commands may behave differently on Docker Desktop because Docker Desktop runs containers inside a Linux VM.
- Bind-mount examples use `$(pwd)`, which works in common Linux/macOS shells and Git Bash. PowerShell uses different syntax.
- Be careful with cleanup commands. Removing a container is not the same as removing a volume, and deleting a volume can permanently delete its data.
