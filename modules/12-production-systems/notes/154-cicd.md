# Lesson 154 — CI/CD

## Objectives
Understand Continuous Integration, Continuous Delivery, Continuous Deployment, and the architecture of a production CI/CD pipeline.

## CI/CD Fundamentals
CI/CD automates the journey from source-code changes to validated production releases.

- **Continuous Integration (CI):** Developers frequently integrate code into a shared repository. Each integration triggers automated build, test, and quality checks.
- **Continuous Delivery:** Every validated change is packaged and kept ready for production. Production release generally requires an explicit approval or decision.
- **Continuous Deployment:** Every change passing the required pipeline is automatically deployed to production without a normal manual release approval.

CI reduces integration risk through small, frequently validated changes. Continuous Delivery and Deployment extend automation into the release process.

## CI/CD Pipeline
Typical stages:
1. Source checkout: Retrieve the exact source revision identified by its commit SHA.
2. Dependency installation: Install declared, reproducible dependencies.
3. Build: Compile and package the application.
4. Testing: Execute unit, integration, contract, and other automated tests.
5. Quality/security checks: Run linting, static analysis, secret detection, and vulnerability scanning.
6. Artifact creation: Package the application into a JAR, binary, or container image.
7. Artifact publishing: Push the versioned artifact to a registry.
8. Deployment: Deploy the artifact to staging or production.
9. Verification: Execute smoke tests, health checks, and application-level checks.

## CI/CD Architecture
- Source repository: GitHub, GitLab, Bitbucket.
- Orchestrator: Coordinates pipeline triggers, jobs, dependencies, approvals, and execution. Examples: GitHub Actions, Jenkins, GitLab CI.
- Runner/Agent: Executes pipeline commands in an isolated environment.
- Artifact registry: Stores versioned build outputs and container images. Examples: Docker Hub, Amazon ECR.
- Deployment infrastructure: VMs, Kubernetes, or managed cloud platforms where artifacts run.

The orchestrator coordinates work; runners execute it.

## GitHub Actions Example
Workflow files live under `.github/workflows/`.

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
      - uses: actions/checkout@v4
      - uses: actions/setup-java@v4
        with:
          distribution: temurin
          java-version: '21'
      - run: mvn clean verify
```

Required branch protection checks can prevent merging when CI fails.

## Artifacts and Environments
An artifact is the packaged output of a build, such as a JAR, Docker image, or compiled frontend bundle.

- Build once and promote the same artifact across development, staging, and production.
- Use immutable version identifiers or image digests instead of mutable tags alone.
- Keep environment-specific configuration and secrets separate from the artifact.
- Staging provides production-like verification but may not perfectly match production.

## Production Considerations
- **Pipeline as Code:** Version-control pipeline definitions and review changes like application code.
- **Secrets:** Use protected secret stores and short-lived credentials. Never hardcode credentials or expose them in logs.
- **Reproducibility:** Pin dependencies, use lockfiles, and control build environments.
- **Verification:** Deployment success does not guarantee correct business behavior. Check application health, smoke tests, error rates, latency, and business-level outcomes.
- **Database migrations:** Prefer backward-compatible expand-and-contract changes when application versions overlap.
- **Rollback:** Retain previous known-good artifacts. Database changes and external side effects may make rollback incomplete.
- **Security:** Scan source dependencies, artifacts, and container images; preserve artifact provenance.

## Integration with Existing Infrastructure
- Git provides source history and change tracking.
- Docker packages applications consistently.
- Registries store build artifacts.
- Kubernetes orchestrates deployed workloads.
- Readiness probes control traffic eligibility.
- Prometheus, Grafana, and OpenTelemetry support post-deployment monitoring.

CI/CD controls how software is built, validated, and released. Kubernetes controls how deployed workloads run.

## Common Misconceptions
- CI/CD does not necessarily mean automatic production deployment.
- Successful compilation does not prove production readiness.
- Successful deployment does not prove correct business behavior.
- Staging and production should preferably use the same artifact.
- Kubernetes is not itself a complete CI/CD system.
- Rollback cannot always reverse database changes or external side effects.

## Key Takeaways
- CI encourages frequent integration backed by automated validation.
- Continuous Delivery keeps changes ready for release; Continuous Deployment automates the production release decision.
- A pipeline coordinates checkout, build, testing, packaging, publishing, deployment, and verification.
- Build once and promote the same immutable artifact across environments.
- Secure credentials, backward-compatible migrations, observability, and recovery are essential production concerns.

## Reflection Questions
1. Why does infrequent code integration increase risk, and how does CI address it?
2. Differentiate Continuous Delivery and Continuous Deployment. Give a suitable use case for Continuous Delivery.
3. Explain the responsibilities of an orchestrator, runner, and artifact registry.
4. Why should the same Docker image be promoted through staging and production instead of rebuilding it separately?
5. A Kubernetes deployment succeeds and all Pods are ready, but order totals are incorrect. Why might the pipeline have missed this, and what safeguards would help?
6. Why can application rollback become dangerous after a database schema migration? How would you design a safer release?

## Related Lessons
- Lesson 97 — Docker Images
- Lesson 98 — Docker Layers
- Lesson 99 — Dockerfile
- Kubernetes Deployments and Rolling Updates
- Lesson 147 — Health Checks
- Lessons 148–153 — Observability

## Supporting Reference
- [Lesson 154 CI/CD Commands and GitHub Actions Reference](../commands/154-cicd-reference.md)
