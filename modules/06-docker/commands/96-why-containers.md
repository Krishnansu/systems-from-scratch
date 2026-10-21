# Lesson 96 — Why Containers?

These commands help inspect containers and understand their lifecycle.

## Inspect the Docker environment

```bash
docker version
docker info
```

- `docker version` shows client and server versions.
- `docker info` shows details about the Docker daemon and runtime environment.

## List containers

```bash
docker ps
docker ps -a
```

- `docker ps` lists running containers.
- `docker ps -a` includes stopped containers.

## Run and inspect a container

```bash
docker run -d --name sfs-web nginx:alpine
docker inspect sfs-web
docker logs sfs-web
docker stop sfs-web
docker rm sfs-web
```

The detached container runs in the background. `inspect` exposes configuration and runtime state; `logs` displays its output. Stop the container before removing it.

## Run a temporary container

```bash
docker run --rm alpine echo "Hello from a container"
```

`--rm` removes the container after it exits. It does not remove the image.
