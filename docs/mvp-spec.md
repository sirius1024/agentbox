# AgentBox MVP Specification

This document defines the minimum useful behavior for an AgentBox-like implementation.

It is a product specification, not a mandatory engineering plan. Implementers may choose their own stack and workflow as long as the product behavior and safety constraints are preserved.

---

## 1. MVP Goal

Build a lightweight manager for multiple isolated, long-running AI agent instances on one machine.

The MVP should support:

- owners;
- agent instances;
- platform settings;
- secret references and secret storage;
- container or sandbox lifecycle;
- runtime-specific setup for at least one agent framework;
- CLI and/or API management;
- clear status, logs, backup, restore, and diagnosis paths.

---

## 2. Core Objects

### Owner

An owner represents the human, role, or project served by one or more agents.

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

Rules:

- one owner may have multiple agents;
- an owner can be a person, role, or project;
- MVP does not require each owner to log in to AgentBox;
- MVP may use one admin identity for platform management.

### Agent

An agent is a dedicated long-running runtime instance.

Suggested fields:

```yaml
Agent:
  id: string
  name: string
  display_name: string
  owner_id: string
  runtime_type: hermes | openclaw | custom
  status: created | starting | running | unhealthy | restarting | stopping | stopped | failed | deleted
  container_name: string
  image: string
  data_dir: string
  cpu_limit: string | null
  memory_limit: string | null
  disk_quota: string | null
  auto_restart: boolean
  created_at: datetime
  updated_at: datetime
```

Rules:

- one agent belongs to exactly one owner in the MVP;
- an agent is not shared by multiple owners in the MVP;
- each agent has its own runtime home, workspace, memory, sessions, and config;
- an agent can be stopped, restarted, inspected, backed up, restored, and upgraded.

### Platform Settings

Platform settings hold global defaults.

Suggested fields:

```yaml
PlatformSettings:
  data_dir: string
  default_model_provider: string | null
  default_model_name: string | null
  runtime_driver: podman | custom
  podman_path: string
  default_cpu_limit: string | null
  default_memory_limit: string | null
```

### Secret

Secrets store sensitive values such as model API keys.

Suggested fields:

```yaml
Secret:
  id: string
  name: string
  scope: platform | agent
  agent_id: string | null
  value_ref: string
  created_at: datetime
  updated_at: datetime
```

Rules:

- secret values must be write-only through normal CLI/API/UI flows;
- list/show responses expose metadata only;
- logs must not print secret values;
- generated configs may reference secrets but should avoid unnecessary duplication.

---

## 3. Runtime Model

Each agent should have an isolated data directory such as:

```text
AGENTBOX_HOME/
  agents/
    <agent_id>/
      runtime-home/
      workspace/
      backups/
      runtime/
```

A container-based implementation should mount only the agent's own directories, for example:

```text
<agent_dir>/runtime-home -> /agent/home
<agent_dir>/workspace    -> /agent/workspace
```

Runtime-specific names may vary. For Hermes Agent, `runtime-home` may be `hermes` and should map to `HERMES_HOME`.

---

## 4. Recommended Capabilities

### Core CRUD

- create/list/show/update/delete owners;
- create/list/show/update/delete agents;
- get/set platform settings;
- set/list/delete secrets without leaking values.

### Runtime lifecycle

- build runtime image;
- create container;
- start agent;
- stop agent;
- restart agent;
- remove container;
- inspect status;
- read logs;
- exec command;
- open shell.

### Management lifecycle

- backup agent metadata and data;
- restore agent from backup;
- reset an agent safely;
- diagnose common failures;
- upgrade runtime image/config with pre-upgrade backup.

### Interfaces

At least one management interface should exist:

- CLI;
- API;
- Web console.

A useful implementation may start with CLI only, then add API and Web later.

---

## 5. Hermes Runtime P0

A Hermes-oriented implementation should eventually support:

- one independent `HERMES_HOME` per agent;
- generated `config.yaml`;
- generated `.env`;
- platform default model provider/model injection;
- platform-level model API key injection;
- long-running command such as `hermes gateway run`;
- shell access so the admin can run runtime-native setup commands when needed.

---

## 6. Non-Goals for MVP

The MVP should not implement first:

- SaaS multi-tenancy;
- Kubernetes scheduling;
- serverless/Knative wake-up;
- complex enterprise RBAC;
- audit/compliance suite;
- agent marketplace;
- shared public agents;
- fine-grained per-tool policy editor;
- custom chat gateway replacement;
- Docker Desktop dependency.

---

## 7. Minimum Useful Demo

A useful MVP demo should prove:

1. initialize AgentBox data directory;
2. configure a platform model provider/key once;
3. create an owner;
4. create an agent for that owner;
5. create isolated agent runtime and workspace directories;
6. build or select a runtime image;
7. start the agent as a long-running isolated runtime;
8. inspect status and logs;
9. execute a command or open a shell in the agent runtime;
10. verify host home and container sockets are not mounted;
11. backup the agent;
12. restore the agent;
13. create a second agent and verify data isolation.
