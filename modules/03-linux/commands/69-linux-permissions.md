# Lesson 69 — Linux Permissions: Commands

```bash
whoami
id
ls -l /path/to/file
stat /path/to/file
namei -l /path/to/file
getfacl /path/to/file
```

Common permission-changing commands (use only when authorized):

```bash
chmod MODE /path/to/file
chown USER:GROUP /path/to/file
chgrp GROUP /path/to/file
```

- `id` shows the current shell's user and groups, which may differ from a service's credentials.
- `namei -l` helps inspect permissions on path components; `getfacl` shows ACLs when available.
- Avoid using `chmod 777` as a general fix. Check the actual service identity and required access first.
