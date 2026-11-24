# Lesson 154 — CI/CD Commands and Configuration Reference

## Maven Build and Verification

```bash
mvn dependency:resolve
mvn clean package
mvn clean verify
```

- `dependency:resolve`: Resolve declared dependencies.
- `clean package`: Compile, test, and package the application.
- `verify`: Execute verification checks configured in the Maven lifecycle.

## Node.js Dependency Installation

```bash
npm ci
```

Uses the lockfile for reproducible CI dependency installation.

## Docker Artifact Creation

```bash
docker build -t bookstore:1.0.0 .
docker tag bookstore:1.0.0 registry.example.com/bookstore:1.0.0
docker push registry.example.com/bookstore:1.0.0
```

Prefer immutable version identifiers and registry digests when promoting artifacts.

Inspect a pushed image digest:

```bash
docker inspect --format='{{index .RepoDigests 0}}' bookstore:1.0.0
```

## Kubernetes Deployment

```bash
kubectl set image deployment/bookstore \
  bookstore=registry.example.com/bookstore:1.0.0

kubectl rollout status deployment/bookstore
```

Verify application health:

```bash
curl -f https://staging.example.com/health
```

These commands assume the appropriate Kubernetes context, permissions, deployment, container name, registry access, and health endpoint already exist. They change deployment state; use a non-production environment for experiments.

## GitHub Actions Workflow

Location: `.github/workflows/ci.yml`

```yaml
name: Bookstore CI

on:
  push:
    branches: [main]
  pull_request:
    branches: [main]

jobs:
  build-and-test:
    runs-on: ubuntu-latest

    steps:
      - name: Checkout source
        uses: actions/checkout@v4

      - name: Set up Java
        uses: actions/setup-java@v4
        with:
          distribution: temurin
          java-version: '21'

      - name: Build and test
        run: mvn clean verify
```

Important fields:
- `on`: Pipeline triggers.
- `jobs`: Independent or dependent units of work.
- `runs-on`: Runner environment.
- `steps`: Ordered operations within a job.
- `uses`: Reusable action.
- `run`: Shell command.

## Recommended Pipeline Sequence

1. Pull request: checkout, build, tests, static analysis, security checks.
2. Merge to main: repeat required checks and create a release artifact.
3. Publish: push the immutable image to a registry.
4. Staging: deploy the same image and execute smoke tests.
5. Production: release following the configured approval policy.
6. Verification: monitor health, errors, latency, and business behavior.

## Safety Notes

- Store credentials in protected CI/CD secrets or use workload identity.
- Never print secrets or commit them to workflow files.
- Do not use mutable image tags as the only release identifier.
- Do not deploy to production from an untrusted pull-request workflow.
- Retain previous known-good artifacts for recovery.
- Avoid destructive migration or deployment experiments against production.
- No cleanup is required for the read-only inspection commands; Docker build/push and Kubernetes deployment commands create or change resources.
