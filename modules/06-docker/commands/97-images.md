# Lesson 97 — Images

## List and download images

```bash
docker image ls
docker pull nginx:alpine
```

`docker image ls` lists images stored locally. `docker pull` downloads an image from a registry.

## Inspect image metadata and history

```bash
docker image inspect nginx:alpine
docker image history nginx:alpine
```

- `inspect` displays image configuration, IDs, tags, and other metadata.
- `history` shows the image's recorded build-layer history.

## Run a container from an image

```bash
docker run -d --name sfs-nginx -p 8080:80 nginx:alpine
docker ps
docker logs sfs-nginx
```

Open `http://localhost:8080` to test the web server. The port mapping forwards host port 8080 to container port 80.

## Stop and remove the container

```bash
docker stop sfs-nginx
docker rm sfs-nginx
```

Removing the container does not remove the image. Avoid removing images that other projects still use.
