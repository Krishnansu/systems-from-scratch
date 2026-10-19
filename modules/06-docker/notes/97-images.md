# Lesson 97 — Images

## Objectives
- Explain why container images exist.
- Distinguish images, containers, registries, tags, and digests.
- Understand the image build, publish, pull, and run lifecycle.
- Identify production practices for reproducible and secure image deployment.

## Prerequisites
- Lesson 96 — Why Containers?
- Basic Linux filesystem and process concepts

## Theory
A container image is a packaged filesystem and metadata used to create containers. It commonly includes application files, user-space dependencies, a runtime, a default command, and configuration defaults. It does not contain an independently booted kernel.

A container is a runtime instance created from an image. It has runtime configuration and a writable layer separate from the image's read-only layers.

## Real World Example
A team builds `catalog-api:1.4.0`, publishes it to a registry, and deploys it to testing and production. Both environments can use the same image while receiving different runtime configuration and secrets.

## Deep Dive
- **Image:** packaged artifact containing filesystem layers and metadata.
- **Container:** runtime instance created from an image; its writable changes do not modify the image.
- **Registry:** service that stores and distributes images. Building, pushing, pulling, and running are separate operations.
- **Tag:** human-readable image reference such as `1.4.0` or `latest`. Tags can be moved to different image content.
- **Digest:** content-based identifier, commonly used to pin the exact artifact. For multi-platform images, a digest may identify an image index containing platform-specific images.
- **Lifecycle:** build → push → pull → create/start container. Layer caching can reduce repeated downloads and builds.
- **Reproducibility:** use explicit versions and, where appropriate, digests. A digest identifies content but does not guarantee that the image is secure, compatible, or healthy.
- **Runtime configuration:** supply environment-specific configuration and secrets separately from the image. Avoid baking secrets into image layers, build arguments, or build artifacts.
- **Production security:** use trusted base images, scan for vulnerabilities, track provenance, restrict publishing permissions, and run with least privilege.
- **Troubleshooting:** a successful image pull proves availability of the artifact, not successful application startup. Inspect container status, exit code, logs, command/entrypoint, runtime configuration, and dependencies.

## Hands-on Exercise
1. Explain why three replicas of one service can be created from the same image.
2. Explain why pulling `payments-api:latest` on different days may produce different content.
3. Inspect a local image with `docker image inspect` and identify its command and metadata.
4. Diagnose a container that exits after its image is pulled successfully.

Useful commands:
```bash
docker image ls
docker image inspect nginx
docker pull nginx:alpine
```

## Common Misconceptions
- An image is not the same as a running container.
- `latest` does not guarantee the newest or safest image.
- Tags are not necessarily immutable.
- A successful pull does not prove that the application can start.
- Image digests improve artifact identity but do not guarantee runtime correctness.
- Secrets should not be embedded in image layers.

## Summary
Images package an application's filesystem, dependencies, and startup metadata for distribution. Containers are runtime instances of those artifacts. Registries distribute images, tags provide convenient names, and digests support content-based identification. Reproducible deployments also require appropriate runtime configuration, secrets management, and operational checks.

## Key Takeaways
- Build and publish an artifact, then deploy that artifact consistently.
- Containers are instances; images are the packaged templates.
- Tags can change; digests identify content more precisely.
- Configuration and secrets generally belong outside the image.
- Pull success and application health are different signals.

## Reflection Questions
1. What is the difference between a container image and a container?
2. Why can two servers pulling the same tag at different times receive different image content?
3. What is the advantage of using an image digest in a production deployment?
4. Why does pulling an image not guarantee that its application will start successfully?
5. Why should environment-specific secrets and configuration generally be supplied separately from the image?

## What's Next
Lesson 98 — Layers. Learn how image layers and caching work and how they affect build speed, storage, and image design.
