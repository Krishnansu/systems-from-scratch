# Lesson 66 — CPU Scheduling

## Objectives
- Understand how the OS selects runnable tasks for CPU time.
- Distinguish running, runnable, and waiting states.
- Explain preemption, time slices, and context switches.
- Recognize common scheduling algorithms and Linux scheduling policies.
- Diagnose CPU contention using Linux tools.

## Concept Summary
CPU scheduling determines which runnable thread gets CPU time. A scheduler balances fairness, responsiveness, throughput, and policy requirements.

## Core Ideas
- **Running:** currently executing on a CPU core.
- **Runnable:** eligible to run but waiting for CPU time.
- **Waiting/blocked:** unable to run until an event occurs, such as I/O completion or lock availability.
- **Preemption:** the scheduler can interrupt a running task and give CPU time to another task.
- **Context switch:** saves one task's execution state and restores another's. It has overhead but enables multitasking.
- **Time quantum:** maximum time slice before a scheduling decision in time-sliced algorithms such as Round Robin.
- **FCFS:** serves tasks in arrival order; a long task can delay interactive work.
- **SJF/SRTF:** prefer the shortest expected CPU burst or remaining time; long tasks may starve.
- **Round Robin:** rotates runnable tasks through time slices, improving responsiveness under contention.
- **Priority scheduling:** favors higher-priority tasks; aging can help prevent starvation.
- **MLFQ:** adjusts priority across queues based on observed task behavior.
- **EDF:** prioritizes the earliest deadline, often in real-time systems.

## ASCII Diagram
```text
              runnable
                  |
                  v
             +---------+
             | Running |
             +---------+
               |     |
     preempted |     | waits for I/O/event
               v     v
           Runnable  Waiting
               ^       |
               |_______|
             event completes
```

## Linux Scheduling
- Linux schedules kernel-visible tasks, which includes individual threads.
- Ordinary tasks use Linux's fair-scheduling class; modern Linux scheduling is evolving from CFS toward EEVDF.
- `SCHED_FIFO` and `SCHED_RR` are real-time scheduling policies.
- `SCHED_DEADLINE` supports deadline-oriented scheduling.
- Plain Round Robin is a classic algorithm; it is not the general policy used for all ordinary Linux tasks.

## Practical Commands
```bash
ps -eo pid,tid,psr,stat,ni,pri,%cpu,comm --sort=-%cpu | head -20
top
```
In `top`, press `1` to show per-core CPU usage and `q` to exit. For a controlled CPU-bound experiment, run `python3 -c "while True: pass"` and stop it with Ctrl+C.

## Production Perspective
- High CPU utilization with many runnable tasks may indicate CPU contention.
- Low CPU utilization does not rule out latency caused by I/O, locks, or other waiting.
- Load average reflects runnable work and certain uninterruptible tasks; it is not simply CPU utilization.
- Correlate CPU metrics with per-thread activity, latency, I/O, and application-level evidence.

## Common Mistakes
- Assuming a blocked task is actively using CPU.
- Treating load average as another name for CPU utilization.
- Assuming Round Robin is the scheduler used for every Linux task.
- Assuming a higher priority is always better.
- Ignoring the number of runnable tasks when reasoning about scheduling delay.

## Key Takeaways
1. The scheduler selects among runnable tasks; waiting tasks are not eligible until their wait condition clears.
2. Preemption and time slicing let the OS share CPU time among tasks.
3. Scheduling policies trade off fairness, responsiveness, throughput, and deadlines.
4. Linux has different scheduling classes and policies for different requirements.
5. Production diagnosis must distinguish CPU contention from waiting on other resources.

## Reflection Questions
1. Why can FCFS create poor interactive responsiveness?
2. How does Round Robin improve responsiveness, and what affects its overhead?
3. What is the difference between a runnable task and a waiting task?
4. Why does a high load average not necessarily mean CPU usage is high?
5. Why does Linux need scheduling policies beyond a simple Round Robin algorithm?

## Related Lessons
- Lesson 63 — Linux Architecture
- Lesson 64 — Processes
- Lesson 65 — Threads
- Next: Lesson 67 — Memory Management
