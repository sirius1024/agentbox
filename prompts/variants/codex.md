# Codex Variant Prompt

Use this with Codex or another autonomous coding CLI.

---

You are working on AgentBox, an open product idea and prompt kit for building lightweight multi-agent runtime managers.

Before coding, read:

- README.md;
- docs/vision.md;
- docs/mvp-spec.md;
- docs/safety-rules.md;
- docs/acceptance-demo.md.

Implement the requested milestone only. Preserve the safety rules and do not overbuild.

Workflow guidance:

- use your preferred branch/commit workflow;
- keep changes focused;
- add tests before or alongside code;
- do not require external services for default tests;
- use generic examples only;
- do not add personal, private, family, or company-specific data;
- summarize commands and verification at the end.

Hard constraints:

- no Docker Desktop dependency;
- no host-home mount;
- no host-root mount;
- no other-agent-data mount;
- no Docker/Podman socket mount;
- no secret leakage;
- no shell string concatenation for user-controlled runtime commands.

If requirements are ambiguous, choose the simplest MVP behavior and document the assumption.
