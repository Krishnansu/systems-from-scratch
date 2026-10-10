# Lesson 71 — Linux Services

## Objectives
- Explain services, processes, and service managers.
- Understand `systemd` units, lifecycle states, dependencies, and restart policies.
- Inspect service status and logs with `systemctl` and `journalctl`.
- Connect service management to graceful shutdown and production operations.

## Concept Summary
A service is an operational unit managed for ongoing system functionality. On many modern Linux distributions, `systemd` manages service startup, shutdown, dependencies, restart policies, and status. The kernel still manages process execution and CPU scheduling.

## Core Ideas
- A service is not necessarily identical to one process; it can manage related processes or represent other resources.
- `systemctl start` starts a unit now; `systemctl enable` configures it for activation through boot targets. They are distinct operations.
- Common states include `active (running)`, `active (exited)`, `inactive`, `failed`, `activating`, and `deactivating`.
- `active (running)` does not guarantee application health.
- Unit files define settings such as `ExecStart`, `User`, `WorkingDirectory`, restart policy, dependencies, and installation targets.
- `After=` specifies ordering; it does not by itself guarantee that a dependency is ready or reachable.
- `Restart=on-failure` can restart a service after qualifying failures, subject to configuration and restart limits.
- `systemd` may request graceful shutdown using `SIGTERM` and force termination after a timeout, depending on configuration.
- Graceful application shutdown should stop accepting work, drain or cancel in-flight requests, close resources, and exit within a bounded time.

## Lifecycle Model
```text
Boot or administrator request
          |
          v
   systemd reads unit
          |
          v
Checks dependencies and starts process
          |
          v
Tracks service lifecycle
          |
          +---- exits normally
          +---- fails; restart policy may apply
          +---- receives stop request and shuts down
```

## Practical Commands
```bash
ps -p 1 -o pid,comm,args
systemctl status ssh
systemctl list-units --type=service --state=running
systemctl list-unit-files --type=service
journalctl -u ssh -b
journalctl -u ssh --since "1 hour ago"
journalctl -u ssh -f
```

The service may be named `sshd` instead of `ssh`, and permissions may be needed to read logs. Use start/stop/restart only when authorized and when the service impact is understood.

## Production Perspective
- Services should run with least-privilege OS credentials.
- Restart policies improve recovery but do not replace health checks, alerting, or root-cause analysis.
- Inspect status, logs, executable paths, working directory, permissions, and dependencies when startup fails.
- Graceful shutdown is a contract between the service manager and application code.

## Common Mistakes
- Treating a service as exactly one process.
- Confusing `start` with `enable`.
- Assuming `After=network.target` guarantees remote dependency readiness.
- Treating an active process as proof of application health.
- Repeatedly restarting without investigating the cause.

## Key Takeaways
1. A process is a running execution instance; a service is an operational unit that can be managed.
2. `systemd` manages lifecycle, while the kernel schedules processes.
3. Unit configuration controls startup, dependencies, and restart behavior.
4. `systemctl` exposes state; `journalctl` helps explain behavior.
5. Graceful shutdown requires both a manager request and application cooperation.

## Reflection Questions
1. Why can a running service still be unhealthy?
2. How do `start` and `enable` differ?
3. Why is startup ordering not the same as dependency readiness?
4. How does `SIGTERM` fit into service shutdown?
5. What would you inspect before changing a restart policy?

## Related Lessons
- Lesson 64 — Processes
- Lesson 65 — Threads
- Lesson 69 — Linux Permissions
- Lesson 70 — Linux Signals
- Next: Lesson 72 — Linux Networking Tools
