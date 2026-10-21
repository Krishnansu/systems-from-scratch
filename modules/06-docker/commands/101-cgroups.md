# Lesson 101 — cgroups

Control groups (cgroups) account for and constrain resource usage. Docker exposes several resource controls through `docker run` and usage information through `docker stats`.

## Observe container resource usage

```bash
docker stats
docker stats --no-stream
```

The first command continuously updates resource statistics for running containers. `--no-stream` prints a single snapshot.

## Apply a memory limit

```bash
docker run --rm --memory=512m alpine sh -c 'sleep 300'
```

This applies a 512 MiB memory limit to the container. The example is intended to demonstrate configuration; it does not consume 512 MiB by itself.

## Apply CPU and process-count limits

```bash
docker run --rm --cpus=0.5 alpine sh -c 'sleep 300'
docker run --rm --pids-limit=100 alpine sh -c 'sleep 300'
```

- `--cpus=0.5` limits the container to approximately half a CPU's worth of scheduling time.
- `--pids-limit=100` limits the number of processes and threads counted by the PID controller, subject to platform/runtime support.

These examples run for five minutes unless stopped earlier. Use `Ctrl+C` if running them in the foreground, or stop a named container if you change the examples to run in the background.

## Inspect configuration

```bash
docker inspect CONTAINER_NAME
```

Replace `CONTAINER_NAME` with a real container name or ID. Inspect the resource configuration and state.

## Inspect cgroups on a Linux host

```bash
stat -fc %T /sys/fs/cgroup/
cat /proc/self/cgroup
```

On many cgroup v2 Linux systems, the filesystem type is `cgroup2fs`. The following files may expose controller values, but the exact paths depend on the host's cgroup hierarchy and the process's cgroup membership:

```bash
cat /sys/fs/cgroup/cpu.max
cat /sys/fs/cgroup/memory.current
cat /sys/fs/cgroup/memory.max
cat /sys/fs/cgroup/memory.events
```

If a file does not exist or access is denied, inspect the hierarchy and your current cgroup path first. Docker Desktop host inspection differs because the containers run inside a Linux VM.
