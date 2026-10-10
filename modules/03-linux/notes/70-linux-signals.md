# Lesson 70 — Linux Signals

## Objectives
- Explain signals and their role in process communication.
- Distinguish common signals and their default actions.
- Understand signal handlers, blocked and pending signals, and thread delivery.
- Use signals safely when inspecting processes.

## Concept Summary
A signal is a kernel-managed notification that informs a process or thread of an event. Depending on the signal and its disposition, delivery can invoke a handler, trigger a default action, or be ignored. Delivery may be delayed when blocked.

## Core Ideas
- `SIGTERM` requests termination and can be handled for graceful shutdown.
- `SIGKILL` forces termination and cannot be caught, blocked, or ignored.
- `SIGINT` commonly results from Ctrl+C in a terminal; `SIGSTOP` stops a process and `SIGCONT` resumes it.
- `SIGCHLD` informs a parent about child-process state changes. Parents still need wait-related calls to reap exited children.
- Blocked signals cannot currently be delivered to a thread; pending signals have been generated but not yet delivered.
- Standard signals can coalesce rather than queue every repeated occurrence. Real-time signals have different queueing behavior.
- Process-directed signals may be delivered to an eligible thread; thread-directed signals target a specific thread.
- Signal handlers must avoid unsafe asynchronous operations. A common design is to set a flag and perform cleanup in the main execution path.
- Sending signals is subject to process-identity and permission checks.

## Signal Flow
```text
Event or sender
      |
      v
Kernel validates target and request
      |
      v
Signal becomes pending if delivery is deferred
      |
      v
Signal delivered when permitted
      |
      v
Handler / default action / ignore
```

## Practical Commands
```bash
kill -l
sleep 300 &
PID=$!
ps -p "$PID" -o pid,stat,comm
kill -TERM "$PID"

sleep 300 &
PID=$!
kill -STOP "$PID"
ps -p "$PID" -o pid,stat,comm
kill -CONT "$PID"
kill -TERM "$PID"
```

Run experiments only against processes you own and can safely stop. `kill` sends a signal; it does not always terminate the target.

## Production Perspective
- Service managers often send `SIGTERM` to begin graceful shutdown and may force termination after a deadline.
- Services should stop accepting new work, finish or cancel in-flight work, and release resources within a bounded time.
- `SIGPIPE`, `SIGCHLD`, and termination signals can explain otherwise surprising process behavior.
- Multithreaded programs must deliberately coordinate signal handling.

## Common Mistakes
- Assuming `kill` always sends a termination signal.
- Treating `SIGTERM` as a guarantee of graceful exit.
- Assuming `SIGKILL` can run application cleanup.
- Treating standard signals as a reliable event queue.
- Calling arbitrary library functions from an asynchronous signal handler.

## Key Takeaways
1. Signals provide asynchronous notifications managed by the kernel.
2. `SIGTERM` permits application handling; `SIGKILL` does not.
3. Blocked and pending describe different signal states.
4. Signal handling requires care in multithreaded applications.
5. Graceful shutdown is an application and supervision design concern.

## Reflection Questions
1. Why is `SIGTERM` usually tried before `SIGKILL`?
2. How does a blocked signal differ from a pending signal?
3. Why can standard signals coalesce?
4. What role does `SIGCHLD` play?
5. What might a supervisor do when a process ignores its shutdown deadline?

## Related Lessons
- Lesson 63 — Linux Architecture
- Lesson 64 — Processes
- Lesson 65 — Threads
- Lesson 69 — Linux Permissions
- Next: Lesson 71 — Linux Services
