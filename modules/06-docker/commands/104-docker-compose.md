# Lesson 104 — Docker Compose Command Reference

## Validate Configuration

```bash
docker compose config
```

Renders and validates the Compose configuration, including variable interpolation. Treat the output as potentially sensitive because interpolated credentials may appear in it.

## Start and Inspect

```bash
docker compose up -d
docker compose ps
docker compose images
```

- `up -d`: creates or updates the required resources and starts services in the background.
- `ps`: shows the state of Compose services and their containers.
- `images`: lists images used by the Compose project.

## Read Logs

```bash
docker compose logs
docker compose logs -f db
docker compose logs wordpress
```

Use service-specific logs to narrow down startup, connection, and application failures. Press `Ctrl+C` to stop following logs; this does not stop the services.

## Execute a Command in a Service

```bash
docker compose exec db mysql -u wordpress -p wordpress
```

This opens a MySQL client in the running `db` service. Enter the database user's password when prompted.

## Stop and Clean Up

```bash
docker compose down
```

Removes the project's containers and network. Named volumes are normally retained.

```bash
docker compose down -v
```

**Destructive:** also removes Compose-managed named volumes. This can permanently remove database data. Verify the volume and its contents before running this command.

## Troubleshooting Checklist

1. Check service state: `docker compose ps`.
2. Inspect the failing service's logs: `docker compose logs <service>`.
3. Check the dependency's health-check status.
4. Verify that service names and container ports are correct, such as `db:3306`.
5. Confirm environment variables, database name, username, and credentials.
6. Confirm the application is listening on the expected container port and that host port publishing is correct.
7. Confirm persistent volumes are mounted where expected.
8. Validate the rendered configuration with `docker compose config`, protecting sensitive output.

## Configuration Safety

- Keep local `.env` files out of version control; add `.env` to `.gitignore`.
- Example passwords are for disposable local learning only.
- Avoid sharing configuration output that contains secrets.
- Bind local development ports to `127.0.0.1` when access should be limited to the host, for example `127.0.0.1:8080:80`.
- Avoid publishing internal database ports unless host access is genuinely required.
- Use deliberate, maintained image versions for reproducible deployments rather than relying on a mutable `latest` tag.

## Related Lessons

- [102 — Volumes](102-volumes.md)
- [103 — Docker Networks](103-docker-networks.md)
