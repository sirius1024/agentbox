# Prompt 02: Podman Runtime Milestone

Use this prompt when the implementation already has basic Owner/Agent records and per-agent data directories.

---

You are implementing the AgentBox Podman runtime milestone.

AgentBox is a lightweight platform for running multiple isolated, long-running AI agent instances on one personal computer, home server, lab machine, or small team server.

You may start from any AgentBox implementation or a clean repository. Use any branch, commit, or coding-agent workflow you prefer.

## Goal

Add a Podman-based runtime layer that can safely manage per-agent containers.

## Required Capabilities

Implement a runtime driver that can:

- detect Podman;
- report Podman version;
- build image;
- create container;
- start container;
- stop container;
- restart container;
- remove container;
- inspect container status;
- read logs;
- exec command inside container;
- open or prepare a shell command.

## Recommended Structure

This is recommended, not mandatory:

```text
runtime/
  errors
  spec
  podman driver
```

Have a container spec object that includes:

- name;
- image;
- command;
- environment;
- mounts;
- workdir;
- resource limits;
- restart policy.

## Safety Requirements

- never require Docker Desktop;
- never mount host home;
- never mount host root;
- never mount another agent's data directory;
- never mount Docker or Podman sockets into agent containers;
- never shell-concatenate user input;
- pass runtime commands as argument arrays/lists.

## MVP Container Isolation Model

Each agent should have its own data directory. The container should mount only:

```text
agent runtime home -> /agent/home
agent workspace    -> /agent/workspace
```

Runtime-specific environment variables may be added. For Hermes-like runtimes, `HERMES_HOME=/agent/home` is expected later.

## Useful CLI/API Behavior

Expose lifecycle operations through the chosen interface:

- start;
- stop;
- restart;
- status;
- logs;
- exec;
- shell;
- remove container.

## Testing

Default tests must not require real Podman.

Use mocks/fakes for subprocess or the runtime driver.

Test:

- command generation;
- error handling;
- dangerous mount rejection;
- lifecycle service behavior;
- CLI/API lifecycle commands if those interfaces exist.

Optional real-Podman integration tests are welcome, but they must be skipped unless explicitly enabled.

## Do Not Implement Yet

- Web console;
- full Hermes runtime adapter;
- backup/restore/reset/diagnose/upgrade;
- enterprise RBAC/audit;
- Kubernetes;
- Docker Desktop dependency.

## Acceptance Criteria

- existing CRUD behavior still works;
- container lifecycle commands are available;
- dangerous mounts are rejected;
- secret values are not leaked;
- default tests pass;
- implementation remains focused on the Podman runtime milestone.
