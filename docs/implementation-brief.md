# AgentBox Implementation Brief

This is a concise handoff brief for implementing AgentBox with Codex, Claude Code, or Kimi Code. The full specification is in `docs/spec.md`.

## Goal

Build **AgentBox**, a lightweight multi-agent management platform that runs multiple isolated Hermes Agent / OpenClaw instances on one personal computer, family server, or team server.

MVP focus:

- P0: Hermes Agent runtime
- P1: OpenClaw runtime
- Podman/rootless Podman, not Docker Desktop
- one long-running container per agent
- one owner can have multiple agents
- one agent belongs to exactly one owner
- platform-level shared model key
- backend API + CLI + Web Console

## Stack

- Python + FastAPI backend
- Typer CLI
- SQLite database
- React + Vite + TypeScript frontend
- Podman CLI runtime driver
- Default data dir: `~/.agentbox`

## Core Objects

- Owner: human/role served by agents
- Agent: one long-running isolated instance
- Runtime: Hermes/OpenClaw adapter
- Platform Settings: global config/model/runtime settings
- Secrets: platform-level and agent-level secret references

## MVP Capabilities

### Owner

- create/list/show/update/delete owners

### Agent

- create/list/show/delete
- start/stop/restart/status
- logs
- shell/exec
- backup/restore/reset
- diagnose
- upgrade

### Hermes Runtime

- create independent `HERMES_HOME`
- generate `config.yaml` and `.env`
- inject platform default model provider/key
- build local `agentbox/hermes-runtime:<version>` image from Containerfile
- run default command: `hermes gateway run`
- expose shell so admin can run `hermes gateway setup` manually in MVP

### Isolation

Each agent container mounts only:

```text
~/.agentbox/agents/<agent_id>/<runtime-home> -> /agent/home
~/.agentbox/agents/<agent_id>/workspace      -> /agent/workspace
```

Do not mount host home, other agent directories, Docker/Podman socket, or host root.

### Authentication

- single-admin token
- API requires bearer token
- Web Console login required
- CLI reads local token

### Service

Support service commands for:

- Linux systemd
- macOS launchd
- Windows Service

If incomplete on a platform, return clear unsupported error.

## Suggested Milestones

1. Project skeleton: FastAPI, Typer, SQLite, config paths, tests.
2. Owner/settings/secrets metadata CRUD.
3. Podman runtime driver: build/run/stop/logs/inspect/exec.
4. Hermes runtime P0: image, directory creation, config generation, container lifecycle.
5. Backup/restore/reset/diagnose.
6. Web Console: login/dashboard/owners/agents/settings/logs.
7. Cross-platform service wrappers.
8. OpenClaw P1 adapter.

## Acceptance Tests

Minimum working demo:

1. `agentbox init`
2. configure model provider/key once
3. create owner `family-member-1`
4. create Hermes agent `family-hermes`
5. build Hermes runtime image
6. start `family-hermes` as Podman container
7. verify container has independent `HERMES_HOME`
8. verify host home and other agent dirs are not mounted
9. view status/logs from CLI and Web
10. enter shell and run `hermes gateway setup`
11. backup and restore the agent
12. create second owner/agent and verify isolation

## Non-Goals

Do not implement in MVP:

- Docker Desktop dependency
- Knative/serverless/on-demand wakeup
- AgentBox custom WeChat/Feishu gateway
- enterprise RBAC/audit
- shared agents
- fine-grained tool/network/file policies
- MicroVM/Kubernetes runtimes
- SaaS multi-tenancy
