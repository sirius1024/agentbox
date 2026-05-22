# AgentBox Architecture Principles

This document captures the architectural intent behind AgentBox.

Implementations can vary, but these principles should remain stable.

---

## 1. Long-Running Agents First

AgentBox is designed for long-running dedicated agent instances.

The MVP should not be serverless-first. Messaging agents often need persistent gateway connections, login state, session state, memory, and background jobs. A long-running container or sandbox is easier to reason about for the first useful version.

---

## 2. One Agent, One Isolated Runtime Home

Each agent should have its own:

- runtime home;
- workspace;
- memory;
- sessions;
- config;
- environment;
- login state;
- backups.

Agents should not share a home directory by default.

---

## 3. Platform-Level Credential Injection

Many personal or family users should not need to manage model credentials.

AgentBox should support platform-level model provider/key configuration and inject the necessary environment or config into each managed agent.

Secret values must remain protected and should not be shown by default.

---

## 4. Runtime Adapters

AgentBox should not be tied to one agent framework forever.

A practical architecture separates:

```text
product/domain model -> runtime driver -> runtime adapter
```

Example layers:

- domain: Owner, Agent, Settings, Secret;
- driver: Podman or another sandbox/container backend;
- adapter: Hermes Agent, OpenClaw, custom MCP agent, coding-agent wrapper.

---

## 5. Podman/Rootless-First Recommendation

Podman/rootless Podman is recommended for local-first implementations because it avoids Docker Desktop dependency and fits a personal/server Linux environment well.

This is a recommendation, not a permanent universal requirement. Other sandbox technologies can be explored if they preserve the safety model.

---

## 6. CLI/API/Web Can Share the Same Service Layer

A clean implementation should avoid duplicating business logic across interfaces.

Recommended shape:

```text
CLI  -> service layer -> domain/runtime layer
API  -> service layer -> domain/runtime layer
Web  -> API/service layer
```

---

## 7. Reference Implementations Should Be Clearly Scoped

If this repository gains reference code, it should live under a clear directory such as:

```text
reference-implementations/python-fastapi/
```

This keeps the repository open-ended: the spec and prompts remain the primary artifact, while code is an example rather than the only valid implementation.
