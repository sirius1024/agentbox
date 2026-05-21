# Initial Implementation Prompt for Codex / Claude Code / Kimi Code

Use this prompt to start implementing AgentBox from the specification in this repository.

---

You are implementing **AgentBox**, a lightweight multi-agent management platform.

Read these documents first:

1. `docs/spec.md` — full MVP product and technical specification.
2. `docs/implementation-brief.md` — concise implementation handoff.

## Product Goal

Build AgentBox: a lightweight platform that can run many isolated personal AI agent instances on one personal computer, old home server, or team server.

MVP priorities:

- P0 runtime: Hermes Agent
- P1 runtime: OpenClaw
- Podman/rootless Podman only; do **not** depend on Docker Desktop
- one long-running container per Agent
- one Owner can have multiple Agents
- one Agent belongs to exactly one Owner in MVP
- platform-level shared model key so family members/employees do not configure API keys
- backend API + CLI + Web Console

## Required Tech Stack

Use:

- Python + FastAPI for backend
- Typer for CLI
- SQLite for DB
- React + Vite + TypeScript for Web Console
- Podman CLI for container runtime

Do not switch stacks unless there is a strong reason and you document it.

## Core MVP Scope

Implement in milestones. Do not try to build future enterprise features first.

### Milestone 0 — Project Skeleton

Create a clean repo structure with:

```text
agentbox/
  agentbox/
    api/
    cli/
    core/
    db/
    models/
    runtime/
    services/
  runtimes/
    hermes/
      Containerfile
    openclaw/
      Containerfile
  web/
  docs/
  tests/
```

Add:

- Python packaging metadata
- FastAPI app entrypoint
- Typer CLI entrypoint
- SQLite initialization
- config path handling using default `~/.agentbox`
- basic unit tests
- README update with dev commands

### Milestone 1 — Domain Model and CRUD

Implement:

- Owner model and CRUD
- Agent model and CRUD
- Platform settings model
- Secret metadata model; do not leak secret values in API responses
- SQLite persistence
- REST API endpoints
- matching CLI commands

### Milestone 2 — Podman Runtime Driver

Implement `PodmanDriver` using Podman CLI:

- detect Podman
- build image
- create container
- start/stop/restart/remove container
- inspect status
- get logs
- exec command
- open shell

Important constraints:

- do not use Docker Desktop
- do not mount host home directory
- do not mount other Agent directories
- do not mount Docker/Podman socket into Agent containers
- prefer rootless Podman where possible

### Milestone 3 — Hermes Runtime P0

Implement Hermes runtime adapter:

- create per-agent directory under `~/.agentbox/agents/<agent_id>/`
- create Hermes home under `~/.agentbox/agents/<agent_id>/hermes`
- create workspace under `~/.agentbox/agents/<agent_id>/workspace`
- generate Hermes `config.yaml`
- generate Hermes `.env`
- inject platform default model provider/model/API key
- build local image `agentbox/hermes-runtime:<version>` from `runtimes/hermes/Containerfile`
- start container with:
  - `HERMES_HOME=/agent/home`
  - `HOME=/agent`
  - working directory `/agent/workspace`
  - default command `hermes gateway run`
- expose `agentbox agent shell <agent_id>` so admin can run `hermes gateway setup` manually

### Milestone 4 — Lifecycle and Management

Implement:

- start
- stop
- restart
- status
- logs
- shell
- exec
- backup
- restore
- reset
- diagnose
- upgrade

Backup must package agent metadata, runtime home, and workspace into `.tar.gz`.
Restore must stop the agent and create a safety backup before overwriting data.
Upgrade must backup first, recreate the container with the new image, then health check.

### Milestone 5 — Web Console

Implement a minimal Web Console:

- Login page using single admin token
- Dashboard
- Owners list/detail
- Agents list/detail
- Logs view
- Backups view
- Settings page

Web UI can be functional and simple. Do not spend effort on enterprise dashboards or marketplace features.

### Milestone 6 — Cross-platform Service Commands

Implement command interface:

```bash
agentbox service install
agentbox service start
agentbox service stop
agentbox service status
agentbox service uninstall
```

Support:

- Linux systemd
- macOS launchd
- Windows Service

If a platform implementation is incomplete, return a clear unsupported/not-yet-implemented error.

### Milestone 7 — OpenClaw P1

Implement a basic OpenClaw runtime adapter with:

- independent data directory
- local Containerfile
- build/start/stop/restart/status/logs/shell/exec/backup/restore

Do not build deep OpenClaw-specific setup UI in the first pass.

## Acceptance Demo

The first useful demo should prove:

1. `agentbox init`
2. configure platform model provider/key once
3. create Owner `family-member-1`
4. create Hermes Agent `family-hermes`
5. build Hermes runtime image
6. start `family-hermes` as Podman container
7. verify container has independent `HERMES_HOME`
8. verify host home and other Agent directories are not mounted
9. view status/logs from CLI and Web
10. enter shell and run `hermes gateway setup`
11. backup and restore the Agent
12. create a second Owner/Agent and verify isolation

## Non-Goals

Do not implement in MVP:

- Docker Desktop dependency
- Knative/serverless/on-demand wakeup
- AgentBox custom WeChat/Feishu gateway
- enterprise RBAC/audit
- shared Agents
- fine-grained tool/network/file policies
- MicroVM/Kubernetes runtimes
- SaaS multi-tenancy

## Engineering Rules

- Follow `docs/spec.md` as the source of truth.
- Keep implementation incremental and testable.
- Add tests for service logic and runtime command generation.
- Do not hardcode absolute user paths except via config defaults.
- Do not print secret values in logs, API responses, or test fixtures.
- Prefer clear adapter interfaces so future runtimes can be added.
- If a requirement is ambiguous, add a short note in `docs/implementation-notes.md` and choose the simplest MVP behavior.

Start with Milestone 0 and Milestone 1. Commit after each coherent milestone.
