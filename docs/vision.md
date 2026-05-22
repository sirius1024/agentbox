# AgentBox Vision

AgentBox is an open product idea for managing multiple isolated, long-running AI agent instances on one machine.

It exists because the practical problem is no longer only "how do I talk to one agent?" The new problem is:

> How do I safely run many dedicated agents for different people, roles, projects, and runtimes without manually managing containers, data directories, model keys, configs, login states, and startup scripts?

---

## Core Idea

AgentBox should make personal and small-team agent hosting feel like creating a managed app instance:

1. create an owner;
2. create an agent for that owner;
3. choose a runtime such as Hermes Agent, OpenClaw, or another agent framework;
4. start the agent in an isolated long-running runtime;
5. connect it to the runtime's native gateway or interface;
6. monitor, repair, backup, restore, and upgrade it.

---

## Product Shape

AgentBox is best understood as:

```text
multi-agent personal runtime manager
```

The first useful version should focus on one machine:

- personal computer;
- old home server;
- lab box;
- small team server;
- edge machine;
- workstation.

It should not begin as a complex enterprise platform.

---

## Target Scenarios

### Personal use

A technical user wants several separate agents:

- personal assistant;
- coding agent;
- research agent;
- operations agent;
- experiment agent.

Each agent should have its own memory, sessions, workspace, config, and runtime home.

### Family use

A technical user wants to create simple agent instances for family members.

Family users should not need to manage API keys, model names, containers, or config files. They should interact through the underlying agent framework's normal channels.

### Small team use

A manager or team lead wants one or more dedicated agents for team members, projects, or functions.

The MVP should support the structure for this, but not heavy enterprise governance.

### Runtime experimentation

Builders may want to compare Hermes Agent, OpenClaw, Claude Code wrappers, Codex CLI wrappers, or custom MCP agents under the same management concept.

AgentBox should provide a common lifecycle and isolation model while allowing runtime-specific behavior.

---

## Why Prompt Kit Instead of One Fixed Implementation?

The AI coding era changes open source collaboration.

Many people will not clone a project and contribute exactly as instructed. They may:

- paste the product spec into Codex;
- ask Claude Code to build a variant;
- use Kimi Code with a different stack;
- fork the concept into a new product;
- improve the prompt before implementing;
- build only the subset they need.

So AgentBox should provide:

- a clear product idea;
- necessary constraints;
- useful acceptance criteria;
- reusable prompts;
- optional reference implementations.

It should not over-prescribe branches, commits, tools, or one engineering workflow.

---

## Success Criteria

AgentBox succeeds if people can use this repository to quickly build or remix a system that:

- creates multiple independent agent instances;
- isolates their data and runtime state;
- shares platform-level model credentials safely;
- starts and stops long-running agent containers;
- supports basic monitoring and recovery;
- avoids dangerous host mounts and secret leakage;
- remains simple enough for personal and small-team use.
