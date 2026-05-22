# Minimal AgentBox Prompt

Use this when you want a short, flexible prompt.

---

Build or continue AgentBox: a lightweight manager for multiple isolated, long-running AI agent instances on one machine.

Keep the core idea:

- one machine first;
- many isolated agents;
- one owner can have multiple agents;
- one agent belongs to one owner in the MVP;
- each agent has its own runtime home, workspace, config, memory, sessions, and login state;
- platform-level model provider/key can be configured once and injected safely;
- Podman/rootless-first is recommended;
- no Docker Desktop dependency.

Do not violate safety rules:

- do not mount host home;
- do not mount host root;
- do not mount another agent's data;
- do not mount Docker/Podman sockets;
- do not leak secrets;
- do not shell-concatenate user input into runtime commands.

Implement the next useful milestone only. Do not jump to enterprise RBAC, Kubernetes, SaaS, marketplace, or custom gateway work.

Add or update tests. Default tests should not require external services unless explicitly marked as integration tests.

When done, summarize:

- what was implemented;
- how to run it;
- how to test it;
- what remains out of scope.
