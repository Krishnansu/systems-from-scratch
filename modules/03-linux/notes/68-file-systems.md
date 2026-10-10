# Lesson 68 — File Systems

## Objectives
- Explain why file systems are needed to organize storage.
- Understand files, directories, inodes, paths, and file descriptors.
- Trace how Linux opens and reads a file.
- Understand VFS, the page cache, and mount points.
- Inspect filesystems and investigate common storage problems.

## Concept Summary
A file system organizes storage into named objects, directories, metadata, and data blocks. Linux provides common filesystem interfaces through the Virtual File System (VFS), while concrete filesystem implementations manage their own formats and storage behavior.

## Core Ideas
- A path such as `/var/log/app.log` identifies an object through the directory hierarchy.
- Directory entries associate names with filesystem objects. On typical Unix-style filesystems, an inode stores metadata and information used to locate data, not the filename itself.
- Hard links are multiple names for the same underlying file; symbolic links are separate objects containing a path to follow.
- A file descriptor is a small process-level integer referring to an open file description. File descriptors also represent sockets, pipes, and other I/O objects.
- Linux's VFS provides common operations across supported filesystem implementations such as ext4 and XFS.
- File reads may be served from the page cache or require storage I/O. This connects filesystem performance to memory management.
- A mount point makes a filesystem accessible within Linux's unified directory tree.
- Filesystem capacity can be limited by data blocks or inodes. Different mount points can have independent capacity constraints.

## ASCII Diagram
```text
Application: open("/var/log/app.log")
              |
              v
        System call / VFS
              |
              v
       Path lookup and access checks
              |
              v
      Filesystem implementation
              |
              v
       Page cache or storage I/O
              |
              v
       File descriptor returned
```

## Practical Commands
```bash
pwd
ls -la
ls -li
stat .
lsblk
findmnt
 df -h
df -i
```

For storage usage and open descriptors:
```bash
du -xhd1 /data 2>/dev/null | sort -h
ls -l /proc/<PID>/fd
```
Replace `<PID>` with a numeric process ID. Command availability and output vary by environment; `du` options may differ across Linux distributions.

## Production Perspective
- `No space left on device` can indicate exhausted data blocks or inodes.
- `Permission denied` may indicate that the process lacks required access; investigate permissions and path traversal.
- Check `findmnt` and `df -h` for the specific path instead of assuming all paths share the same filesystem.
- Slow file access may involve storage latency, cache misses, or I/O contention. Correlate filesystem metrics with application latency before concluding.

## Common Mistakes
- Assuming the filename is stored in the inode.
- Confusing file descriptors with inode numbers.
- Assuming every file read requires physical disk I/O.
- Assuming deleting one name always immediately frees the underlying data.
- Assuming the root filesystem and every mounted filesystem share free space.
- Assuming a full filesystem must have exhausted bytes rather than inodes.

## Key Takeaways
1. A file system organizes data, names, metadata, and free space on storage.
2. Directory entries connect names to filesystem objects; inodes represent objects on typical Unix-style filesystems.
3. File descriptors let processes access open files and other I/O resources.
4. VFS provides common interfaces across filesystem implementations.
5. The page cache links file access to memory management and storage performance.
6. Mount points and inode capacity matter when diagnosing production storage failures.

## Reflection Questions
1. Why does Linux need a file system instead of letting applications manage raw storage blocks?
2. How can two filenames refer to the same underlying file?
3. What is the difference between an inode and a file descriptor?
4. Why might reading the same file twice be faster the second time?
5. How can `/` have free space while `/data` is full?

## Related Lessons
- Lesson 63 — Linux Architecture
- Lesson 64 — Processes
- Lesson 65 — Threads
- Lesson 66 — CPU Scheduling
- Lesson 67 — Memory Management
- Next: Lesson 69 — Linux Permissions
