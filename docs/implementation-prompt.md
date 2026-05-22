# AgentBox Initial Implementation Prompt

This file is kept for compatibility with earlier versions of the repository.

For the current prompt-kit layout, prefer the files under `prompts/`:

- `prompts/00-build-from-scratch.md`
- `prompts/01-core-crud.md`
- `prompts/02-podman-runtime.md`
- `prompts/03-hermes-runtime.md`
- `prompts/04-lifecycle-backup.md`
- `prompts/05-web-console.md`

---

## Short Prompt

Build or continue AgentBox: a lightweight manager for multiple isolated, long-running AI agent instances on one machine.

Read:

- `README.md`
- `docs/vision.md`
- `docs/mvp-spec.md`
- `docs/architecture-principles.md`
- `docs/safety-rules.md`
- `docs/acceptance-demo.md`

Implement the requested milestone only.

Preserve these constraints:

- one machine first;
- many isolated long-running agents;
- independent runtime home and workspace per agent;
- platform-level model settings and secret injection;
- no Docker Desktop dependency;
- no host-home/root/socket mounts;
- no other-agent data mounts;
- no secret leakage;
- no unsafe shell command construction.

You may use any branch, commit workflow, coding agent, or implementation stack.

When done, provide:

- summary;
- verification commands;
- test results;
- intentionally deferred scope.
