# Lesson 99 — Dockerfile

## Build an image

Run these commands from the directory containing the intended `Dockerfile`:

```bash
docker build -t catalog-api .
docker image ls catalog-api
```

The `-t` flag assigns the image a name and optional tag. The build context is the final `.` argument.

## Inspect image configuration and history

```bash
docker image inspect catalog-api
docker image history catalog-api
```

Use `inspect` to examine configuration such as the default command, working directory, environment, and exposed-port metadata. Use `history` to review recorded build steps.

## Run the image's default command

```bash
docker run --rm catalog-api
```

`--rm` removes the container after it exits. It does not remove the image.

## Override the default command

```bash
docker run --rm catalog-api python worker.py
```

This illustrates how arguments supplied after the image name can replace a Dockerfile `CMD`. The exact behavior depends on the Dockerfile's `ENTRYPOINT` and `CMD` configuration; an exec-form `ENTRYPOINT` is not replaced by this command.

## Debug a container that exits

```bash
docker ps -a
docker logs CONTAINER_NAME
docker inspect CONTAINER_NAME
```

Replace `CONTAINER_NAME` with the actual container name or ID. `docker run --rm` removes an exited container automatically, so omit `--rm` temporarily when you need to inspect its stopped state or logs afterward.
