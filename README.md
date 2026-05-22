# AgentBox

[简体中文](README.zh-CN.md)

**AgentBox is an open product idea, MVP spec, and prompt kit for building lightweight multi-agent runtime managers.**

It helps builders use their preferred coding agent to create systems that run many isolated, long-running AI agent instances on one personal computer, home server, lab machine, or small team server.

This repository is not a fixed implementation. It is a reusable product brief and prompt library for Codex, Claude Code, Kimi Code, OpenClaw, Cursor, or any other coding agent.

---

## Who This Is For

AgentBox is for builders who want to:

- run multiple dedicated AI agents on one machine;
- give each agent independent memory, sessions, config, workspace, and runtime home;
- avoid manually writing container scripts and copying API keys;
- use a coding agent to generate their own implementation;
- fork, remix, or extend the product idea.

If you are looking for an installable finished product, this repository is not that yet. It is the spec and prompt kit for creating one.

---

## Quick Start: Give AgentBox to Your Coding Agent

### 1. Pick your starting point

| Situation | Use this prompt |
| --- | --- |
| Start a new implementation | `prompts/00-build-from-scratch.md` |
| Add core domain and CRUD | `prompts/01-core-crud.md` |
| Add Podman/container lifecycle | `prompts/02-podman-runtime.md` |
| Add Hermes Agent runtime | `prompts/03-hermes-runtime.md` |
| Add backup/restore/diagnose/upgrade | `prompts/04-lifecycle-backup.md` |
| Add Web Console | `prompts/05-web-console.md` |
| Need a short general prompt | `prompts/variants/minimal.md` |

### 2. Provide the coding agent with context

Give it this repository, or paste these files:

```text
README.md
docs/vision.md
docs/mvp-spec.md
docs/safety-rules.md
prompts/<selected-prompt>.md
```

### 3. Use a direct task instruction

```text
Use the AgentBox product spec and prompt kit as input.
Implement the milestone in prompts/<selected-prompt>.md.
Keep the implementation simple and focused.
Preserve the safety rules in docs/safety-rules.md.
Do not implement unrelated future features yet.
Add tests and explain how to run them.
```

You may use any branch workflow, stack, or coding agent. The safety rules and acceptance criteria matter more than exact file layout.

---

## How to Iterate When Requirements Change

AgentBox is meant to evolve through prompt-driven iteration. When you change or add requirements, do **not** just tell your coding agent “continue.” Give it a clear delta.

Recommended loop:

1. **Write the change first**
   - Update your own notes, `docs/mvp-spec.md`, or create a new prompt under `prompts/`.
   - Keep the change small enough to verify.

2. **Tell the coding agent what changed**
   - New behavior;
   - changed behavior;
   - removed behavior;
   - constraints that must remain true.

3. **Define acceptance criteria**
   - What commands, tests, UI flows, or demos prove the change works?

4. **Ask the coding agent to update docs/prompts if the product behavior changed**
   - Code should not drift away from the prompt kit.

5. **Review the result against safety rules**
   - Especially mounts, secrets, isolation, and command execution.

### Requirement-change prompt template

```text
We are iterating on an AgentBox implementation.

Context:
- Read README.md, docs/mvp-spec.md, docs/safety-rules.md, and the relevant prompt under prompts/.
- Preserve the existing product intent: one-machine, isolated, long-running agent instances.

Requirement change:
- Add/change/remove: <describe the exact requirement delta>

Must keep:
- No host-home mount.
- No host-root mount.
- No Docker/Podman socket mount.
- No other-agent data mount.
- No secret leakage.
- No unsafe shell command concatenation.

Out of scope:
- <list what should not be implemented in this iteration>

Acceptance criteria:
- <test/demo/check 1>
- <test/demo/check 2>
- <test/demo/check 3>

Tasks:
1. Update the implementation.
2. Add or update tests.
3. Update docs or prompts if behavior changed.
4. Summarize what changed, how to run it, and what remains out of scope.
```

This pattern keeps the coding agent grounded without forcing one rigid engineering process.

---

## Core Product Idea

AgentBox should make personal and small-team agent hosting feel like creating managed app instances:

1. create an owner;
2. create an agent for that owner;
3. choose a runtime such as Hermes Agent, OpenClaw, or another agent framework;
4. start the agent in an isolated long-running container or sandbox;
5. connect it through the runtime's native interface or gateway;
6. monitor, repair, backup, restore, and upgrade it.

Each agent should have its own:

- runtime home;
- workspace;
- memory and sessions;
- configuration;
- login state;
- lifecycle.

---

## Non-Negotiable Safety Rules

Any AgentBox-like implementation should preserve these rules:

- no Docker Desktop dependency;
- no host home mounted into agent runtimes;
- no host root mounted into agent runtimes;
- no other agent's data mounted into an agent runtime;
- no Docker or Podman socket mounted into agent runtimes;
- no secret values printed through CLI, API, logs, or UI;
- no unsafe shell string concatenation for runtime commands.

See `docs/safety-rules.md` for details.

---

## What Should Stay Consistent

- one machine first;
- many isolated long-running agent instances;
- one owner can have multiple agents;
- one agent belongs to one owner in the MVP;
- platform-level model provider/key support;
- container or sandbox based isolation;
- Podman/rootless-first runtime is recommended.

---

## What You Can Change

You are encouraged to remix:

- implementation language;
- backend framework;
- database;
- UI design;
- coding agent;
- branch workflow;
- prompt style;
- runtime driver;
- deployment model;
- milestone order.

Suggested stack, if you want one:

- Python + FastAPI;
- Typer CLI;
- SQLite;
- React + Vite + TypeScript;
- Podman/rootless Podman.

---

## Repository Map

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

## MVP Non-Goals

Do not let the first useful implementation drift into:

- SaaS multi-tenancy;
- Kubernetes orchestration;
- enterprise RBAC/audit;
- marketplace features;
- serverless/Knative wake-up;
- custom messaging gateway replacement;
- Docker Desktop dependency;
- unsafe host mounts or secret leakage.

These may become future experiments, but they should not dominate the MVP.

---

## Current Status

This repository is currently a product idea, MVP specification, and prompt kit.

Earlier implementation code was intentionally removed from the main branch to keep the project open-ended and agent-friendly.

Future contributors may add reference implementations under a clearly named directory such as:

```text
reference-implementations/python-fastapi/
```

---

## License

MIT. See [LICENSE](LICENSE).
