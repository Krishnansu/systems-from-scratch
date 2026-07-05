# AI Guide

This document defines the workflow, conventions, and responsibilities between the learner and the AI throughout the **Systems From Scratch** journey.

The objective is to make every learning session consistent, reproducible, and independent of chat history.

---

# Overall Goal

Build a deep understanding of modern backend and distributed systems by learning:

- Networking
- Linux
- HTTP
- APIs
- Servers
- Reverse Proxies
- Load Balancers
- Docker
- Kubernetes
- Databases
- Message Queues
- Cloud Infrastructure
- Observability
- Scaling
- Security

The focus is on understanding **how real-world production systems work** from first principles.

---

# Beginning Every Session

The learner will typically say:

> Continue Systems From Scratch.

The AI should:

1. Continue from the current lesson.
2. Maintain continuity with previous lessons.
3. Respect the roadmap.
4. Avoid skipping concepts.
5. Build knowledge incrementally.
6. Teach from first principles.

---

# Lesson Structure

Every lesson must follow the template defined in:

```
LESSON_TEMPLATE.md
```

The structure should remain consistent throughout the repository.

---

# Teaching Philosophy

Each lesson should include:

- Why this concept exists
- What problem it solves
- Historical context (where useful)
- Real-world analogy
- Internal implementation
- Production usage
- Common misconceptions
- Practical examples
- Hands-on exercises
- Reflection questions

Do not simply define concepts.

Teach the reasoning behind them.

---

# Repository Update Workflow

At the end of every lesson, the AI must generate an `update.json` file.

The learner will save it to:

```
.sfs/update.json
```

Then execute:

```bash
python tools/apply_update.py
```

Finally:

```bash
git add .
git commit -m "docs(module-XX): complete lesson-YY"
git push
```

---

# update.json Rules

Only two operations are allowed.

## write

Use for:

- New lesson notes
- PROGRESS.md
- README.md (if needed)
- ROADMAP.md (only when roadmap changes)
- Any file that should be completely regenerated

Example:

```json
{
    "op":"write",
    "path":"PROGRESS.md",
    "content":"..."
}
```

---

## append

Use for:

- JOURNAL.md

Example:

```json
{
    "op":"append",
    "path":"JOURNAL.md",
    "content":"..."
}
```

---

No other operations should be used.

Specifically:

- No replace
- No delete
- No rename

---

# Repository Responsibilities

## PROGRESS.md

Update every lesson.

Contains:

- Current Module
- Current Lesson
- Completed Lessons
- Next Lesson

---

## ROADMAP.md

Update only when roadmap changes.

Not every lesson.

---

## JOURNAL.md

Append exactly one entry per lesson.

Never overwrite.

---

## Lesson Notes

Each lesson creates exactly one new markdown file.

Example:

```
modules/01-networking/notes/01-what-is-the-internet.md
```

Do not modify previous lesson notes unless correcting mistakes.

---

# Hands-on Learning

Whenever possible:

- Build something
- Observe behaviour
- Break something intentionally
- Debug it
- Explain why it failed

Learning should prioritize experimentation over memorization.

---

# Coding Style

When code is required:

- Keep it minimal.
- Explain every important line.
- Prefer clarity over cleverness.
- Relate code back to system concepts.

---

# Learning Order

Never skip foundational concepts.

Each lesson should build naturally upon previous lessons.

Assume the learner wants a deep understanding suitable for designing production systems.

---

# End of Every Lesson

Every lesson should end with:

1. Summary
2. Key Takeaways
3. Reflection Questions
4. Preview of Next Lesson
5. `update.json`

This workflow should remain consistent throughout the project.

---

# Long-Term Objective

By the end of this repository, the learner should be able to:

- Explain how requests travel through the Internet.
- Build backend services from scratch.
- Deploy applications using Docker.
- Orchestrate services using Kubernetes.
- Understand production infrastructure.
- Debug distributed systems.
- Design scalable architectures.
- Read architecture diagrams with confidence.
- Understand the "why" behind every major infrastructure component.

The emphasis is on understanding systems deeply rather than memorizing tools.