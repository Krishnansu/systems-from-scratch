# Lesson 65 — Threads: Commands

```bash
ps -L -p PID -o pid,tid,stat,pcpu,comm
ps -T -p PID
cat /proc/PID/status
```

- `ps -L` and `ps -T` help inspect threads belonging to a process.
- Compare thread states and CPU use; one snapshot may miss short-lived activity.
- Thread state alone does not identify the exact cause of a hang. Use application diagnostics and appropriate tracing when needed.
