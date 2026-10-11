# Lesson 67 — Memory Management: Commands

```bash
free -h
cat /proc/meminfo
cat /proc/pressure/memory
vmstat 1
ps -eo pid,rss,vsz,%mem,comm --sort=-rss
```

- `free` summarizes memory and cache; available memory is often more informative than the raw free value.
- Memory PSI reports time spent under memory pressure where supported.
- `vmstat` can reveal swapping and reclaim-related activity.
- RSS is resident memory; VSZ is virtual address-space size. High usage alone does not prove a leak.
