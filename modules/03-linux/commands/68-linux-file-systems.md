# Lesson 68 — File Systems: Commands

```bash
lsblk
findmnt
df -h
df -i
du -sh /path/to/directory
stat /path/to/file
ls -li /path/to/file
```

- `lsblk` lists block devices; `findmnt` shows mounted filesystems.
- `df -h` checks filesystem space; `df -i` checks inode availability.
- `du` estimates directory usage; `stat` shows file metadata; `ls -i` displays inode numbers.
- A filesystem can run out of inodes even when it has free data space.
