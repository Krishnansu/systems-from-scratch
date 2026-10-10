# Lesson 64 — Processes

## Objectives
- Distinguish programs from processes.
- Understand process creation, execution, scheduling, and lifecycle.
- Inspect process state and resources on Linux.
- Apply process-level evidence to production debugging.

## Concept Summary
A process is an executing instance of a program with operating-system-managed identity, execution state, virtual address space, and resources. A process can contain multiple threads.

## Core Ideas
- PID identifies a process within a PID namespace; PPID identifies its parent.
- `fork()` creates a child process; `execve()` replaces the calling process's program image.
- Linux schedules runnable threads onto CPU cores and performs context switches.
- Common `ps` state indicators: `R` running/runnable, `S` interruptible sleep, `D` uninterruptible sleep, `T` stopped/traced, `Z` zombie.
- A zombie has exited but has not yet been reaped by its parent.
- Processes usually have separate virtual address spaces, while physical memory pages can be shared.
- File descriptors provide access to files, sockets, pipes, and other resources.
- Parent-child relationships do not guarantee that killing a parent kills every descendant.

## ASCII Diagram
```text
Shell process
    |
    | fork() or related creation
    v
Child process
    |
    | execve()
    v
New program image
    |
    v
Runnable <-> Running <-> Waiting
    |
    v
Exit -> Reaped
```

## Practical Commands
```bash
echo $$
ps -p $$ -o pid,ppid,stat,comm
ps -C sleep -o pid,ppid,stat,etime,comm
ps -eo pid,ppid,stat,comm --forest
ps -eo pid,ppid,stat,%cpu,%mem,comm --sort=-%cpu | head
cat /proc/<PID>/status
ls -l /proc/<PID>/fd
```
Replace `<PID>` with a real numeric PID. Commands and output may vary across environments.

## Production Perspective
- High CPU can indicate computation, excessive work, or a tight loop.
- Low CPU may indicate waiting on I/O, locks, connections, or incoming work.
- Growing memory, many file descriptors, zombie accumulation, and repeated restarts each require different investigations.
- Treat process metrics as clues; correlate them with application logs, thread state, I/O, sockets, and service-manager evidence.

## Common Mistakes
- Equating a process with its executable file.
- Assuming each process owns unique physical RAM.
- Assuming one process has only one thread.
- Treating sleeping processes as inherently unhealthy.
- Confusing zombies with processes still executing.
- Assuming parent termination automatically kills all descendants.

## Key Takeaways
1. A process is an execution context managed by the OS.
2. Process creation and program replacement are different operations.
3. Linux schedules runnable threads and tracks process state and resources.
4. Process state and resource inspection support systematic production debugging.

## Reflection Questions
1. Why are ordinary variables isolated between processes?
2. Why does `execve()` usually preserve the PID?
3. How does a sleeping process differ from a zombie?
4. Why is virtual memory size different from physical RAM usage?
5. What evidence distinguishes CPU saturation from I/O waiting?

## Related Lessons
- Lesson 63 — Linux Architecture
- Next: Lesson 65 — Threads
