# Lesson 104 — Docker Compose Architecture

## Compose Resource Model

```mermaid
flowchart TD
    A[compose.yaml] --> B[Docker Compose CLI]
    B --> C[Docker Engine]
    C --> D[WordPress container]
    C --> E[MySQL container]
    C --> F[Project network]
    C --> G[Named volume: db-data]
    D --- F
    E --- F
    E --> G
```

The Compose file describes the desired services and resources. The Compose CLI coordinates their lifecycle through the Docker Engine.

## WordPress and MySQL Communication

```mermaid
flowchart LR
    Browser[Browser on host] -->|127.0.0.1:8080| WP[WordPress container :80]
    WP -->|db:3306 over project network| DB[MySQL container :3306]
    DB --> Data[(Named volume: db-data)]
```

- The browser uses the published host port `127.0.0.1:8080` to reach WordPress.
- WordPress resolves the service name `db` on the Compose network and connects to MySQL's container port `3306`.
- MySQL persists database files in the named volume mounted at `/var/lib/mysql`.
- MySQL does not need a host-published port for WordPress to communicate with it over the Compose network.

## Dependency Startup and Health

```mermaid
flowchart TD
    A[Compose starts db container] --> B[Configured MySQL health check runs]
    B --> C{Health check passes?}
    C -->|No| B
    C -->|Yes| D[Compose can start WordPress]
    D --> E[Application request is attempted]
```

With `depends_on` configured using `condition: service_healthy`, Compose waits for the dependency's configured health check to pass before starting the dependent service. A successful health check is not a guarantee of ongoing availability or of every application request succeeding.

## Cleanup and Data Persistence

```mermaid
flowchart TD
    A[docker compose down] --> B[Remove project containers and network]
    B --> C[Named volume normally retained]
    A --> D[docker compose down -v]
    D --> E[Remove Compose-managed named volumes too]
    E --> F[Persisted database data may be lost]
```

Before using `down -v`, confirm that the volume's data is disposable or safely backed up.
