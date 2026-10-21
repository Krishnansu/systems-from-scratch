# Lesson 102 — Volumes

## Objectives
- Explain container writable-layer lifecycle versus persistent storage.
- Distinguish Docker volumes, bind mounts, and tmpfs mounts.
- Mount and inspect persistent data using Docker CLI commands.
- Identify production durability and storage concerns.

## Concept Summary
A container's writable layer belongs to that container and is removed with it. Docker volumes and bind mounts provide storage whose lifecycle can be independent of a container.

## Core Ideas
- **Writable layer:** stores container-specific filesystem changes; unsuitable as the sole location for data that must survive container removal.
- **Docker volume:** Docker-managed storage identified by a name. A named volume can be reused by replacement containers.
- **Bind mount:** exposes a specified host filesystem path inside a container. Useful for source-code sharing and host-managed files.
- **tmpfs:** temporary memory-backed storage on supported Linux configurations.
- **Mount point:** a path inside the container backed by the mounted storage. Mounting over an existing image directory obscures its original contents while the mount is active.
- **Lifecycle:** removing a container does not normally remove a named volume. Explicit volume removal can delete its data.

## Practical Example

```bash
# Create and inspect a named volume
docker volume create sfs-data
docker volume inspect sfs-data

# Write data, then let Docker remove the container
docker run --rm --mount source=sfs-data,target=/data alpine \
  sh -c 'echo "persistent data" > /data/message.txt'

# A new container reads the same volume
docker run --rm --mount source=sfs-data,target=/data alpine \
  cat /data/message.txt

# Inspect volumes
docker volume ls

# Development example: mount the current host directory
docker run --rm --mount type=bind,source="$(pwd)",target=/workspace alpine \
  ls -la /workspace

# Remove the learning volume only when no longer needed
docker volume rm sfs-data
```

The named-volume example demonstrates persistence across container removal. Bind-mount path syntax varies by host environment. Removing a volume deletes its data; do not remove volumes containing important data.

## Production Perspective
- Database files commonly need persistent volumes or suitable external storage.
- Volumes are not backups or replication systems.
- Plan backups, restore testing, capacity monitoring, permissions, security, and failure recovery.
- Replication and failover do not replace backups because deletion or corruption can propagate.
- A mount can hide image files at its target path, causing missing-configuration problems.

## Common Mistakes
- Expecting a container writable layer to survive container removal.
- Assuming named volumes are automatically deleted with containers.
- Treating volumes as backups or guarantees against data loss.
- Confusing bind mounts with Docker-managed volumes.
- Forgetting that a mount hides the image's existing files at the mount point.

## Key Takeaways
- Separate application lifecycle from data lifecycle.
- Named volumes are a strong default for persistent container data.
- Bind mounts explicitly expose host paths and require attention to permissions.
- Persistence alone does not provide backup, recovery, or high availability.

## Reflection Questions
1. Why does a file in the writable layer disappear when its container is removed?
2. How do Docker volumes and bind mounts differ?
3. Why can database data survive container replacement when the same volume is reattached?
4. What happens when an empty host directory is mounted over a populated image directory?
5. Why do persistent volumes still require backups and recovery planning?

## Related Lessons
- Lesson 98 — Layers
- Lesson 99 — Dockerfile
- Lesson 101 — cgroups
- Next: Lesson 103 — Docker Networks
