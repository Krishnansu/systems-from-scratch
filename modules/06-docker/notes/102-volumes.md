# Lesson 102 — Volumes

## Objectives
- Explain container writable-layer lifecycle versus persistent storage.
- Distinguish Docker volumes, bind mounts, and tmpfs mounts.
- Mount and inspect persistent data using Docker CLI commands.
- Identify production durability and storage concerns.
- Distinguish a database system from the storage it uses.

## Concept Summary
A container's writable layer belongs to that container and is removed with it. Docker volumes and bind mounts provide storage whose lifecycle can be independent of a container.

A **database is software that manages structured data**; a **volume is a filesystem storage mechanism**. When PostgreSQL runs in a container, PostgreSQL manages tables, indexes, transactions, and database files. A mounted volume can keep those files independent of the PostgreSQL container's lifecycle.

## Core Ideas
- **Writable layer:** stores container-specific filesystem changes; unsuitable as the sole location for data that must survive container removal.
- **Docker volume:** Docker-managed storage identified by a name. A named volume can be reused by replacement containers.
- **Bind mount:** exposes a specified host filesystem path inside a container. Useful for source-code sharing and host-managed files.
- **tmpfs:** temporary memory-backed storage on supported Linux configurations.
- **Mount point:** a path inside the container backed by the mounted storage. Mounting over an existing image directory obscures its original contents while the mount is active.
- **Lifecycle:** removing a container does not normally remove a named volume. Explicit volume removal can delete its data.
- **Database vs. volume:** PostgreSQL understands SQL, tables, indexes, transactions, and recovery. A volume does not understand database concepts; it provides a place for PostgreSQL's files.
- **Database files:** PostgreSQL persists data in files under its data directory (commonly `/var/lib/postgresql/data` in standard container images). Mounting a volume there lets those files outlive the container.
- **Remote/managed database:** if the application connects to PostgreSQL hosted on another machine or by a cloud provider, the application container does not need a Docker volume for the remote database's files. That database's storage is managed separately.
- **Distributed systems:** multiple application replicas commonly connect to one logical database service. They should not each maintain unrelated local copies of the authoritative production data.
- **Host boundary:** a standard local Docker volume is generally tied to its Docker host. It does not automatically provide cross-host replication, failover, or backup.

## Mental Model: Application, Database, and Storage

```text
Client
  |
  v
Application container
  |  sends SQL over a network connection
  v
PostgreSQL server
  |  manages SQL, tables, indexes, transactions
  v
Database files on a mounted Docker volume
     (persistent filesystem storage)
```

The responsibilities are separate:
- **Application:** business logic.
- **PostgreSQL:** database engine and SQL operations.
- **Database files:** persisted database state.
- **Volume:** storage location for those files, independent of the container's writable layer.

See [`../diagrams/volumes-database-mental-model.md`](../diagrams/volumes-database-mental-model.md) for editable diagrams of this relationship, container replacement, and distributed deployment.

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

### PostgreSQL example

```bash
docker volume create postgres-data

docker run -d \
  --name postgres \
  -e POSTGRES_PASSWORD=example \
  -v postgres-data:/var/lib/postgresql/data \
  postgres
```

In `-v postgres-data:/var/lib/postgresql/data`, the left side is the Docker volume and the right side is the path inside the container where PostgreSQL stores its data. Recreating the container and reattaching the same volume can preserve the database files.

This is a simplified learning example. Do not use a hard-coded example password in production; use suitable secret management and follow PostgreSQL's backup and recovery procedures.

The named-volume example demonstrates persistence across container removal. Bind-mount path syntax varies by host environment. Removing a volume deletes its data; do not remove volumes containing important data.

## Production Perspective
- Database files commonly need persistent volumes or suitable external storage.
- Volumes are not backups or replication systems.
- Plan backups, restore testing, capacity monitoring, permissions, security, and failure recovery.
- Replication and failover do not replace backups because deletion or corruption can propagate.
- A mount can hide image files at its target path, causing missing-configuration problems.
- For a managed PostgreSQL service, the provider operates the database infrastructure and its underlying storage; the application connects over the network.
- For self-hosted PostgreSQL, you are responsible for operating the database, securing it, maintaining storage, and planning backups and recovery.
- A local Docker volume usually does not move automatically to another host after host failure. Cross-host storage, replication, and failover need additional architecture.

## Common Mistakes
- Expecting a container writable layer to survive container removal.
- Assuming named volumes are automatically deleted with containers.
- Treating volumes as backups or guarantees against data loss.
- Confusing bind mounts with Docker-managed volumes.
- Forgetting that a mount hides the image's existing files at the mount point.
- Thinking a Docker volume is itself a database.
- Assuming an application container needs a local volume to use a remote managed database.
- Assuming a named volume alone provides distributed replication or high availability.

## Key Takeaways
- Separate application lifecycle from data lifecycle.
- Named volumes are a strong default for persistent container data.
- PostgreSQL is the database engine; the volume is one possible place for its files.
- Multiple application instances can connect over a network to one logical database service.
- Bind mounts explicitly expose host paths and require attention to permissions.
- Persistence alone does not provide backup, recovery, replication, or high availability.

## Reflection Questions
1. Why does a file in the writable layer disappear when its container is removed?
2. How do Docker volumes and bind mounts differ?
3. Why can database data survive container replacement when the same volume is reattached?
4. What happens when an empty host directory is mounted over a populated image directory?
5. Why do persistent volumes still require backups and recovery planning?
6. Is PostgreSQL the same thing as a Docker volume? Explain the responsibility of each.
7. If an application container connects to a managed PostgreSQL service on another host, whose storage holds the database files?
8. Why doesn't one local Docker volume automatically provide high availability across multiple hosts?

## Related Lessons
- Lesson 98 — Layers
- Lesson 99 — Dockerfile
- Lesson 101 — cgroups
- Next: Lesson 103 — Docker Networks
