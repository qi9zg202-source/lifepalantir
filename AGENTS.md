# Agent Instructions

This repository is the master orchestration layer for Summer's life-management
systems. Work in this repo must be direct, verifiable, and product-oriented.

## Communication

Final reports to the user must be plain, clear English or Chinese, depending on
the user's latest language. Avoid implementation jargon unless the user asks for
details.

## Work Standard

- Verify before reporting completion.
- Prefer small, testable changes.
- Keep `lifepalantir` as the master system; do not bury master navigation inside a subsystem.
- Do not copy Palantir trademarks, logos, or proprietary assets.
- Use Palantir-inspired principles: ontology, operational workflows, audit trail, permission-aware design, and action loops.
- Preserve subsystem boundaries:
  - `LifeToolSystem` = life equipment and services.
  - `TomeofSouls` = personal attributes, identity, goals, AI-agent context.
  - `Whattoeat` = daily food execution.
  - `Vancouver` = immigration and settlement.

## Verification Checklist

Before saying done, run:

```bash
python3 -m py_compile server.py
python3 server.py
```

Then verify:

- `GET /api/health` returns ok.
- `GET /api/bootstrap` returns all four subsystems.
- the homepage opens in a browser.
- creating a decision writes to SQLite and is visible after reload.

## File Rules

- Keep docs current when changing architecture.
- Keep database schema documented in `docs/database.md`.
- Keep UI rules documented in `docs/palantir-design-standard.md`.
- Keep Claude/Codex rules documented in `CLAUDE.md` and `docs/claudecode-development-standard.md`.
