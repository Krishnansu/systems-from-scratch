# Lesson 101 — cgroups

## Objectives
- Explain how cgroups control and account for resource consumption.
- Distinguish resource control from namespace isolation.
- Understand CPU quota, CPU weight, and memory limits in cgroup v2.

## Concept Summary
Control groups (cgroups) organize processes into groups and measure or constrain their resource usage. Containers commonly use cgroups to prevent one workload from consuming an unfair or excessive share of host resources.

Namespaces isolate views of system resources; cgroups control resource consumption. Neither replaces the other.

## Core Ideas

### Common controllers
- **CPU:** limit CPU bandwidth and distribute CPU time under contention.
- **Memory:** account for memory and enforce limits.
- **PIDs:** limit the number of processes and threads.
- **I/O:** control or account for block-device I/O, depending on the controller and configuration.
- **cpuset:** restrict processes to selected CPUs or memory nodes.

### CPU quota vs. weight
In cgroup v2, `cpu.max` contains a quota and period in microseconds. For example:

```text
50000 100000
```

This permits up to 50 ms of CPU time per 100 ms period, equivalent to half a CPU's capacity over time. A quota is a bandwidth cap. CPU weight instead influences relative CPU sharing when workloads compete; it is not a fixed CPU reservation.

### Memory controls
- `memory.current`: memory currently charged to the cgroup.
- `memory.max`: hard limit on charged memory; `max` means no configured limit at that level.
- `memory.events`: counters for memory-limit and OOM-related events.

Reaching `memory.max` does not necessarily kill every process immediately. The kernel may reclaim memory, an allocation may fail, or an OOM event may terminate a process. A container can hit its own limit even when the host has free RAM.

## Practical Example

```bash
# Inspect the cgroup filesystem type
stat -fc %T /sys/fs/cgroup/

# Inspect the current process's cgroup membership
cat /proc/self/cgroup

# Start a container with a memory limit
 docker run --rm --memory=512m alpine sh -c 'sleep 300'

# Limit CPU bandwidth to approximately half a CPU
 docker run --rm --cpus=0.5 alpine sh -c 'sleep 300'

# Limit process count
 docker run --rm --pids-limit=100 alpine sh -c 'sleep 300'

# Observe running containers' resource usage
 docker stats
```

The examples are illustrative; Docker, kernel, and cgroup configuration affect the exact behavior and available controls. Remove the leading space before `docker` if copying the commands into a shell.

## Production Perspective
- Resource limits improve workload isolation and help protect host stability.
- A memory limit that is too low can cause allocation failures or OOM termination even when host memory remains available.
- CPU quota limits sustained CPU usage; CPU weight matters when workloads contend.
- Monitor resource usage and limit events rather than relying on configured limits alone.

## Common Mistakes
- Assuming namespaces limit CPU or memory consumption.
- Treating CPU weight as a hard cap or reservation.
- Assuming reaching `memory.max` always kills every process in the cgroup.
- Assuming host free memory overrides a container's memory limit.
- Assuming every system uses the same cgroup version or exposes identical controls.

## Key Takeaways
- Namespaces isolate views; cgroups account for and control resource consumption.
- CPU quota limits bandwidth; CPU weight affects relative sharing under contention.
- `memory.current` reports charged usage; `memory.max` sets the limit.
- A container can exhaust its own memory budget while the host still has free RAM.
- Containers rely on multiple kernel mechanisms; cgroups alone are not a complete security boundary.

## Reflection Questions
1. Can a container with its own PID and network namespaces still exhaust host memory if no effective memory limit is set?
2. How does CPU quota differ from CPU weight?
3. Does reaching `memory.max` necessarily kill every process in a cgroup immediately?
4. What do `memory.current` and `memory.max` represent?
5. Why can a container hit its memory limit while the host still has free RAM?

## Related Lessons
- Lesson 98 — Layers
- Lesson 99 — Dockerfile
- Lesson 100 — Namespaces
- Next: Lesson 102 — Volumes
