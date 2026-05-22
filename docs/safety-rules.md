# AgentBox Safety Rules

These rules are more important than the exact implementation stack.

AgentBox manages long-running agents that may hold credentials, memory, files, sessions, and access to communication channels. The MVP must avoid obvious isolation and secret-handling mistakes.

---

## 1. Do Not Mount Host Home

An agent container or sandbox must not mount the host user's home directory.

Bad examples:

```text
/home/user -> /home/user
/home/user -> /agent/home
~          -> /agent/home
```

Each agent should only receive its own runtime home and workspace.

---

## 2. Do Not Mount Host Root

Never mount host root into an agent runtime.

Bad examples:

```text
/ -> /host
/ -> /agent/host
```

---

## 3. Do Not Mount Other Agents' Data

Agent A must not receive Agent B's data directory.

Each agent should have a separate directory under the AgentBox data root.

---

## 4. Do Not Mount Container Runtime Sockets

Do not mount Docker or Podman sockets into agent containers.

Bad examples:

```text
/var/run/docker.sock -> /var/run/docker.sock
/run/podman/podman.sock -> /run/podman/podman.sock
```

Mounting container sockets can let an agent escape the intended isolation boundary.

---

## 5. Do Not Leak Secrets

Secret values must not be printed by normal commands, API responses, logs, or UI pages.

Allowed:

```json
{
  "name": "OPENROUTER_API_KEY",
  "scope": "platform",
  "exists": true,
  "updated_at": "..."
}
```

Not allowed:

```json
{
  "name": "OPENROUTER_API_KEY",
  "value": "sk-..."
}
```

---

## 6. Avoid Shell String Concatenation

Runtime commands should pass arguments as arrays/lists rather than shell-concatenated strings.

Preferred:

```python
subprocess.run(["podman", "start", container_name])
```

Avoid:

```python
subprocess.run(f"podman start {container_name}", shell=True)
```

---

## 7. Localhost by Default

If an implementation exposes an HTTP API, bind to localhost by default.

Exposing the API on a LAN or public network should require explicit configuration and authentication.

---

## 8. Safe Failure Behavior

If the runtime driver is missing, a container fails, or a lifecycle operation cannot complete, AgentBox should return clear errors and avoid partial unsafe state.

Examples:

- Podman missing: explain how to install or configure the runtime;
- start failed: preserve logs and status;
- restore failed: keep a safety backup;
- upgrade failed: allow rollback or manual recovery.
