# Lesson 69 — Linux Permissions

## Objectives
- Understand Linux users, groups, ownership, and permission bits.
- Read symbolic permissions and numeric modes.
- Distinguish file permissions from directory permissions.
- Diagnose common permission errors.
- Understand least privilege, ACLs, and special permission bits.

## Concept Summary
Linux enforces access controls using process credentials, filesystem ownership and permissions, and additional security policies. Traditional permissions distinguish the owner, owning group, and others.

## Core Ideas
- Users are represented by UIDs; groups are represented by GIDs. Processes carry user and group credentials.
- `r`, `w`, and `x` mean read, write, and execute for files. For directories, they mean listing names, modifying directory entries, and traversing/searching the directory, respectively.
- `ls -l` displays object type and symbolic permission bits. The first character indicates type; the next nine represent owner, group, and others.
- Numeric permissions add `r=4`, `w=2`, and `x=1` for each category. `755` means `rwxr-xr-x`; `640` means `rw-r-----`.
- `chmod` changes permission bits; `chown` changes ownership; `chgrp` changes the owning group.
- Accessing a path normally requires search/execute permission on each parent directory, not merely read permission on the target file.
- ACLs can grant or restrict access beyond the basic owner/group/other model. Security modules, capabilities, and mount options may also affect access.
- Root has extensive privileges but is not the same as kernel mode. Production services should follow least privilege.
- Special bits include setuid, setgid, and sticky bit; their behavior depends on object type and system policy.

## Access Check Model
```text
Process credentials
        |
        v
Path lookup and directory traversal
        |
        v
Ownership / mode bits / ACLs
        |
        v
Other applicable security policies
        |
        +---- allowed: operation proceeds
        +---- denied: operation fails
```

## Practical Commands
```bash
whoami
id
ls -l /path/to/file
namei -l /path/to/file
stat /path/to/file
chmod 640 file
chown user:group file
getfacl file
```

Use paths you own for experiments. `getfacl` and `namei` may not be installed on every system. Avoid broad recursive permission changes and do not use `chmod 777` as a default fix.

## Production Perspective
- `Permission denied` may result from file mode bits, ownership, missing directory traversal permissions, ACLs, or additional security policies.
- Check the identity of the actual service process rather than assuming it runs as the deploying user.
- Grant services only the access they require; avoid running applications as root by default.
- Diagnose every component of a path before changing permissions.

## Common Mistakes
- Confusing root with kernel mode.
- Assuming readable means writable.
- Ignoring parent-directory permissions.
- Treating `chmod 777` as a safe universal fix.
- Assuming the basic nine permission bits describe every access-control rule.

## Key Takeaways
1. Linux checks access using process credentials and filesystem access controls.
2. Owner, group, and others have separate permission bits.
3. Directory execute permission enables path traversal/search.
4. `chmod`, `chown`, and `chgrp` perform different jobs.
5. Least privilege reduces the impact of bugs and compromise.

## Reflection Questions
1. What access does a group member get from mode `640`?
2. Why can a readable file still be inaccessible through its path?
3. What does mode `750` mean?
4. Why should a backend service avoid running as root by default?

## Related Lessons
- Lesson 63 — Linux Architecture
- Lesson 64 — Processes
- Lesson 68 — File Systems
- Next: Lesson 70 — Linux Signals
