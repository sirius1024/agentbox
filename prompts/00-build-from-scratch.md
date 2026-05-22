# Prompt 00: Build AgentBox From Scratch

Use this prompt when starting a new AgentBox-like implementation from a clean repository.

---

You are building **AgentBox**, a lightweight manager for multiple isolated, long-running AI agent instances on one machine.

AgentBox is an open product idea, not a rigid implementation mandate. You may choose the stack and branch workflow, but preserve the product intent and safety rules.

Read or create these conceptual documents:

- product vision;
- MVP spec;
- architecture principles;
- safety rules;
- acceptance demo.

## Product Goal

Build a system that can create and manage dedicated AI agent instances for different owners, roles, or projects.

Each agent should have its own:

- runtime home;
- workspace;
- memory/session data;
- config;
- login state;
- lifecycle.

## Recommended Stack

Use this stack unless you intentionally choose another:

- backend: Python + FastAPI;
- CLI: Typer;
- database: SQLite;
- runtime driver: Podman/rootless Podman;
- web later: React + Vite + TypeScript.

Alternative stacks are welcome if they preserve the MVP behavior.

## Initial Scope

Implement only the first useful foundation:

1. project skeleton;
2. owner model and CRUD;
3. agent model and CRUD;
4. platform settings;
5. secret metadata and write-only secret values;
6. isolated per-agent directory creation;
7. CLI and/or API for the above;
8. tests.

## Do Not Implement Yet

- Web console;
- Hermes runtime adapter;
- backup/restore;
- enterprise RBAC;
- Kubernetes;
- SaaS multi-tenancy;
- custom messaging gateway;
- Docker Desktop dependency.

## Safety Requirements

- never leak secret values;
- never use real private or personal names in examples;
- design for no host-home mounting in later runtime work;
- design each agent as isolated from other agents.

## Acceptance Criteria

- tests pass;
- owner CRUD works;
- agent CRUD works;
- settings can be read/written;
- secrets can be set/listed without showing values;
- creating an agent creates its isolated runtime/workspace directories;
- documentation explains how to run and test the implementation;
- next step is clearly identified as Podman runtime lifecycle.
