# AgentBox Legacy Spec Notice

The repository has been repositioned.

The old implementation-heavy spec has been replaced by a more flexible product-spec and prompt-kit structure.

Please use:

- `docs/vision.md`
- `docs/mvp-spec.md`
- `docs/architecture-principles.md`
- `docs/safety-rules.md`
- `docs/acceptance-demo.md`
- `prompts/`

AgentBox is now framed as:

```text
open product idea + MVP specification + prompt kit + optional reference implementations
```

rather than one fixed implementation plan.

The essential idea remains:

> Manage multiple isolated, long-running AI agent instances on one machine, with safe runtime isolation and shared platform-level model configuration.
