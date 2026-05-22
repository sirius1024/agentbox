# Prompt 05: Web Console Milestone

Use this prompt after core domain and lifecycle APIs are usable.

---

You are implementing a minimal AgentBox Web Console.

AgentBox manages multiple isolated, long-running AI agent instances. The Web Console should make the core management flows usable without requiring command-line expertise.

## Goal

Build a simple functional Web Console.

Recommended stack:

- React;
- Vite;
- TypeScript;
- Tailwind CSS or another simple UI system.

Alternative stacks are acceptable.

## Required Pages

Implement minimal pages for:

- login or admin-token entry;
- dashboard;
- owners list/detail;
- agents list/detail;
- agent logs;
- platform settings;
- secrets metadata and secret update form;
- backups/lifecycle actions if the backend supports them.

## Required Behavior

The UI should support:

- create owner;
- create agent;
- start/stop/restart agent;
- view status;
- view logs;
- set model provider/model;
- set secret values without showing existing values;
- trigger backup/restore if available.

## Do Not Overbuild

Do not implement first:

- enterprise dashboards;
- complex RBAC;
- marketplace;
- drag-and-drop orchestration;
- fine-grained policy editor;
- SaaS billing;
- custom messaging gateway.

## Security/UI Requirements

- never display secret values;
- show clear warning before destructive actions;
- make localhost/admin-token assumptions explicit;
- show runtime errors plainly;
- avoid embedding private example data.

## Testing

Add appropriate UI tests or component tests if the stack supports them.

At minimum, verify:

- app builds;
- key pages render;
- API client handles errors;
- secret forms do not display existing secret values;
- destructive actions require confirmation.

## Acceptance Criteria

- user can manage owners and agents from the UI;
- user can view agent status/logs;
- user can update settings and secrets safely;
- Web Console is simple, functional, and aligned with MVP scope;
- default build/test commands pass.
