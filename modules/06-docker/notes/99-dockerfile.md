# Lesson 99 — Dockerfile

## Objectives
- Understand how a Dockerfile defines an image build.
- Distinguish build-time instructions from container startup behavior.
- Understand the build context, `.dockerignore`, and multi-stage builds.

## Prerequisites
- Lesson 96 — Why Containers?
- Lesson 97 — Images
- Lesson 98 — Layers

## Theory
A Dockerfile is a recipe used by an image builder. The build context is the set of files made available to the build. The resulting image contains filesystem layers and metadata; a container is a runtime instance of that image.

Common instructions:
- `FROM`: selects a base image and starts a build stage.
- `WORKDIR`: sets the working directory for subsequent instructions.
- `COPY`: copies files from the build context or another stage.
- `RUN`: executes a command while building the image.
- `CMD`: defines the default command or default arguments used at container startup.
- `ENTRYPOINT`: defines the executable intended to run when the container starts.
- `ENV`: sets image-level environment defaults; it is not a secret store.

Example:

```dockerfile
FROM python:3.12-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY app.py .
CMD ["python", "app.py"]
```

## Real World Example
A backend service can be built into an image once and deployed to development, staging, and production. Each environment supplies its own runtime configuration, while the image remains the same artifact.

## Deep Dive

### Build time vs. runtime
- `RUN` executes during image construction. It is appropriate for installing dependencies or compiling code.
- `CMD` and `ENTRYPOINT` configure the container's startup process.
- `RUN python app.py` normally attempts to launch the application during the build; it does not define the normal startup command for containers created from the image.

### CMD vs. ENTRYPOINT
With no `ENTRYPOINT`, `CMD` can specify the complete default command:

```dockerfile
CMD ["python", "app.py"]
```

A runtime command such as `docker run my-app python worker.py` replaces that default command.

Together, `ENTRYPOINT` and `CMD` commonly define an executable and its default arguments:

```dockerfile
ENTRYPOINT ["python", "app.py"]
CMD ["--port", "8080"]
```

The default is `python app.py --port 8080`. Running `docker run my-app --port 9090` replaces the default arguments, yielding `python app.py --port 9090`. To replace the executable, Docker supports `--entrypoint`.

Prefer exec-form arrays, such as `CMD ["python", "app.py"]`, for predictable argument handling and signal delivery. Shell-form instructions have different shell and signal behavior.

### Build context and .dockerignore
The final argument in `docker build -t catalog-api .` is the build context. `COPY` normally cannot access files outside that context. A `.dockerignore` file excludes unnecessary or sensitive files from the context, reducing transfer and accidental inclusion.

Example `.dockerignore` entries:

```text
.git
.venv
__pycache__
*.pyc
.env
```

Review exclusions carefully: ignored files cannot be copied from the context into the image.

### Layer caching
Build instructions and their relevant inputs affect cache reuse. Copy relatively stable dependency manifests and install dependencies before copying frequently changing source files. Changing a dependency manifest can invalidate the dependency-installation layer and require the installation step to run again.

### Multi-stage builds
Multi-stage builds separate compilation tools and intermediate files from the final runtime image. For example, a Go builder stage can compile a binary that is copied into a smaller runtime stage. The final stage must still include required runtime dependencies, certificates, and other files.

### Configuration and security
- Keep credentials out of image contents and build arguments that may be exposed in build metadata or history. Use suitable secret mechanisms for build-time secrets.
- Supply environment-specific configuration and runtime secrets through appropriate deployment or secret-management mechanisms.
- Default, non-sensitive configuration may be included in the image.
- Use maintained base images, minimize unnecessary files, and run as a non-root user where practical.

## Hands-on Exercise
1. Build an image with `docker build -t catalog-api .` and inspect it with `docker image inspect catalog-api`.
2. Compare `RUN python app.py` with `CMD ["python", "app.py"]`. Explain when each executes.
3. Add `.venv` and `.git` to `.dockerignore`. Explain how this affects the build context.
4. Create a Dockerfile with `ENTRYPOINT ["python", "app.py"]` and `CMD ["--port", "8080"]`. Run it with the default arguments and with `--port 9090`.
5. Explain which files and tools can be excluded from a final image by using a multi-stage build.

## Common Misconceptions
- A Dockerfile is not the image; it describes how to build one.
- The build context is not automatically the entire filesystem on the host.
- `RUN` is a build-time instruction, while `CMD` and `ENTRYPOINT` define startup behavior.
- `CMD` does not always mean arguments: without an `ENTRYPOINT`, it can define the complete default command.
- `.dockerignore` excludes files from the build context; multi-stage builds control what is copied into the final stage.
- An image is not a safe place for credentials merely because its filesystem is read-only at runtime.
- A smaller image is not automatically secure or production-ready; runtime dependencies and operational requirements still matter.

## Summary
A Dockerfile defines how an image is assembled. Instruction ordering affects cache reuse, `.dockerignore` controls the build context, and multi-stage builds separate build tooling from runtime contents. `RUN` operates during the build; `CMD` and `ENTRYPOINT` define startup behavior. Runtime configuration and secrets should be managed separately from image contents.

## Key Takeaways
- Dockerfile = build recipe; build context = available input files; image = packaged artifact; container = runtime instance.
- Put stable dependency inputs before frequently changing application source to improve caching.
- `ENTRYPOINT` defines the executable; `CMD` supplies defaults and can also define the whole command when no entrypoint exists.
- Use `.dockerignore` and multi-stage builds for their distinct purposes.
- Keep secrets out of images and use the same image across environments when possible.

## Reflection Questions
1. What is the difference between a Dockerfile, build context, image, and container?
2. Why is `RUN python app.py` not the normal way to configure application startup?
3. How do `CMD` and `ENTRYPOINT` behave together, and how can runtime arguments override `CMD` defaults?
4. How do `.dockerignore` and multi-stage builds solve different problems?
5. Why should credentials and environment-specific configuration generally be supplied separately from the image?

## What's Next
Lesson 100 — Namespaces. Explore how Linux namespaces provide isolation for container processes and their view of system resources.
