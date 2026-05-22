# Claude Code Variant Prompt

Use this with Claude Code or a similar coding agent.

---

You are helping build or remix AgentBox.

AgentBox is a product idea, MVP spec, and prompt kit for managing multiple isolated, long-running AI agent instances on one machine.

Please first inspect the repository and read:

- README.md;
- docs/vision.md;
- docs/mvp-spec.md;
- docs/architecture-principles.md;
- docs/safety-rules.md.

Then implement the requested milestone in a focused way.

Principles:

- prefer simple MVP behavior;
- avoid broad rewrites unless needed;
- keep interfaces clear;
- add tests for behavior and safety boundaries;
- document how to run and verify;
- keep examples generic.

Do not implement unrelated future features such as enterprise RBAC, Kubernetes, SaaS multi-tenancy, marketplace, or custom gateway replacement.

Security boundaries are non-negotiable:

- do not mount host home/root;
- do not mount container runtime sockets;
- do not mount data from other agents;
- do not leak secrets;
- do not build commands with unsafe shell concatenation.

At the end, provide:

- summary;
- test results;
- changed files;
- deferred scope.
