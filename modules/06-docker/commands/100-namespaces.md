# Lesson 100 — Namespaces

Namespaces isolate views of system resources. These commands demonstrate container process visibility and, on Linux hosts, allow you to inspect namespace identifiers.

## Start a container for inspection

```bash
docker run -d --name sfs-ns alpine sleep 300
docker inspect sfs-ns
docker top sfs-ns
docker exec sfs-ns ps
```

- `docker inspect` shows container configuration and runtime state.
- `docker top` lists processes associated with the container.
- `docker exec` runs a command inside a running container. The availability of `ps` depends on the image.

## Find the container's host-visible PID

```bash
docker inspect --format '{{.State.Pid}}' sfs-ns
```

On a native Linux host, copy the PID printed by this command and substitute it for `PID` below:

```bash
lsns
readlink /proc/PID/ns/pid
readlink /proc/PID/ns/mnt
readlink /proc/PID/ns/net
readlink /proc/PID/ns/uts
```

These commands list namespaces and display namespace identifiers for the selected process. Namespace files and available inspection tools can vary by host and permissions.

## Clean up

```bash
docker stop sfs-ns
docker rm sfs-ns
```

**Platform note:** Host `/proc` and `lsns` inspection is intended for native Linux. On Docker Desktop, the Docker daemon and containers run inside a Linux VM, so the container PID may not identify a process in the Windows or macOS host's `/proc`. Avoid `--pid=host`, `--network=host`, and privileged containers unless you understand the isolation changes they introduce.
