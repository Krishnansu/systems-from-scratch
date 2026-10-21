# Lesson 102 — Volumes

A Docker volume is storage managed by Docker that can outlive a container. It is not a database: a database such as PostgreSQL is software that manages data, while a volume can persist the files that software stores.

## Create and inspect a named volume

```bash
docker volume create sfs-data
docker volume ls
docker volume inspect sfs-data
```

## Write data to a named volume

```bash
docker run --rm --mount source=sfs-data,target=/data alpine sh -c 'echo "persisted data" > /data/example.txt'
```

The container is removed when the command exits, but the named volume remains.

## Read the data from another container

```bash
docker run --rm --mount source=sfs-data,target=/data alpine cat /data/example.txt
```

This demonstrates persistence across container lifecycles when the same named volume is mounted again.

## Use a bind mount

From a directory you want to expose inside the container:

```bash
docker run --rm --mount type=bind,source="$(pwd)",target=/workspace alpine ls -la /workspace
```

A bind mount maps a specific host path into the container. The host path must exist and be accessible to Docker. `$(pwd)` is common in Linux/macOS shells and Git Bash; PowerShell uses different syntax.

## Mount storage for PostgreSQL

For a PostgreSQL container, a named volume is commonly mounted at the database data directory:

```bash
docker volume create postgres-data
docker run -d --name sfs-postgres -e POSTGRES_PASSWORD=change-me -v postgres-data:/var/lib/postgresql/data postgres:alpine
docker logs sfs-postgres
docker inspect sfs-postgres
```

Use a suitable secret instead of `change-me` outside a disposable local demonstration. PostgreSQL initialization can take a short time; check logs before connecting. The volume persists database files after the container is removed, provided the volume itself is retained.

## Remove the demonstration containers

```bash
docker stop sfs-postgres
docker rm sfs-postgres
```

**Data safety:** These commands deliberately leave `postgres-data` and `sfs-data` intact. Do not run `docker volume rm` or `docker volume prune` unless you have verified that the volumes contain no data you need. Volume persistence is not a backup, and a standard local named volume does not automatically replicate data across Docker hosts. Applications connecting to a remote database generally do not need a local volume for that remote database's files.
