# Lesson 98 — Layers

## Objectives
- Explain how image layers support image construction and distribution.
- Understand build-cache reuse and invalidation.
- Distinguish image layers from a container's writable layer.
- Identify layer-related performance and security risks.

## Prerequisites
- Lesson 96 — Why Containers?
- Lesson 97 — Images

## Concept Summary
Container images are assembled from filesystem layers and image configuration. Layers allow filesystem content to be reused across builds and images. Build caching avoids repeating work when the relevant instructions and inputs have not changed.

## Core Ideas
- **Image layers:** Represent filesystem changes that combine into the image's final filesystem. Actual layer boundaries depend on the builder and instruction.
- **Build cache:** A builder can reuse prior results when the instruction and relevant inputs satisfy its cache rules. A cache hit is an optimization, not proof of correctness or security.
- **Instruction ordering:** Copy relatively stable dependency manifests before frequently changing source files when practical. This can preserve the dependency-installation cache when only application code changes.
- **Cache invalidation:** Changes to an instruction, its relevant inputs, or preceding build results can require subsequent steps to run again.
- **Image versus container:** Image layers provide the packaged filesystem. A container's writable layer stores container-specific filesystem changes.
- **Persistence:** The writable layer is tied to the container lifecycle. Use volumes or bind mounts for data that must survive container replacement.
- **Security:** Deleting a secret in a later layer does not necessarily remove it from earlier layers. Avoid putting secrets into image layers or build artifacts.

## Practical Example
```dockerfile
FROM python:3.12-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
CMD ["python", "app.py"]
```

Copying `requirements.txt` separately allows the dependency-installation result to be reused when application source changes but the dependency inputs remain unchanged.

## Production Perspective
- Optimize build speed by separating stable inputs from frequently changing files.
- Keep the build context controlled with an appropriate `.dockerignore`.
- Do not assume a cache hit guarantees fresh dependencies, reproducibility, or a secure artifact.
- Use volumes or bind mounts for persistent runtime data.
- Never rely on deleting a secret in a later layer to remove it from image history.

## Commands
```bash
docker image ls
docker image history IMAGE_NAME
docker build -t demo-app .
```

`docker image history` helps inspect image history but does not expose every detail of modern build caching or all files in every layer.

## Common Mistakes
- Assuming every Dockerfile instruction creates a filesystem layer.
- Copying all source files before dependency installation when this unnecessarily invalidates the cache.
- Treating cached build results as proof of correctness or security.
- Confusing image layers with persistent volumes.
- Assuming deleting a file in a later layer erases it from earlier layers.

## Key Takeaways
- Layers enable reuse and more efficient image distribution.
- Cache reuse depends on instructions and relevant inputs.
- Stable dependency inputs should precede frequently changing source when practical.
- Container writable-layer changes do not modify the original image.
- Keep secrets out of image layers and build artifacts.

## Reflection Questions
1. What problem do image layers solve?
2. Why can copying `requirements.txt` before application source improve build performance?
3. Why might changing `requirements.txt` invalidate the dependency-installation cache?
4. How do read-only image layers differ from a container's writable layer?
5. Why can deleting a secret in a later layer still leave a security risk?

## Related Lessons
- Lesson 96 — Why Containers?
- Lesson 97 — Images
- Lesson 99 — Dockerfile

## What's Next
Lesson 99 — Dockerfile. Study Dockerfile instructions, build context, and practices for producing reliable images.
