# AgentBox Implementation Brief

This is a concise handoff for coding agents and human builders.

AgentBox is a lightweight manager for multiple isolated, long-running AI agent instances on one machine.

Use this repository as:

```text
product idea + MVP spec + safety rules + prompt kit
```

not as a rigid branch or implementation mandate.

---

## Product Goal

Make it easy to create, run, monitor, repair, backup, restore, and upgrade dedicated AI agent instances for different owners, roles, or projects.

Each agent should have independent:

- runtime home;
- workspace;
- config;
- memory;
- sessions;
- login state;
- lifecycle.

---

## Recommended Stack

A simple reference implementation may use:

- Python + FastAPI backend;
- Typer CLI;
- SQLite;
- React + Vite + TypeScript frontend;
- Podman/rootless Podman runtime.

This is not mandatory. Other stacks are acceptable if they preserve the product behavior and safety model.

---

## Core MVP Objects

- Owner: human, role, or project served by agents;
- Agent: one isolated long-running runtime instance;
- Runtime: Hermes/OpenClaw/custom runtime adapter;
- Settings: platform defaults;
- Secret: write-only sensitive value with metadata visibility.

---

## Key Safety Constraints

- do not require Docker Desktop;
- do not mount host home;
- do not mount host root;
- do not mount another agent's data;
- do not mount Docker or Podman sockets into agents;
- do not leak secret values;
- use safe command argument arrays instead of shell string concatenation.

---

## Suggested Milestones

1. Spec and prompt kit;
2. core domain and CRUD;
3. Podman runtime driver;
4. Hermes runtime adapter;
5. lifecycle management: backup, restore, reset, diagnose, upgrade;
6. Web console;
7. additional runtimes and variants.

Milestones are guidance. They do not require fixed branch names.

---

## Minimum Useful Demo

A useful implementation should prove:

1. initialize data directory;
2. configure shared model provider/key;
3. create owner;
4. create agent;
5. create isolated runtime/workspace directories;
6. start agent runtime;
7. inspect status/logs;
8. exec/shell into runtime;
9. verify dangerous host mounts are absent;
10. backup and restore;
11. create a second agent and prove isolation.

---

## How to Use the Prompt Kit

Choose a prompt from `prompts/` based on your starting point:

- `00-build-from-scratch.md` for a new implementation;
- `01-core-crud.md` for domain model and CRUD;
- `02-podman-runtime.md` for container lifecycle;
- `03-hermes-runtime.md` for Hermes Agent integration;
- `04-lifecycle-backup.md` for backup/restore/diagnose;
- `05-web-console.md` for UI.

You may edit, shorten, expand, or remix any prompt before use.
