# Lesson 63 — Linux Architecture

## Objectives

- Understand why an operating system is needed.
- Distinguish hardware, the Linux kernel, and user space.
- Understand system calls and user/kernel privilege boundaries.
- Connect Linux architecture to production debugging.

## Concept Summary

Linux is the kernel. A Linux distribution combines the kernel with user-space software, system libraries, utilities, and often services to provide a usable operating-system environment.

```text
Applications and utilities (user space)
                 |
            System calls
                 |
          Linux kernel
     /       |       |       \
 Processes  Memory Filesystems Networking
                 |
              Hardware
```

## Core Ideas

- **Kernel:** Privileged core responsible for process management, CPU scheduling, memory management, filesystems, networking, device drivers, and security boundaries.
- **User space:** Where most applications, shells, libraries, and utilities execute with restricted privileges.
- **System calls:** Controlled interfaces through which programs request kernel services, such as reading files, creating processes, or using sockets.
- **User mode vs. kernel mode:** CPU privilege levels that help protect the system. System calls use a controlled transition into the kernel.
- **Root vs. kernel mode:** Root is a highly privileged user identity; a root process still normally executes in user mode.
- **Shell:** A user-space program that interprets commands and launches other programs. It is not the kernel.
- **Linux distribution:** Kernel plus user-space software and tools.

## Example: Reading a File

```text
Application
    -> library function
    -> system call
    -> kernel checks and filesystem
    -> result returned to application
```

A library function is not necessarily identical to a system call; it may perform additional work or invoke multiple system calls.

## Example: Sending Network Data

```text
HTTP server
    -> socket interface
    -> kernel networking subsystem
    -> transport processing
    -> device driver / network interface
    -> network
```

This is a conceptual path. Buffering, protocol choice, and hardware offloads affect the implementation details.

## Commands

- `uname -r` — display the running kernel version.
- `ps -p $$ -o pid,ppid,comm` — inspect the current shell process in common shells.
- `cat /proc/1/status` — inspect status information for process 1 through procfs.
- `lscpu` — display CPU information, if installed.
- `free -h` — display memory statistics, if installed.

`/proc` is a virtual filesystem exposing kernel and process information; its entries are not ordinary disk files.

## Production Perspective

When debugging a slow or unhealthy service, ask whether the process is CPU-bound, waiting for I/O, under memory pressure, blocked by permissions, or encountering network/socket problems. Knowing the user-space/kernel boundary helps narrow the investigation.

## Common Misconceptions

- Linux is not the terminal or shell.
- Not every operation requires a system call; ordinary computation can remain in user mode.
- Root does not mean kernel mode.
- The kernel does much more than operate device drivers.
- A Linux distribution is broader than the Linux kernel.

## Key Takeaways

1. The kernel manages resources and enforces protection boundaries.
2. Applications use system calls to request operating-system services.
3. User space and kernel space are privilege domains, not separate physical machines.
4. Understanding these boundaries provides a foundation for process, memory, filesystem, networking, and production-debugging topics.

## Reflection Questions

1. Why is an operating system needed if a computer already has hardware?
2. How do Linux, the Linux kernel, and a Linux distribution differ?
3. Why do applications use system calls instead of controlling hardware directly?
4. Why is root not the same as kernel mode?
5. What roles do an HTTP server, kernel networking subsystem, and network hardware play when sending a response?

## Related Lessons

- Earlier HTTP lessons: sockets and network protocol layering.
- Next: Lesson 64 — Processes.
