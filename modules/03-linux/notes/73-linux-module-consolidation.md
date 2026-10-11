# Lesson 73 — Linux Module Consolidation

## Objectives
- Connect Linux architecture, processes, threads, scheduling, memory, filesystems, permissions, signals, services, and networking.
- Apply a systematic approach to production troubleshooting.
- Distinguish observed evidence from assumptions.

## Concept Summary
Linux applications depend on cooperating kernel and user-space mechanisms. Production debugging means identifying the failing boundary and gathering evidence rather than assuming that one healthy component proves the whole service is healthy.

## Core Ideas
- The kernel manages CPU scheduling, virtual memory, filesystem access, and networking; applications execute in user space.
- A service manager such as systemd supervises lifecycle, while the kernel manages process and thread execution.
- A process can exist while its application is stuck, unhealthy, or unable to serve requests.
- A listening socket does not prove remote reachability or application health.
- CPU contention, memory pressure, storage exhaustion, permissions, signals, and unavailable dependencies can all affect requests.
- Diagnose using the actual service identity and resource or network path involved.
- Restarting can temporarily restore service without fixing the root cause.

## System Mental Model

```text
Client request
      |
      v
Network path and listening socket
      |
      v
Application process and threads
      |
      +--> CPU scheduling
      +--> Virtual memory and RAM
      +--> Filesystems and permissions
      +--> Downstream dependencies
      |
      v
Application response

systemd supervises service lifecycle;
the kernel manages execution and resources.
```

This is a conceptual map, not a literal sequence for every operation. Networking, memory, storage, and scheduling interact through multiple paths.

## Troubleshooting Strategy

```text
Observe symptom
      |
      v
Choose the relevant system boundary
      |
      v
Gather targeted evidence
      |
      v
Update or reject hypotheses
      |
      v
Make one targeted change
      |
      v
Verify the result
```

## Symptom-to-First-Checks Map

| Symptom | Initial investigation |
|---|---|
| Service won't start | `systemctl status`, `journalctl`, executable path, permissions |
| Process exists but requests hang | Thread state, CPU, memory, locks, downstream dependencies |
| Unexpected process termination | Exit status, kernel logs, OOM events, signals, restart history |
| `Permission denied` | Service credentials, ownership, directory traversal, ACLs |
| `No space left on device` | `df -h`, `df -i`, relevant mount and resource limits |
| Local request works, remote request fails | Listener bind address, routes, firewall, network path |
| Slow requests under load | CPU contention, memory pressure, I/O, application and dependency latency |

These are starting points, not guaranteed diagnoses. Confirm the actual resource or failure boundary.

## Practical Commands

```bash
ps -p 1 -o pid,comm,args
uptime
free -h
df -h
df -i
ip addr show
ip route show
sudo ss -lntp
systemctl status SERVICE
journalctl -u SERVICE --since "15 minutes ago"
```

Use an actual service name and inspect commands appropriate to the observed symptom. Prefer read-only inspection before making changes.

## Production Perspective
- A service being active does not prove application health.
- High memory usage alone does not prove a leak; examine pressure, trends, reclaim, and process-level evidence.
- Permission errors should be investigated using the actual service identity and every path component.
- Successful ping does not prove TCP or HTTP reachability.
- Restart policies help recovery but do not replace root-cause analysis, monitoring, or health checks.
- Make targeted changes, verify the result, and avoid broad permission or firewall changes as guesses.

## Common Mistakes
- Treating a running process as proof that requests are being served.
- Assuming a listening port guarantees remote reachability.
- Treating one memory measurement as proof of a leak.
- Using `chmod 777` as a universal permission fix.
- Repeatedly restarting without inspecting logs and dependencies.
- Treating a single successful diagnostic test as proof of overall health.

## Key Takeaways
1. Linux is a collection of cooperating kernel and user-space mechanisms.
2. Different symptoms point toward different system boundaries.
3. Each command answers a limited question; interpret results in context.
4. Troubleshooting is evidence-driven hypothesis testing.
5. Apply targeted fixes and verify them rather than guessing.

## Reflection Questions
1. A service is active, its process exists, and its port is listening. Why might users still receive HTTP 500 errors?
2. An API works locally but remote clients time out. Which boundaries would you investigate?
3. What evidence helps distinguish normal cache usage from harmful memory pressure?
4. Why should you check service credentials and the entire file path before changing permissions?
5. Why is restarting a failing service not a complete root-cause analysis?

## Related Lessons
- Lessons 63–72 — Linux fundamentals
- Next: Lesson 74 — API Fundamentals
