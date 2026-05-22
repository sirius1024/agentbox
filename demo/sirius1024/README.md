# sirius1024 AgentBox Demo

This directory is reserved for `sirius1024`'s own AgentBox implementation demo.

AgentBox itself is positioned as an open product idea, MVP specification, and prompt kit. This folder is intentionally scoped as a personal demo implementation area, not the only official implementation path.

## Purpose

This demo may later contain:

- one concrete AgentBox implementation;
- notes on how the prompts were used;
- implementation-specific architecture decisions;
- runnable code, tests, and setup instructions;
- screenshots or demo walkthroughs.

## Status

Placeholder only. Implementation code will be added later.

## Scope Guardrails

The demo should still preserve the core AgentBox principles:

- one machine first;
- isolated, long-running agent instances;
- independent runtime home and workspace per agent;
- platform-level model provider/key support;
- no host-home/root/socket mounts into agent runtimes;
- no secret leakage.

See the repository root README and `docs/` for the product-level specification.
