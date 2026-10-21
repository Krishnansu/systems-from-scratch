# Lesson 98 — Image Layers

## Examine an image's history

```bash
docker image history nginx:alpine
docker image inspect nginx:alpine
```

Use these commands to examine image history and metadata. The history can help connect image construction steps with layers, though not every history entry necessarily corresponds one-to-one with a separately stored layer.

## Build an image

From a directory containing a `Dockerfile` and its required files:

```bash
docker build -t demo-app .
docker image ls demo-app
docker image history demo-app
```

The final `.` is the build context sent to the builder.

## Rebuild without the build cache

```bash
docker build --no-cache -t demo-app .
```

Use `--no-cache` when you specifically need to rerun build steps rather than reuse cached results. It can make builds slower and does not mean every external dependency is guaranteed to be fresh.

## Compare image sizes

```bash
docker image ls
```

Compare the `SIZE` column when examining how changes to a Dockerfile affect the resulting images. Remember that images can share layers, so reported image sizes should not simply be added to estimate total disk usage.
