# Lesson 73 — Linux Module Consolidation: Commands

## Quick System Snapshot

```bash
uptime
ps -eo pid,ppid,stat,%cpu,%mem,comm,args
top
free -h
cat /proc/pressure/memory
df -h
df -i
```

## Process and Thread Inspection

```bash
ps -p PID -o pid,ppid,stat,%cpu,%mem,comm,args
ps -L -p PID -o pid,tid,stat,pcpu,comm
```

## Network and Service Inspection

```bash
ip addr show
ip route show
sudo ss -lntp
systemctl status SERVICE
journalctl -u SERVICE --since "15 minutes ago"
curl -v --connect-timeout 3 http://HOST:PORT/
```

## Filesystem and Permission Inspection

```bash
findmnt
df -h
df -i
id
namei -l /path/to/file
stat /path/to/file
```

## Diagnostic Reminder

1. State the observed symptom.
2. Choose the likely system boundary.
3. Gather targeted, preferably read-only evidence.
4. Update the hypothesis before making a change.
5. Verify the outcome after any authorized change.

Replace `PID`, `SERVICE`, `HOST`, `PORT`, and paths with actual values. These commands provide evidence, not guaranteed diagnoses. An active service or listening socket does not prove end-to-end application health.
