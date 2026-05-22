# AgentBox

**AgentBox is an open product idea, MVP specification, and prompt kit for building lightweight multi-agent runtime managers.**

The goal is simple: make it easy to run many isolated, long-running AI agent instances on one personal computer, home server, lab machine, or small team server.

AgentBox is not only a software implementation. It is a reusable product concept that you can implement with your preferred coding agent, stack, branch workflow, and design choices.

Use this repository to:

- understand the AgentBox product idea;
- reuse the MVP requirements and safety rules;
- feed the prompts to Codex, Claude Code, Kimi Code, OpenClaw, or another coding agent;
- fork, remix, or build your own implementation;
- contribute improved specs, prompts, diagrams, or reference implementations.

---

## Why AgentBox?

Personal and team AI agents are becoming useful, but running more than one serious agent is still too manual.

A user may want separate agents for:

- personal assistance;
- coding;
- research;
- operations;
- family use;
- small team support;
- experiments with different frameworks such as Hermes Agent, OpenClaw, Claude Code wrappers, Codex CLI wrappers, or other local/remote agent runtimes.

Each agent should have its own memory, workspace, sessions, configuration, runtime home, login state, and lifecycle.

Users should not need to manually create containers, write startup scripts, copy API keys, separate data directories, or remember which process belongs to which agent.

---

## Repository Positioning

This repository is currently focused on:

```text
open idea + MVP spec + prompt kit + optional reference implementations
```

It intentionally does **not** force one implementation workflow.

You may:

- start from a clean repository;
- start from your own fork;
- use this repo only as a product brief;
- use any branch naming convention;
- use any coding agent;
- use any reasonable implementation stack;
- create your own prompt variants.

The important part is to preserve the AgentBox product intent, MVP boundaries, and safety constraints.

---

## What Should Stay Consistent

An AgentBox-like implementation should keep these principles:

- one machine first;
- many isolated long-running agent instances;
- one owner can have multiple agents;
- one agent belongs to one owner in the MVP;
- each agent has independent runtime home, memory, sessions, workspace, and config;
- platform-level shared model provider/key support, so each end user does not need to manage model credentials;
- container or sandbox based isolation;
- Podman/rootless-first runtime is recommended;
- no Docker Desktop dependency;
- no mounting host home into agent containers;
- no mounting other agents' data into an agent container;
- no mounting Docker or Podman sockets into agent containers;
- no leaking secret values through CLI, API, logs, or UI.

---

## What You Can Change

You are encouraged to remix:

- implementation language;
- web framework;
- database;
- UI design;
- branch workflow;
- prompt style;
- coding agent;
- runtime driver;
- packaging approach;
- deployment model;
- milestone ordering, as long as the MVP intent stays coherent.

The suggested implementation stack is only a recommendation:

- backend: Python + FastAPI;
- CLI: Typer;
- database: SQLite;
- frontend: React + Vite + TypeScript;
- runtime: Podman/rootless Podman.

Alternative stacks are welcome.

---

## Suggested Repository Map

```text
docs/
  vision.md                  # product idea and problem framing
  mvp-spec.md                # required MVP behavior
  architecture-principles.md # runtime and isolation model
  safety-rules.md            # non-negotiable safety constraints
  acceptance-demo.md         # demo checklist for useful implementations

prompts/
  00-build-from-scratch.md
  01-core-crud.md
  02-podman-runtime.md
  03-hermes-runtime.md
  04-lifecycle-backup.md
  05-web-console.md
  variants/
    minimal.md
    codex.md
    claude-code.md
    kimi-code.md
```

---

## Suggested Milestones

These milestones are guidance, not a required branch plan.

1. **Product spec and prompt kit**
   - clarify the idea, MVP, safety rules, and acceptance demo;
   - create reusable prompts for coding agents.

2. **Core domain and CRUD**
   - owners;
   - agents;
   - platform settings;
   - secret metadata without secret leakage;
   - CLI/API optional.

3. **Podman runtime driver**
   - build/start/stop/restart/remove containers;
   - inspect status;
   - logs;
   - exec/shell;
   - mount validation.

4. **Hermes runtime P0**
   - independent `HERMES_HOME` per agent;
   - generated config and env;
   - shared model key injection;
   - `hermes gateway run` as the long-running command.

5. **Lifecycle management**
   - backup;
   - restore;
   - reset;
   - diagnose;
   - upgrade.

6. **Web console**
   - login;
   - dashboard;
   - owners;
   - agents;
   - logs;
   - settings;
   - backups.

7. **Additional runtimes**
   - OpenClaw;
   - coding-agent wrappers;
   - custom MCP agents;
   - other agent frameworks.

---

## Prompt Kit Quick Start

Pick one prompt from `prompts/` and paste it into your preferred coding agent.

For a new implementation, start with:

```text
prompts/00-build-from-scratch.md
```

For an existing implementation that already has core CRUD, continue with:

```text
prompts/02-podman-runtime.md
```

You can freely edit the prompts before using them.

---

## Non-Goals for the MVP

AgentBox MVP should not start as:

- a SaaS multi-tenant platform;
- a Kubernetes orchestration system;
- an enterprise RBAC/audit suite;
- a marketplace;
- a serverless/Knative wake-up system;
- a replacement gateway for WeChat, Telegram, Feishu, Slack, etc.;
- a tool that requires Docker Desktop;
- a system that exposes host home directories or container sockets to agents.

Those may become future experiments, but they should not dominate the first useful version.

---

## Current Status

This repository has been repositioned as a product idea, MVP specification, and prompt kit.

Earlier implementation code has intentionally been removed from the main branch to keep the project open-ended and agent-friendly.

Future contributors may add reference implementations under a clearly named directory such as:

```text
reference-implementations/python-fastapi/
```

without turning the whole repository back into one fixed implementation.

---

## License

MIT. See [LICENSE](LICENSE) if present. If a generated implementation uses this repository as input, keep the license and attribution appropriate for your project.
