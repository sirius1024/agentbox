# AgentBox

AgentBox is a lightweight multi-agent management platform for running many isolated personal AI agents (Hermes Agent, OpenClaw, etc.) on one personal computer, family server, or small team server.

See [docs/spec.md](docs/spec.md) for the full MVP product and technical specification.

## Status

- Milestone 0 — Project skeleton ✅
- Milestone 1 — Owner / Agent / Settings / Secret CRUD ✅
- Milestone 2 — Podman runtime driver (planned)
- Milestone 3 — Hermes runtime P0 (planned)
- Milestone 4 — Lifecycle, backup, restore, diagnose (planned)
- Milestone 5 — Web Console (planned)
- Milestone 6 — Cross-platform service wrappers (planned)
- Milestone 7 — OpenClaw P1 (planned)

## Repository Layout

```
agentbox/             # Python package
  api/                # FastAPI app + routers
  cli/                # Typer CLI
  core/               # config, paths, ids
  db/                 # SQLAlchemy engine/session
  models/             # ORM models
  schemas/            # Pydantic schemas
  services/           # business logic (no HTTP)
runtimes/
  hermes/             # Hermes Containerfile (P0)
  openclaw/           # OpenClaw Containerfile (P1)
web/                  # React + Vite frontend (Milestone 5)
docs/                 # Specification documents
tests/                # pytest suite
```

## Requirements

- Python 3.10+
- Podman (rootless preferred) — not required for the M0/M1 dev workflow but needed once runtime milestones land
- Node.js 20+ (only for the Web Console in Milestone 5)

AgentBox never depends on Docker Desktop.

## Install (Editable, for Development)

```bash
python -m venv .venv
source .venv/bin/activate
pip install -e ".[dev]"
```

## Configuration

AgentBox stores all state under a single data directory.

| Env var                | Default       | Purpose                                    |
| ---------------------- | ------------- | ------------------------------------------ |
| `AGENTBOX_HOME`        | `~/.agentbox` | Data directory (db, agents, secrets, etc.) |
| `AGENTBOX_HOST`        | `127.0.0.1`   | Bind host for the API server               |
| `AGENTBOX_PORT`        | `8765`        | Bind port for the API server               |
| `AGENTBOX_ADMIN_TOKEN` | _unset_       | Bearer token required by the API           |

When `AGENTBOX_ADMIN_TOKEN` is unset and no `admin_token_hash` is stored, the API runs in single-user dev mode and is reachable only on localhost.

## Quick Start

```bash
# 1. Initialize the data directory and SQLite database
agentbox init

# 2. Configure the platform-shared model provider (one time)
agentbox config set model.provider openrouter
agentbox config set model.default anthropic/claude-sonnet-4
agentbox secret set OPENROUTER_API_KEY     # prompts for value, never echoed

# 3. Create an owner and an agent
agentbox owner create family-member-1 --display-name "Family Member 1"
agentbox agent create family-hermes --owner family-member-1 --runtime hermes

# 4. List
agentbox owner list
agentbox agent list

# 5. Run the HTTP API
agentbox server --host 127.0.0.1 --port 8765
```

Secret values are write-only: they are never printed by the CLI or returned by the API. Only metadata (`name`, `scope`, `exists`, `updated_at`) is visible.

## Running the API in Dev Mode

```bash
# Using the CLI wrapper:
agentbox server --reload

# Or directly with uvicorn:
uvicorn agentbox.api.app:app --host 127.0.0.1 --port 8765 --reload
```

OpenAPI docs are then available at <http://127.0.0.1:8765/docs>.

## Tests

```bash
pytest
```

The test suite uses a temporary `AGENTBOX_HOME` and a per-test SQLite database; running the suite never touches your real `~/.agentbox`.

## Security Notes (MVP)

- Secret values are stored as mode-`0600` files under `<AGENTBOX_HOME>/secrets/`. They are not encrypted at rest yet — this is a known MVP limitation tracked in `docs/spec.md` §12.
- The API is bound to `127.0.0.1` by default. Exposing AgentBox on a LAN requires explicit `--host 0.0.0.0` and setting `AGENTBOX_ADMIN_TOKEN`.
- AgentBox does not mount the host home directory, other agents' data, or any container socket into agent containers.

## License

Apache-2.0 (LICENSE file to be added).
