# Lesson 71 — Linux Services: Commands

```bash
systemctl status SERVICE
systemctl list-units --type=service --state=running
systemctl list-unit-files --type=service
journalctl -u SERVICE --since "15 minutes ago"
journalctl -u SERVICE -b
journalctl -u SERVICE -f
ps -p 1 -o pid,comm,args
```

- Replace `SERVICE` with the actual unit name; for example, SSH may be called `ssh` or `sshd`.
- `status` and `journalctl` help inspect service state and logs.
- `start`, `stop`, `restart`, `reload`, `enable`, and `disable` change service state or configuration. Understand the impact before using them.
