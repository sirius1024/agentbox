# Kimi Code Variant Prompt

Use this with Kimi Code or another coding agent.

---

You are implementing or remixing AgentBox.

AgentBox is a lightweight one-machine manager for multiple isolated, long-running AI agent instances.

Read first:

- README.md;
- docs/vision.md;
- docs/mvp-spec.md;
- docs/safety-rules.md;
- prompts/variants/minimal.md.

Your task is to implement the requested milestone only.

Keep the project flexible:

- branch names are not prescribed;
- implementation stack may vary;
- prompt can be adapted;
- acceptance criteria and safety rules matter more than exact file layout.

Required safety behavior:

- no Docker Desktop dependency;
- no host home/root mount;
- no other agent data mount;
- no Docker/Podman socket mount;
- no secret leakage;
- no unsafe shell concatenation.

Testing:

- add focused tests;
- default tests should not require real external services;
- integration tests should be opt-in.

When complete, explain:

- what changed;
- how to run;
- how to test;
- what is intentionally not implemented.
