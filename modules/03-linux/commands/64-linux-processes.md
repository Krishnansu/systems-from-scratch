# Lesson 64 — Processes: Commands

```bash
ps -ef
ps -p PID -o pid,ppid,stat,%cpu,%mem,comm,args
pstree -p
cat /proc/PID/status
ls -l /proc/PID/fd
```

- `ps` shows process identity, parent, state, and resource snapshots.
- `/proc/PID/status` exposes process status; `/proc/PID/fd` lists file-descriptor links.
- Replace `PID` with a real process ID. Process states and available fields vary by system.
