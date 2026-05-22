# Prompt 03: Hermes Runtime Milestone

Use this prompt after the implementation has a safe container/runtime driver.

---

You are implementing the AgentBox Hermes runtime milestone.

AgentBox should be able to run a dedicated Hermes Agent instance for each managed agent.

Use any branch and workflow you prefer. Preserve the product intent and safety rules.

## Goal

Add a Hermes runtime adapter that prepares per-agent Hermes homes, generates config/env files, injects platform model settings safely, and starts Hermes as a long-running isolated runtime.

## Required Behavior

For each Hermes agent:

- create independent runtime home;
- create independent workspace;
- generate Hermes `config.yaml` or equivalent config;
- generate `.env` or equivalent environment file;
- inject platform default model provider;
- inject platform default model name;
- inject model API key without exposing it in CLI/API/UI output;
- run the container with `HERMES_HOME=/agent/home`;
- set `HOME=/agent`;
- set working directory to `/agent/workspace`;
- use a long-running Hermes command such as `hermes gateway run` where appropriate;
- provide shell access so an admin can run Hermes-native setup when necessary.

## Container Mounts

Mount only the agent's own directories:

```text
agent hermes home -> /agent/home
agent workspace   -> /agent/workspace
```

Do not mount host home, host root, other agents' data, or container runtime sockets.

## Useful Commands

Expose or document commands for:

- build Hermes runtime image;
- prepare Hermes home;
- start Hermes agent;
- stop Hermes agent;
- restart Hermes agent;
- view logs;
- open shell;
- inspect generated config with secrets redacted.

## Testing

Default tests should not require a live external model API.

Test:

- generated config shape;
- generated env shape with secrets protected;
- per-agent directory layout;
- correct mounts/env/workdir passed to the runtime driver;
- no dangerous mount paths;
- lifecycle operations call the runtime driver correctly.

## Do Not Implement Yet

- Web console unless already in scope;
- OpenClaw runtime;
- enterprise RBAC;
- Kubernetes;
- custom messaging gateway replacement.

## Acceptance Criteria

- a Hermes agent can be prepared and started through the chosen interface;
- each Hermes agent has an independent home and workspace;
- platform model settings are injected;
- secret values are not leaked;
- dangerous mounts are absent;
- tests pass.
