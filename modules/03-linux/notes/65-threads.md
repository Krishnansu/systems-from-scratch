# Lesson 65 — Threads

## Objectives
- Explain why threads exist and how they differ from processes.
- Identify thread-local state versus shared process resources.
- Understand concurrency, parallelism, and race conditions.
- Inspect threads on Linux and recognize common concurrency hazards.

## Concept Summary
A thread is a schedulable execution path within a process. Threads normally share the process's virtual address space and many resources, while each thread has its own execution state, stack, thread ID, and thread-local data.

## Core Ideas
- Shared resources commonly include heap/global memory, program mappings, and the process's file descriptor table.
- Each thread has its own CPU execution state, stack, scheduling state, and thread-specific data.
- Linux represents threads as kernel-visible tasks and schedules runnable threads onto CPU cores.
- A Linux thread has a TID; threads in a process share a thread-group ID (TGID), commonly represented as the process ID.
- **Concurrency** means tasks can make progress during overlapping periods; **parallelism** means simultaneous execution.
- A race condition occurs when uncontrolled operation ordering affects correctness.
- Mutexes and other synchronization mechanisms protect shared state, but can introduce contention or deadlocks.
- Alternatives include reducing shared mutable state, message passing, and event-driven I/O.

## ASCII Diagram
```text
Process: shared address space and resources
    |
    +-- Thread A: registers, execution state, stack
    |
    +-- Thread B: registers, execution state, stack
    |
    +-- Thread C: registers, execution state, stack
```

## Practical Commands
```bash
ps -T -p <PID> -o pid,spid,stat,comm
ls /proc/<PID>/task
ps -p <PID> -o pid,ppid,nlwp,stat,comm
```
Replace `<PID>` with a real numeric PID. Python's `threading` module can be used to create threads and inspect native thread IDs.

## Production Perspective
Threads can improve throughput and responsiveness, particularly when work waits on I/O or can run in parallel. More threads do not guarantee better performance. Shared-state races, lock contention, deadlocks, excessive thread counts, and blocking an event-loop thread can hurt reliability and throughput.

## Common Mistakes
- Treating threads as fully isolated processes.
- Assuming concurrency always means parallel execution.
- Assuming shared memory removes the need for coordination.
- Assuming more threads always improve performance.
- Believing a lock protects state that is not consistently guarded by its protocol.
- Assuming a thread failure can never affect the entire process.

## Key Takeaways
1. Threads share much of a process's resources but retain independent execution state.
2. Linux schedules threads as tasks.
3. Shared mutable state requires correct coordination.
4. Threading is a trade-off among throughput, responsiveness, complexity, and resource usage.

## Reflection Questions
1. Why does each thread need its own stack?
2. How does concurrency differ from parallelism?
3. How can a race condition lose an update?
4. What are the costs of using a mutex?
5. When might an event loop be preferable to a thread per connection?

## Related Lessons
- Lesson 63 — Linux Architecture
- Lesson 64 — Processes
- Next: Lesson 66 — Scheduling
