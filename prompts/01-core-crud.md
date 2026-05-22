# Prompt 01: Core CRUD Milestone

Use this prompt when an AgentBox implementation needs its first domain model and persistence layer.

---

You are implementing the AgentBox core CRUD milestone.

AgentBox manages multiple isolated, long-running AI agent instances on one machine.

You may use any branch and coding-agent workflow. The important part is to satisfy the product behavior and safety criteria.

## Goal

Implement the foundation objects:

- Owner;
- Agent;
- Platform Settings;
- Secret metadata and write-only secret values.

## Required Behavior

### Owner

Support:

- create;
- list;
- show;
- update;
- delete.

An owner represents a person, role, team member, or project.

### Agent

Support:

- create;
- list;
- show;
- update;
- delete.

Rules:

- one owner can have many agents;
- one agent belongs to one owner in the MVP;
- creating an agent creates an isolated data directory;
- each agent should have a runtime home, workspace, backups directory, and runtime metadata directory.

### Platform Settings

Support reading and writing settings such as:

- default model provider;
- default model name;
- runtime driver;
- default resource limits;
- data directory.

### Secrets

Support:

- set secret value;
- list secret metadata;
- delete secret;
- never return the secret value in normal API/CLI/UI output.

## Recommended Interfaces

Implement CLI and/or API endpoints. If both are implemented, use a shared service/domain layer.

## Do Not Implement Yet

- Podman lifecycle;
- Hermes runtime adapter;
- Web console;
- backup/restore;
- enterprise features.

## Testing

Add tests for:

- owner CRUD;
- agent CRUD;
- per-agent directory creation;
- settings read/write;
- secret value not leaked;
- delete conflict behavior if useful.

## Acceptance Criteria

- default test suite passes;
- CRUD behavior works through chosen interface;
- secret values are write-only;
- generated examples are generic;
- next milestone is Podman runtime lifecycle.
