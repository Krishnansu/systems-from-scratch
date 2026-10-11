# Lesson 70 — Linux Signals: Commands

```bash
sleep 300 &
echo $!
kill -TERM PID
kill -STOP PID
kill -CONT PID
kill -KILL PID
```

- In this exercise, capture the PID printed by `echo $!` and substitute it for `PID`.
- `TERM` requests termination; `STOP` suspends; `CONT` resumes; `KILL` forcefully terminates.
- `kill` sends a signal; it does not always mean immediate termination.
- Use a disposable test process. Do not signal production processes without authorization.
