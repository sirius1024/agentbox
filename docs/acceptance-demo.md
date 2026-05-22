# AgentBox Acceptance Demo

This checklist defines what a useful AgentBox-like implementation should eventually demonstrate.

It is not tied to a specific coding agent, branch plan, or implementation language.

---

## Demo 1: Core Setup

Show that the platform can initialize its data directory and store persistent state.

Expected proof:

- data directory exists;
- database or metadata store exists;
- config/settings can be read and written;
- test or demo environment does not touch unrelated user files.

---

## Demo 2: Owner and Agent Creation

Show that the platform can create:

- an owner;
- an agent assigned to that owner;
- isolated directories for that agent.

Expected proof:

```text
agents/<agent_id>/runtime-home
agents/<agent_id>/workspace
agents/<agent_id>/backups
```

Names may vary, but isolation must be visible.

---

## Demo 3: Secret Handling

Show that a platform-level model key can be configured without leaking the value.

Expected proof:

- secret can be set;
- secret metadata can be listed;
- secret value is not printed;
- generated runtime config does not expose more than necessary.

---

## Demo 4: Container Lifecycle

Show that an agent runtime can be managed.

Expected proof:

- build or select runtime image;
- create container or sandbox;
- start;
- stop;
- restart;
- inspect status;
- read logs;
- exec command;
- open shell or equivalent admin entrypoint.

---

## Demo 5: Isolation Verification

Show that the agent runtime does not receive dangerous host access.

Expected proof:

- host home is not mounted;
- host root is not mounted;
- Docker socket is not mounted;
- Podman socket is not mounted;
- another agent's data directory is not mounted;
- only the agent's own runtime home and workspace are mounted.

---

## Demo 6: Runtime-Specific Agent

For Hermes Agent or another target runtime, show that the runtime has its own generated config and home directory.

For Hermes-like runtimes, expected proof may include:

- independent runtime home;
- generated config;
- generated env;
- platform model provider/key injected safely;
- long-running gateway or service command configured.

---

## Demo 7: Backup and Restore

Show that an agent can be backed up and restored.

Expected proof:

- backup archive includes agent metadata, runtime home, and workspace;
- restore creates a safety backup before overwriting;
- restored agent remains startable;
- restore does not affect other agents.

---

## Demo 8: Two-Agent Isolation

Create two agents and prove they do not share runtime state.

Expected proof:

- separate directories;
- separate configs;
- separate container names;
- one agent cannot see or modify the other's mounted data;
- stopping one does not stop the other unless explicitly requested.
