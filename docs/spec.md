# AgentBox MVP Specification

> Status: Draft for review  
> Owner: Project maintainer  
> Purpose: This document is a spec-driven product and implementation guide for building AgentBox with AI coding tools such as Codex, Claude Code, or Kimi Code.

---

## 1. Product Vision

AgentBox is a lightweight multi-agent management platform for running many isolated personal AI agents on a single personal computer, old home server, team server, or future enterprise server.

The original problem is simple:

> Hermes Agent / OpenClaw are useful, but deploying many independent instances for different people is too hard. Users should not need to manually create containers, manage profiles, separate memory directories, configure model keys repeatedly, or invent strange startup scripts.

AgentBox should make it easy to create and run dedicated agents for different owners:

- Project maintainer的 Hermes Agent
- family member A的 Hermes Agent
- family member B的 Hermes Agent
- 某个员工的 Hermes Agent
- Project maintainer的 OpenClaw / future coding agent

Each agent should have its own memory, sessions, workspace, configuration, login state, and runtime environment. Agents must not pollute each other or the host machine.

AgentBox is not initially a large enterprise orchestration platform. It starts as a practical, lightweight, single-machine multi-agent host, and can later grow into team and enterprise management.

---

## 2. Target Users and Scenarios

### 2.1 Personal user

A technical user wants to run multiple agents for different roles on one laptop or old computer:

- personal assistant
- coding agent
- research agent
- operations agent

### 2.2 Family use

A technical user wants to create agents for family members:

- spouse
- parents
- children

Family members should use the agent through the agent framework's native channels such as WeChat, Feishu, Telegram, or other gateways. They should not need to understand API keys, models, config files, containers, or command lines.

### 2.3 Small team / employee use

A manager wants to give each employee one or more dedicated agents, with background information preloaded and independent memory.

MVP should support the basic structure for this use case, but does not implement complex enterprise RBAC, audit, or shared-agent collaboration.

### 2.4 Future enterprise use

Future versions may support:

- shared team agents
- department agents
- enterprise RBAC
- audit and compliance
- network/tool policies
- multi-node scheduling
- MicroVM / Firecracker / Kata / gVisor stronger isolation
- Kubernetes runtime

---

## 3. Non-Goals for MVP

MVP explicitly does **not** implement:

1. Serverless / Knative / on-demand agent wake-up.
2. A new WeChat / Feishu / Telegram gateway written by AgentBox.
3. Complex multi-agent DAG orchestration.
4. Shared agents or public group agents.
5. Complex enterprise RBAC.
6. Full audit/compliance system.
7. Fine-grained tool permission control.
8. Fine-grained network allowlist/denylist.
9. File ACL editor.
10. MicroVM / Firecracker / Kata / gVisor runtime.
11. Kubernetes runtime.
12. Agent marketplace.
13. SaaS multi-tenant hosting.
14. Docker Desktop dependency.

MVP must stay focused: create, run, isolate, monitor, repair, backup, restore, and upgrade multiple long-running Hermes/OpenClaw instances on one machine.

---

## 4. Product Name and Technical Stack

### 4.1 Product name

- Product name: `AgentBox`
- CLI command: `agentbox`
- Default data directory: `~/.agentbox`

### 4.2 Recommended implementation stack

MVP should use common, AI-coding-friendly technologies:

- Backend: Python + FastAPI
- CLI: Typer
- Database: SQLite
- Frontend: React + Vite + TypeScript
- UI: Tailwind CSS or shadcn/ui
- Runtime driver: Podman CLI
- Container runtime: Podman / rootless Podman preferred

The backend, CLI, and web console should all use the same domain model and service layer.

---

## 5. Core Domain Model

### 5.1 Owner

`Owner` is a first-class object. An owner represents the human or role that an agent serves.

Examples:

- `primary-user`
- `family-member-1`
- `family-member-2`
- `employee-zhangsan`

MVP rules:

- One owner may have multiple agents.
- An owner has a display name.
- Owner can store optional notes/background text.
- Owner does not need to log in to AgentBox in MVP.
- MVP has only one admin user for the platform.

Suggested fields:

```yaml
Owner:
  id: string
  name: string
  display_name: string
  description: string | null
  created_at: datetime
  updated_at: datetime
```

### 5.2 Agent Runtime Type

Runtime type describes which agent framework is being managed.

MVP priorities:

- P0: `hermes`
- P1: `openclaw`

Future runtime types may include Claude Code, Kimi Code, Codex CLI, browser agents, office agents, or custom MCP agents.

Suggested fields:

```yaml
RuntimeType:
  name: hermes | openclaw | custom
  display_name: string
  priority: P0 | P1 | P2
  image_name: string
  default_command: string[]
```

### 5.3 Agent Instance

An agent instance is a long-running dedicated runtime environment owned by exactly one owner.

MVP rules:

- An agent belongs to exactly one owner.
- An owner may have many agents.
- An agent is not shared by multiple owners in MVP.
- Agent runs as a long-running container.
- Agent has its own data directory.
- Agent has its own memory, sessions, config, workspace, and login state.

Suggested fields:

```yaml
Agent:
  id: string
  name: string
  display_name: string
  owner_id: string
  runtime_type: hermes | openclaw
  status: created | starting | running | unhealthy | restarting | stopping | stopped | failed | deleted
  container_name: string
  image: string
  data_dir: string
  cpu_limit: string
  memory_limit: string
  disk_quota: string | null
  auto_restart: boolean
  created_at: datetime
  updated_at: datetime
```

### 5.4 Platform Settings

Platform settings store global configuration:

```yaml
PlatformSettings:
  data_dir: string
  admin_token_hash: string
  default_model_provider: string
  default_model_name: string
  runtime_driver: podman
  podman_path: string
```

### 5.5 Secrets

MVP distinguishes two kinds of secrets:

1. Platform shared secrets
2. Agent-specific secrets

Platform shared secrets include model API keys that can be inherited by agents.

Agent-specific secrets include messaging platform login states, bot tokens, or personal service tokens.

MVP may store secrets in local encrypted files or OS keychain where available. If encryption is not implemented in the first iteration, the spec must clearly mark this as a security limitation and avoid exposing secret values in API responses or logs.

---

## 6. Runtime and Isolation Requirements

### 6.1 Runtime choice

AgentBox MUST NOT require Docker Desktop.

MVP MUST use Podman / rootless Podman as the preferred container runtime.

AgentBox SHOULD define a runtime abstraction so future runtimes can be added:

```text
RuntimeDriver
  PodmanDriver       # MVP
  KubernetesDriver   # future
  FirecrackerDriver  # future
  KataDriver         # future
  ProcessDriver      # optional dev/debug only
```

### 6.2 Container-per-agent model

MVP MUST run each agent as a separate long-running container.

Example:

```text
agentbox-hermes-family-member-1
agentbox-hermes-family-member-2
agentbox-openclaw-primary
```

Each container MUST have:

- independent mounted data directory
- independent environment variables
- independent process space
- independent filesystem view
- CPU limit
- memory limit

### 6.3 Filesystem isolation

Each agent MUST only mount its own directory by default.

Default host layout:

```text
~/.agentbox/
  config.yaml
  agentbox.db
  secrets/
  runtime/
  agents/
    <agent_id>/
      agent.yaml
      hermes/ or openclaw/
      workspace/
      logs/
      backups/
      runtime/
```

Default container layout:

```text
/agent/home       # runtime home, e.g. HERMES_HOME
/agent/workspace  # working directory
```

MVP MUST NOT mount:

- host `/home` or user home directory
- other agent directories
- `/var/run/docker.sock`
- Podman socket
- host root filesystem
- arbitrary host paths by default

Future versions may support explicit external mounts with read-only/read-write settings, but MVP does not need a mount policy UI.

### 6.4 Security posture

MVP isolation goal:

> Agents can freely operate inside their own environment, but should not pollute the host or attack other agents.

MVP SHOULD:

- prefer rootless Podman
- avoid privileged containers
- avoid host network mode by default
- use non-root users inside runtime images where practical
- restrict mounted directories to the agent's own directory
- avoid mounting container runtime sockets

MVP does not implement strong untrusted-code isolation. Future versions may add gVisor, Kata, Firecracker, or MicroVM-based runtimes.

---

## 7. Agent Lifecycle

MVP agents are long-running, always-on instances.

AgentBox MUST NOT implement on-demand wake-up in MVP.

Rationale:

- Hermes/OpenClaw agents usually connect directly to messaging gateways.
- Intercepting messages to wake agents would require AgentBox to reimplement gateway routing.
- Cold start harms family and team user experience.
- Serverless/Knative would add complexity unrelated to the first product goal.

### 7.1 States

MVP agent states:

```text
created
starting
running
unhealthy
restarting
stopping
stopped
failed
deleted
```

### 7.2 Supported actions

MVP MUST support:

- create
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
- delete

### 7.3 Auto restart

Each agent SHOULD have `auto_restart` configuration. MVP may implement this through the platform service monitoring loop or Podman restart policy.

---

## 8. Hermes Runtime Specification

Hermes Agent is P0 runtime.

### 8.1 Boundary

AgentBox MUST NOT fork Hermes or reimplement Hermes gateway.

AgentBox is responsible for:

- creating independent `HERMES_HOME`
- generating Hermes `config.yaml` and `.env`
- injecting platform model configuration
- starting/stopping the Hermes container
- exposing logs/status/shell/backup/restore/upgrade
- providing gateway setup guidance

Hermes is responsible for:

- WeChat / Feishu / Telegram / Slack / other native gateway adapters
- memory
- sessions
- skills
- tool calling
- cron
- messaging behavior

### 8.2 Host directory layout

For Hermes agent `<agent_id>`:

```text
~/.agentbox/agents/<agent_id>/
  agent.yaml
  hermes/
    config.yaml
    .env
    skills/
    sessions/
    logs/
    memory/
    profiles/
    auth.json
  workspace/
  backups/
  runtime/
    Containerfile.snapshot
    image-version.txt
```

### 8.3 Container environment

The Hermes container MUST mount:

```text
~/.agentbox/agents/<agent_id>/hermes    -> /agent/home
~/.agentbox/agents/<agent_id>/workspace -> /agent/workspace
```

Required environment variables:

```text
HERMES_HOME=/agent/home
HOME=/agent
```

Working directory:

```text
/agent/workspace
```

### 8.4 Runtime image strategy

MVP MUST maintain a local Containerfile for Hermes runtime.

Image name:

```text
agentbox/hermes-runtime:<version>
```

Build command:

```bash
podman build -t agentbox/hermes-runtime:<version> -f runtimes/hermes/Containerfile .
```

The image SHOULD include:

- Linux base image
- Python runtime
- git
- curl
- build tools needed by Hermes
- Hermes Agent installation
- optional lightweight agentbox management scripts

Future versions MAY support pulling prebuilt images from a remote registry.

### 8.5 Default command

MVP default command for Hermes agents:

```bash
hermes gateway run
```

Reason: the main use case is long-running messaging-channel agents.

MVP MAY allow future `hermes_mode` values:

```yaml
hermes_mode: gateway | cli
```

But MVP default is `gateway`.

### 8.6 Model configuration injection

Platform-level model settings should be inherited by newly created Hermes agents.

Example platform config:

```yaml
model:
  provider: openrouter
  default: anthropic/claude-sonnet-4
```

Example generated Hermes config:

```yaml
model:
  provider: openrouter
  default: anthropic/claude-sonnet-4
```

Example generated `.env`:

```env
OPENROUTER_API_KEY=...
```

Owner should not need to configure model keys manually.

### 8.7 Gateway setup

MVP does not need to implement a graphical Hermes gateway setup wizard.

MVP MUST support:

```bash
agentbox agent shell <agent_id>
```

Then administrator can run inside the container:

```bash
hermes gateway setup
```

MVP SHOULD also support:

```bash
agentbox agent exec <agent_id> -- hermes gateway setup
```

Web Console MUST show setup instructions on the Agent Detail page.

P1 may implement a Web guided setup, QR display, and binding-state detection.

### 8.8 Health check

MVP health check for Hermes SHOULD include:

- container is running
- `hermes gateway` process exists
- basic config files exist and are parseable
- recent container logs do not show fatal startup errors

Suggested commands:

```bash
podman inspect <container>
podman exec <container> pgrep -f "hermes gateway"
podman logs --tail 200 <container>
```

### 8.9 Logs

MVP MUST expose:

- container logs
- Hermes logs directory if available

CLI:

```bash
agentbox agent logs <agent_id>
agentbox agent logs <agent_id> --follow
```

Web:

- Agent Detail page shows latest logs.
- It should support manual refresh.

### 8.10 Backup

Backup SHOULD package:

- `agent.yaml`
- Hermes home directory
- workspace
- relevant config and runtime metadata

Backup SHOULD NOT include:

- container image layers
- temporary caches
- large dependency cache unless explicitly included later

Backup path:

```text
~/.agentbox/agents/<agent_id>/backups/<timestamp>.tar.gz
```

### 8.11 Restore

Restore workflow:

1. Stop agent.
2. Create safety backup of current data.
3. Extract selected backup.
4. Restore permissions.
5. Start agent.
6. Run health check.
7. If failed, allow rollback to safety backup.

### 8.12 Reset

MVP CLI SHOULD support:

```bash
agentbox agent reset <agent_id> --config
agentbox agent reset <agent_id> --sessions
agentbox agent reset <agent_id> --memory
agentbox agent reset <agent_id> --all
```

Web MVP may expose only:

- Restart
- Factory Reset

Dangerous reset operations MUST require confirmation.

### 8.13 Upgrade

Hermes version SHOULD belong to the runtime image, not mutable per-container state.

Upgrade workflow:

1. Build or pull new `agentbox/hermes-runtime:<version>` image.
2. Backup agent data.
3. Stop container.
4. Remove old container.
5. Recreate container with same mounted data directory.
6. Start container.
7. Run health check.
8. Roll back to old image if health check fails.

---

## 9. OpenClaw Runtime Specification

OpenClaw is P1 runtime.

MVP/P1 goal is to validate runtime abstraction, not to implement deep OpenClaw-specific management.

P1 SHOULD support:

- OpenClaw runtime adapter
- independent data directory
- local Containerfile build for `agentbox/openclaw-runtime:<version>`
- start
- stop
- restart
- status
- logs
- shell
- exec
- backup
- restore

P1 does not need:

- full messaging platform setup wizard
- deep OpenClaw-specific health detection
- specialized OpenClaw config UI

---

## 10. Platform Service and Cross-Platform Requirements

AgentBox MUST support Windows, macOS, and Linux.

### 10.1 Linux

Linux is the recommended production environment.

Expected runtime:

```text
AgentBox backend service
Podman/rootless Podman
Agent containers
```

Service manager:

```text
systemd user service or system service
```

### 10.2 macOS

macOS should run AgentBox control plane natively and run Linux containers through Podman Machine.

Expected runtime:

```text
AgentBox macOS process
Podman Machine Linux VM
Agent containers
```

Service manager:

```text
launchd
```

### 10.3 Windows

Windows should support Podman Machine / WSL2 / Hyper-V backed Linux containers.

Expected runtime:

```text
AgentBox Windows process or WSL2 process
Podman Machine / WSL2 Linux VM
Agent containers
```

Service manager:

```text
Windows Service
```

### 10.4 Service commands

CLI SHOULD support:

```bash
agentbox server
agentbox service install
agentbox service start
agentbox service stop
agentbox service status
agentbox service uninstall
```

MVP MUST implement the command interface for all three platforms. If full service installation is incomplete for a platform, the command must return a clear unsupported/not-yet-implemented error rather than failing silently.

---

## 11. Authentication Requirements

MVP uses single-admin authentication.

### 11.1 Admin token

On first init, AgentBox MUST generate or ask for an admin token/password.

- API requires bearer token.
- Web Console requires login with token/password.
- CLI reads token from local config.

MVP does not implement:

- multi-user login
- Owner self-service login
- RBAC
- SSO
- audit-based access control

Future versions may add these.

### 11.2 Localhost default

By default, backend should bind to localhost only:

```text
127.0.0.1:port
```

Exposing AgentBox on a LAN or public network should require explicit configuration.

---

## 12. Secrets and Model Configuration

### 12.1 Platform shared model key

AgentBox MUST support platform-level shared model configuration.

Purpose: administrator configures model provider and key once; family members or employees do not configure model keys.

Example CLI:

```bash
agentbox config set model.provider openrouter
agentbox config set model.default anthropic/claude-sonnet-4
agentbox secret set OPENROUTER_API_KEY
```

### 12.2 Agent-specific secrets

Agent-specific secrets include:

- WeChat login state
- Telegram bot token
- Feishu app secret
- personal GitHub token
- personal email OAuth token

MVP may initially store these inside the agent's runtime home when the underlying agent framework does so. AgentBox must not copy agent-specific secrets into other agents.

### 12.3 API behavior

Secret values MUST NOT be returned by normal API responses.

API should return only metadata:

```yaml
SecretRef:
  name: OPENROUTER_API_KEY
  scope: platform | agent
  exists: true
  updated_at: datetime
```

---

## 13. Resource Management

MVP MUST support CPU and memory limits per agent.

Default values:

```yaml
resources:
  cpu_limit: "1"
  memory_limit: "1g"
  disk_quota: null
```

CLI example:

```bash
agentbox agent create family-hermes --owner family-member-1 --runtime hermes --cpu 0.5 --memory 1g
```

Disk quota can be recorded in the model but may be implemented later, because cross-platform disk quota support is more complex.

MVP SHOULD display approximate resource usage in Web Console if available from Podman inspect/stats.

---

## 14. Backend API Specification

MVP API should be RESTful and JSON-based.

All protected endpoints require admin token.

### 14.1 Health

```http
GET /health
```

Returns backend health.

### 14.2 Owners

```http
POST /owners
GET /owners
GET /owners/{owner_id}
PATCH /owners/{owner_id}
DELETE /owners/{owner_id}
```

### 14.3 Agents

```http
POST /agents
GET /agents
GET /agents/{agent_id}
PATCH /agents/{agent_id}
DELETE /agents/{agent_id}
```

Actions:

```http
POST /agents/{agent_id}/start
POST /agents/{agent_id}/stop
POST /agents/{agent_id}/restart
GET  /agents/{agent_id}/status
GET  /agents/{agent_id}/logs
POST /agents/{agent_id}/backup
GET  /agents/{agent_id}/backups
POST /agents/{agent_id}/restore
POST /agents/{agent_id}/reset
POST /agents/{agent_id}/diagnose
POST /agents/{agent_id}/upgrade
POST /agents/{agent_id}/exec
```

### 14.4 Runtime images

```http
GET  /runtimes
POST /runtimes/{runtime}/build
GET  /runtimes/{runtime}/images
```

### 14.5 Settings and secrets

```http
GET   /settings
PATCH /settings
POST  /secrets
GET   /secrets
DELETE /secrets/{name}
```

### 14.6 Service status

```http
GET /system/runtime
GET /system/podman
GET /system/resources
```

---

## 15. CLI Specification

CLI command name:

```bash
agentbox
```

### 15.1 Init and server

```bash
agentbox init
agentbox server
agentbox status
```

### 15.2 Service management

```bash
agentbox service install
agentbox service start
agentbox service stop
agentbox service status
agentbox service uninstall
```

### 15.3 Owner commands

```bash
agentbox owner create <name> --display-name <display_name>
agentbox owner list
agentbox owner show <owner_id>
agentbox owner update <owner_id>
agentbox owner delete <owner_id>
```

### 15.4 Agent commands

```bash
agentbox agent create <name> --owner <owner_id> --runtime hermes
agentbox agent list
agentbox agent show <agent_id>
agentbox agent start <agent_id>
agentbox agent stop <agent_id>
agentbox agent restart <agent_id>
agentbox agent status <agent_id>
agentbox agent logs <agent_id> [--follow]
agentbox agent shell <agent_id>
agentbox agent exec <agent_id> -- <command...>
agentbox agent backup <agent_id>
agentbox agent backups <agent_id>
agentbox agent restore <agent_id> <backup_file>
agentbox agent reset <agent_id> [--config|--sessions|--memory|--all]
agentbox agent diagnose <agent_id>
agentbox agent upgrade <agent_id> [--image <image>]
agentbox agent delete <agent_id>
```

### 15.5 Runtime commands

```bash
agentbox runtime list
agentbox runtime build hermes
agentbox runtime build openclaw
agentbox runtime images
```

### 15.6 Config and secrets

```bash
agentbox config get <key>
agentbox config set <key> <value>
agentbox secret set <name>
agentbox secret list
agentbox secret delete <name>
```

---

## 16. Web Console Specification

MVP Web Console should be simple and functional.

### 16.1 Pages

Required pages:

1. Login
2. Dashboard
3. Owners
4. Owner Detail
5. Agents
6. Agent Detail
7. Logs
8. Backups
9. Settings

### 16.2 Dashboard

Show:

- total agents
- running agents
- stopped agents
- failed/unhealthy agents
- Podman runtime status
- approximate host resource summary if available

### 16.3 Owners page

Support:

- list owners
- create owner
- edit owner display name/description
- delete owner if no active agents or with explicit confirmation

### 16.4 Agents page

Support:

- list agents
- filter by owner/runtime/status
- create agent
- show status
- quick start/stop/restart

### 16.5 Agent Detail page

Show:

- agent ID/name/display name
- owner
- runtime type
- status
- container name
- image
- CPU/memory config
- data directory
- recent logs
- actions: start, stop, restart, shell instruction, backup, restore, diagnose, upgrade, delete
- Hermes gateway setup guidance for Hermes agents

For MVP, Web Console may show shell/exec instructions instead of embedding a terminal.

### 16.6 Settings page

Support:

- platform data directory display
- Podman path/status
- default model provider/model
- platform model key setup metadata
- admin token rotation if implemented

---

## 17. Backup, Restore, Repair, and Upgrade

### 17.1 Backup

MVP MUST provide one-click/one-command backup per agent.

Backup should be a `.tar.gz` archive stored under the agent's backup directory.

### 17.2 Restore

Restore MUST stop the agent first and create a safety backup before overwriting current data.

### 17.3 Diagnose

Diagnose should collect:

- AgentBox metadata
- runtime type
- container status
- image version
- config file existence
- recent logs
- Podman inspect summary
- process check result

### 17.4 Repair

MVP repair can be conservative:

- regenerate missing config from template
- fix directory permissions
- restore missing required directories
- validate YAML files

Repair MUST NOT delete memory/sessions/workspace without explicit reset.

### 17.5 Upgrade

Upgrade must backup first, recreate container with new image, then health check.

---

## 18. Internal Management Channel

MVP management channel is implemented through Podman exec.

Examples:

```bash
podman exec <container> <command>
podman logs <container>
podman inspect <container>
```

AgentBox should abstract this as:

```text
ManagementChannel
  exec(command)
  shell()
  status()
  diagnose()
```

Future implementations may use:

- Unix socket sidecar
- agent supervisor process
- VM guest agent
- Kubernetes exec
- SSH

---

## 19. Data Storage

### 19.1 Database

MVP uses SQLite:

```text
~/.agentbox/agentbox.db
```

Should store:

- owners
- agents
- runtime image metadata
- backups metadata
- platform settings
- secret metadata, not plaintext secret values if avoidable
- operation history

### 19.2 Filesystem

MVP stores agent data in:

```text
~/.agentbox/agents/<agent_id>/
```

This directory is the source of truth for that agent's persistent data.

---

## 20. Implementation Milestones

### Milestone 0: Skeleton

- project structure
- FastAPI app
- Typer CLI
- SQLite setup
- config path handling
- basic tests

### Milestone 1: Owner and Settings

- owner CRUD
- settings CRUD
- admin token
- CLI and API for settings/secrets metadata

### Milestone 2: Podman Driver

- detect Podman
- run Podman commands
- build image
- inspect container
- logs
- exec

### Milestone 3: Hermes Runtime P0

- Hermes Containerfile
- build image
- create Hermes agent directory
- generate config/.env
- create/start/stop/restart Hermes container
- logs/status/shell

### Milestone 4: Backup/Restore/Reset/Diagnose

- backup archive
- restore with safety backup
- reset flags
- diagnose report

### Milestone 5: Web Console

- login
- dashboard
- owner pages
- agent pages
- settings page

### Milestone 6: Cross-platform service wrappers

- Linux systemd
- macOS launchd
- Windows Service
- clear unsupported handling where incomplete

### Milestone 7: OpenClaw P1

- OpenClaw runtime adapter
- Containerfile
- basic lifecycle/logs/shell/backup

---

## 21. Acceptance Criteria

MVP is acceptable when all the following are true:

1. User can install/init AgentBox on Linux with Podman.
2. User can configure a platform model provider and API key once.
3. User can create an owner named `family-member-1`.
4. User can create a Hermes agent for `family-member-1`.
5. AgentBox creates a separate data directory for the Hermes agent.
6. AgentBox builds or uses a local Hermes runtime image.
7. AgentBox starts the Hermes agent as a Podman container.
8. Hermes container uses its own `HERMES_HOME`.
9. Hermes container does not mount host home or other agent directories.
10. User can see agent status through CLI and Web Console.
11. User can see agent logs through CLI and Web Console.
12. User can enter the agent container shell and run `hermes gateway setup`.
13. User can stop/restart the agent.
14. User can backup the agent.
15. User can restore the agent from backup.
16. User can diagnose basic runtime problems.
17. User can create a second Hermes agent for another owner, with separate directory/container.
18. The two agents cannot see each other's mounted data directory by default.
19. Web Console requires admin token login.
20. CLI can perform the same core actions as Web Console.

---

## 22. Future Roadmap

Future versions may add:

- shared / group agents
- Owner self-service login
- RBAC
- enterprise audit
- tool policy
- network policy
- file mount policy UI
- secrets backend integration
- Web gateway setup wizard and QR display
- embedded terminal in Web Console
- resource quota dashboard
- cost tracking
- multi-node scheduling
- Kubernetes runtime
- Firecracker / Kata / gVisor runtime
- Agent collaboration through queues/messages, not direct filesystem/process access
- marketplace for runtime templates

---

## 23. Key Design Principles

1. Start from the personal/family/small-team problem, not enterprise overengineering.
2. One owner can have multiple agents.
3. MVP agent belongs to exactly one owner.
4. Agents are long-running, not serverless.
5. AgentBox does not reimplement native agent gateways.
6. Each agent lives in its own box.
7. Use Podman/rootless Podman; do not require Docker Desktop.
8. Let agents do anything inside their own isolated environment in MVP.
9. Share model keys at the platform level to reduce user configuration burden.
10. Keep future policy, VM, enterprise, and collaboration extensions possible without forcing them into MVP.
