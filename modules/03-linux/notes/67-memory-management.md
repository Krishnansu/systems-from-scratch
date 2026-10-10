# Lesson 67 — Memory Management

## Objectives
- Distinguish virtual memory from physical RAM.
- Understand address spaces, pages, frames, and page tables.
- Explain the MMU, TLB, and page faults.
- Understand demand paging, copy-on-write, memory pressure, and swap.
- Inspect Linux process memory for production debugging.

## Concept Summary
Virtual memory gives processes protected address spaces. Linux and the MMU translate virtual addresses to physical memory, manage page mappings, and enforce access permissions.

## Core Ideas
- Each process has its own virtual address space; threads share much of that space but have separate stacks and execution state.
- A virtual address identifies a location in a process's address space, not necessarily a physical RAM location.
- Virtual memory is divided into pages; physical RAM is divided into page frames.
- Page tables record mappings and permissions. The MMU performs address translation; the TLB caches recent translations.
- A page fault requests OS handling for an access that cannot proceed directly. It may be resolved normally or result in a signal such as `SIGSEGV`.
- Minor page faults can be resolved without storage I/O; major page faults require I/O to bring data into memory.
- Demand paging loads or creates page contents when needed rather than eagerly backing every virtual page with resident RAM.
- Copy-on-write lets processes share pages until a write requires a private copy.
- Linux can reclaim eligible memory and use swap when configured. Heavy swapping can cause severe latency.
- `VmSize` measures virtual size; RSS measures resident memory; PSS apportions shared resident pages; swap metrics describe swapped memory.

## ASCII Diagram
```text
Process virtual address
          |
          v
     Page tables <---- maintained by Linux
          |
          v
         MMU
          |
          v
 Physical RAM frame

Invalid or unavailable mapping
          |
          v
      Page fault
          |
          +---- resolved: retry access
          |
          +---- invalid access: signal, e.g. SIGSEGV
```

## Practical Commands
```bash
free -h
cat /proc/self/status
cat /proc/<PID>/status
cat /proc/<PID>/maps
cat /proc/<PID>/smaps_rollup
```
Replace `<PID>` with a numeric process ID. Some files or fields may require permissions or may not exist in every environment.

## Production Perspective
- Memory pressure can cause reclaim and storage I/O, increasing latency even when CPU utilization is moderate.
- High RSS does not necessarily mean all resident memory is private; shared pages can be counted in multiple processes' RSS.
- Correlate memory metrics, major faults, swap activity, storage latency, and application latency before diagnosing a memory bottleneck.

## Common Mistakes
- Equating virtual memory with swap.
- Assuming every virtual page is resident in RAM.
- Assuming every page fault is a bug.
- Treating virtual size as physical memory usage.
- Assuming processes cannot share physical pages.
- Assuming more swap always solves memory pressure.

## Key Takeaways
1. Virtual addresses are translated to physical addresses through mappings and hardware support.
2. Paging lets virtual pages map to non-contiguous physical frames.
3. Page faults can be normal, expensive, or fatal depending on the access.
4. Copy-on-write avoids unnecessary copying until a write requires it.
5. Memory metrics and swap behavior help explain production latency and resource pressure.

## Reflection Questions
1. How can two processes use the same virtual address but access different physical memory?
2. What is the difference between a virtual page and a physical frame?
3. Why does a page fault not always indicate a bug?
4. How does copy-on-write make `fork()` more efficient?
5. Why can memory pressure increase latency when CPU utilization is moderate?

## Related Lessons
- Lesson 63 — Linux Architecture
- Lesson 64 — Processes
- Lesson 65 — Threads
- Lesson 66 — CPU Scheduling
- Next: Lesson 68 — File Systems
