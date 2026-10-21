# Lesson 104 — Docker Compose

## Learning Objectives

By the end of this lesson, you should be able to:

- Explain why Docker Compose is useful for multi-container applications.
- Describe how a Compose file defines services, networks, and volumes.
- Configure service-to-service communication using service names.
- Distinguish container startup order from application readiness.
- Start, inspect, troubleshoot, and stop a Compose application safely.
- Recognize configuration and data-persistence risks when cleaning up resources.

## Prerequisites

- Lesson 97 — Images
- Lesson 99 — Dockerfile
- Lesson 102 — Volumes
- Lesson 103 — Docker Networks

## 1. Why Docker Compose?

A real application often needs several containers that work together. For example, a web application might require a frontend, an API server, and a database. Starting each container with a long `docker run` command makes the setup difficult to reproduce and maintain.

Docker Compose lets you describe the application's services and their configuration in a YAML file. You can then use a small set of commands to create, inspect, and stop the application as a group.

Compose is declarative: the file describes the desired configuration, and the Compose CLI uses Docker to create and manage the required resources.

## 2. Mental Model

```text
compose.yaml
     |
     v
Docker Compose CLI
     |
     v
Docker Engine
     |
     +---- Containers
     +---- Project network(s)
     +---- Named volume(s)
```

The Compose file is configuration, not a replacement for the Docker Engine. Compose translates the configuration into Docker resources and coordinates their lifecycle.

## 3. Example Architecture: WordPress and MySQL

Consider a local WordPress application backed by MySQL:

- The browser accesses WordPress through a published host port.
- WordPress connects to MySQL using the Compose service name `db` and port `3306`.
- MySQL stores its database files in a named volume called `db-data`.
- Both services join the default Compose project network, so they can discover each other by service name.

The important distinction is that WordPress needs to reach `db:3306` from inside its container. Publishing MySQL's port to the host is not required for this container-to-container connection.

See [the architecture diagram](../diagrams/104-compose-architecture.md) and [the command reference](../commands/104-docker-compose.md).

## 4. Important Compose Fields

- `services`: Defines the containers that make up the application.
- `image`: Selects an image to run.
- `build`: Builds an image from a build context and Dockerfile.
- `ports`: Publishes container ports on the host.
- `environment`: Configures environment variables inside a container.
- `depends_on`: Expresses service startup dependencies and, when configured, health-check conditions.
- `healthcheck`: Defines a check Docker can use to report container health.
- `volumes`: Mounts persistent or otherwise managed storage into containers.
- `networks`: Configures the networks that services join.

Compose creates a default project network when one is not explicitly configured. Services on that network can communicate using their service names and container ports.

## 5. Hands-On Example

Create a directory for the project and add a `compose.yaml` file:

```yaml
services:
  wordpress:
    image: wordpress:latest
    ports:
      - "127.0.0.1:8080:80"
    environment:
      WORDPRESS_DB_HOST: db:3306
      WORDPRESS_DB_USER: wordpress
      WORDPRESS_DB_PASSWORD: ${WORDPRESS_DB_PASSWORD:?Set it in .env}
      WORDPRESS_DB_NAME: wordpress
    depends_on:
      db:
        condition: service_healthy

  db:
    image: mysql:8.4
    environment:
      MYSQL_DATABASE: wordpress
      MYSQL_USER: wordpress
      MYSQL_PASSWORD: ${WORDPRESS_DB_PASSWORD:?Set it in .env}
      MYSQL_ROOT_PASSWORD: ${MYSQL_ROOT_PASSWORD:?Set it in .env}
    volumes:
      - db-data:/var/lib/mysql
    healthcheck:
      test: ["CMD", "mysqladmin", "ping", "-h", "localhost"]
      interval: 5s
      timeout: 3s
      retries: 10

volumes:
  db-data:
```

Create a local `.env` file beside `compose.yaml`:

```dotenv
WORDPRESS_DB_PASSWORD=local_wordpress_password
MYSQL_ROOT_PASSWORD=local_root_password
```

These values are disposable learning examples only. Add `.env` to `.gitignore` and do not commit it. Use appropriate secret management and strong credentials for real deployments. Treat output from configuration commands as potentially sensitive because interpolated environment values may be displayed.

The `latest` tag is convenient for a demonstration but mutable. For reproducible deployments, select maintained, deliberately chosen image versions and update them intentionally.

The WordPress port mapping binds to `127.0.0.1`, limiting access to the local host rather than publishing the service on every host interface. Adjust this deliberately if remote access is required.

## 6. Service Discovery and Networking

Within the Compose network, WordPress connects to MySQL using `db:3306`:

- `db` is the Compose service name and DNS name.
- `3306` is the MySQL container port.
- The host does not need a published MySQL port for this connection.
- `localhost` inside a container refers to that same container, not another service or the host.

Use published ports when a service must be reached from outside its container network, such as a browser accessing WordPress at `http://127.0.0.1:8080`.

## 7. Startup Order, Health, and Readiness

A short-form dependency such as `depends_on: [db]` controls startup order, but it does not mean the database is ready to accept application connections.

The long form with `condition: service_healthy` makes Compose wait for the dependency's configured health check to pass before starting the dependent service. The example defines a MySQL health check and uses that condition for WordPress.

Keep these states separate:

1. The container has started.
2. The service has passed its configured health check.
3. The application can successfully handle the request you care about.

A health check is only as meaningful as the check itself. Passing it does not guarantee that the service will remain healthy or that every application-level operation will succeed.

## 8. Essential Commands

Validate and render the Compose configuration:

```bash
docker compose config
```

Start the application in the background and inspect its services:

```bash
docker compose up -d
docker compose ps
```

Inspect logs:

```bash
docker compose logs
docker compose logs -f db
docker compose logs wordpress
```

Open a MySQL client inside the database container:

```bash
docker compose exec db mysql -u wordpress -p wordpress
```

Stop and remove the Compose containers and project network:

```bash
docker compose down
```

By default, `docker compose down` retains named volumes. To remove Compose-managed named volumes as well:

```bash
docker compose down -v
```

**Warning:** `docker compose down -v` can delete persisted database data. Inspect the resources and understand the consequences before running cleanup commands.

For more commands and troubleshooting guidance, see [104 — Docker Compose commands](../commands/104-docker-compose.md).

## 9. Troubleshooting Checklist

When the application does not work, investigate layer by layer:

1. Run `docker compose ps` and inspect the state of each service.
2. Read the relevant service logs with `docker compose logs <service>`.
3. Check health-check status and whether the dependency has become healthy.
4. Verify service names and container ports, especially `db:3306`.
5. Check environment variable names, database name, username, and credentials.
6. Confirm the application is listening on the expected container port and that host port publishing is correct.
7. Check that persistent storage is mounted at the intended location.
8. Validate the rendered configuration with `docker compose config`, while avoiding accidental disclosure of secrets.

Do not jump straight to deleting volumes. First identify the failure and preserve data that matters.

## 10. Compose and Kubernetes

Compose is especially useful for local development, testing, demos, and managing a multi-container application on a single Docker host. It makes an environment easier to describe and reproduce.

Kubernetes addresses a different scale of orchestration, including cluster-level scheduling and reconciliation. Compose is not a replacement for Kubernetes when cluster orchestration and its associated capabilities are required.

## Common Misconceptions

- **Compose is a container runtime:** No. Compose configures and coordinates Docker resources through the Docker Engine.
- **Services must publish ports to communicate:** No. Services on the same Compose network can use service names and container ports.
- **`depends_on` always waits for readiness:** No. Readiness waiting requires an appropriate health check and a supported health condition.
- **A healthy container guarantees a working application:** No. Container health and successful application requests are different signals.
- **`docker compose down` always deletes database data:** Not normally when data is stored in a named volume. `down -v` removes Compose-managed named volumes too.
- **A `.env` file is automatically safe:** No. Protect it from version control and avoid exposing its values in logs or shared output.

## Key Takeaways

- Compose describes a multi-container application in a YAML file.
- Compose manages services and related networks and volumes through Docker.
- Services on the default Compose network can discover each other by service name.
- Container ports and published host ports serve different purposes.
- Startup order, health-check success, and application readiness are distinct.
- Named volumes normally survive `docker compose down`; `down -v` can delete persisted data.
- Configuration and troubleshooting should be deliberate, especially around credentials and persistent storage.

## Reflection Questions

1. What problem does Compose solve compared with manually running several `docker run` commands?
2. Why can WordPress reach MySQL through `db:3306` without publishing MySQL's port on the host?
3. What is the difference between short-form `depends_on` and `condition: service_healthy`?
4. What happens to a named volume after `docker compose down` versus `docker compose down -v`?
5. If WordPress cannot connect to MySQL, what would you inspect first, and why?

## Next Lesson

Lesson 105 — Kubernetes Architecture.
