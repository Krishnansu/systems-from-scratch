# Lesson 63 — Linux Architecture: Commands

```bash
uname -a
cat /etc/os-release
uname -r
ps -p 1 -o pid,comm,args
ls /proc
cat /proc/cpuinfo
cat /proc/meminfo
```

- `uname` reports kernel/system information; `/etc/os-release` identifies the distribution.
- `/proc` exposes kernel-maintained process and system information.
- These commands inspect the system; they do not by themselves prove application health.
