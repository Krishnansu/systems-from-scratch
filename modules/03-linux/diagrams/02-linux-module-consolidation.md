# Diagram 02 — Linux Module Consolidation

## 1. Linux System Mental Model

```text
                     CLIENT
                        |
                        v
              +--------------------+
              | Network and Socket |
              +--------------------+
                        |
                        v
              +--------------------+
              | Application Process|
              |   and Threads      |
              +--------------------+
                 |       |       |
                 v       v       v
              CPU     Memory  Filesystem
            Scheduling  VM    and Access
                 |       |       |
                 +-------+-------+
                         |
                         v
                 Downstream Services
                         |
                         v
                 Application Response

  systemd: supervises service lifecycle
  Kernel: manages execution and system resources
```

This is a conceptual model, not a strict sequence. These mechanisms interact and a request may not use every resource shown.

## 2. Evidence-Driven Troubleshooting

```text
          Observe a symptom
                 |
                 v
       Identify the likely boundary
                 |
                 v
       Gather targeted evidence
                 |
                 v
        Update the hypothesis
           /           \
          v             v
     Evidence fits   Evidence conflicts
          |             |
          v             v
   Targeted change   Investigate another
          |           possible cause
          v
      Verify result
```

Do not treat a symptom as proof of a cause. Each command answers a limited question; combine observations before changing the system.

## 3. Symptoms and First Checks

```text
Service won't start
  -> systemctl status, journalctl, executable path, permissions

Process exists, request hangs
  -> thread state, CPU, memory pressure, locks, dependencies

Process exits unexpectedly
  -> exit status, kernel logs, OOM events, signals, restart history

Permission denied
  -> service identity, ownership, parent-directory traversal, ACLs

No space left on device
  -> df -h, df -i, relevant mount and limits

Local works, remote fails
  -> listening address, routes, firewall, network path

Slow under load
  -> CPU contention, memory pressure, I/O, app and dependency latency
```

These are starting points, not guaranteed diagnoses. Follow the evidence.

## 4. Request Path and Service Lifecycle Are Different

```text
Lifecycle control:
 systemd ---> starts/stops/restarts ---> application process
                                           |
Request handling:                          v
 client ---> network ---> socket ---> application threads
                                           |
                                           v
                                      response
```

A service manager reporting an active service does not prove the application is healthy or that requests succeed. Likewise, a listening socket does not prove remote reachability.

## Quick Recall

- Process exists != application is healthy.
- Listener exists != remote clients can reach it.
- High memory use != memory leak.
- Restart succeeds != root cause is fixed.
- Diagnose the relevant boundary, then verify the result.
