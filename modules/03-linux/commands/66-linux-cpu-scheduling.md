# Lesson 66 — CPU Scheduling: Commands

```bash
uptime
top
ps -eo pid,tid,stat,ni,pri,psr,pcpu,comm --sort=-pcpu
vmstat 1
```

- `uptime` reports load averages and uptime; load average is not identical to CPU utilization.
- `top` and `ps` provide snapshots of CPU use and task state.
- `vmstat 1` samples system activity once per second; stop it with Ctrl+C.
- High CPU usage alone does not prove a scheduler problem.
