# Docker Command References

This directory contains practical command references that accompany the Docker lessons. Use these as quick references; consult the lesson notes for the concepts and trade-offs behind each command.

## Lessons

- [96 — Why Containers?](096-why-containers.md)
- [97 — Images](097-images.md)
- [98 — Layers](098-layers.md)
- [99 — Dockerfile](099-dockerfile.md)
- [100 — Namespaces](100-namespaces.md)
- [101 — cgroups](101-cgroups.md)
- [102 — Volumes](102-volumes.md)
- [103 — Docker Networks](103-docker-networks.md)
- [104 — Docker Compose](104-docker-compose.md)

## General Safety Notes

- Commands that remove containers, images, networks, or volumes can cause data loss or disrupt running workloads. Check the target before cleaning up.
- Docker daemon access is powerful; treat access to it as a privileged capability.
- Docker Desktop and Linux Docker Engine can differ in networking, filesystem mounts, and environment-specific behavior.
- Bind mounts expose paths from the host, while named volumes are managed by Docker. Choose deliberately based on the data and workflow.
- Publishing a port makes a container service reachable through the host's network interfaces according to the binding. Use a loopback binding such as `127.0.0.1:8080:80` for host-only development access when appropriate.
- `docker compose down` normally retains named volumes, while `docker compose down -v` can remove Compose-managed named volumes and persisted data.
- Keep `.env` files containing credentials out of version control. Configuration output may include interpolated sensitive values, so inspect it before sharing.
