# Prompt 04: Lifecycle, Backup, Restore, Diagnose

Use this prompt after basic runtime start/stop/logs behavior exists.

---

You are implementing AgentBox lifecycle management.

AgentBox manages isolated, long-running AI agent instances. Lifecycle operations should help the admin repair, preserve, restore, reset, and upgrade agents safely.

## Goal

Add management operations:

- backup;
- restore;
- reset;
- diagnose;
- upgrade.

## Backup Requirements

A backup should include:

- agent metadata;
- runtime type and image info;
- runtime home;
- workspace;
- relevant config files;
- enough metadata to restore safely.

Recommended format:

```text
.tar.gz archive
```

Do not include unnecessary host files. Do not leak platform secrets into metadata if avoidable.

## Restore Requirements

Restore should:

- validate backup format;
- stop the agent first if it is running;
- create a safety backup before overwriting current data;
- restore runtime home and workspace;
- restore metadata carefully;
- leave clear logs/results;
- avoid affecting other agents.

## Reset Requirements

Reset should support safe modes such as:

- reset workspace only;
- reset runtime home only;
- reset all agent data after confirmation;
- keep or remove backups depending on explicit option.

## Diagnose Requirements

Diagnose should check common problems:

- runtime driver missing;
- container missing;
- container failed;
- config missing;
- secret missing;
- dangerous mounts detected;
- runtime home missing;
- workspace missing;
- recent logs contain obvious errors.

## Upgrade Requirements

Upgrade should:

- backup first;
- build or pull new image;
- recreate container if needed;
- keep agent data;
- run a health/status check;
- report rollback instructions if upgrade fails.

## Safety Requirements

- do not overwrite data without a safety backup;
- do not restore into another agent unless explicitly requested and validated;
- do not print secret values;
- do not delete backups accidentally;
- keep operations auditable through clear logs.

## Testing

Test with temporary directories and fake runtime drivers.

Tests should cover:

- backup archive contents;
- restore safety backup;
- reset modes;
- diagnose findings;
- upgrade order of operations;
- failure handling.

## Acceptance Criteria

- lifecycle commands are available through the chosen interface;
- backup and restore work on test data;
- restore creates safety backup;
- diagnose returns actionable results;
- upgrade backs up first;
- default tests pass.
