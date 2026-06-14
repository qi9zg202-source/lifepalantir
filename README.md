# Life Palantir

Life Palantir is the master control system for Summer's life-management projects.
It is designed as the user-facing command layer that coordinates the following
subsystems:

- `LifeToolSystem`: devices, products, services, hospitals, clothes, shoes, and other life equipment decisions.
- `TomeofSouls`: personal ontology, body attributes, long-term goals, identity, values, and AI-agent context.
- `Whattoeat`: daily food, meal count, quantity, cooking method, and metabolic execution.
- `Vancouver`: immigration roadmap, settlement tasks, documents, and Vancouver migration planning.

The product direction follows Palantir-inspired operating-system principles:
ontology first, decision workflows, auditable data, action loops, and a dense
mission-control UI. It does not use Palantir branding or assets.

## Run Locally

```bash
python3 server.py
```

Open:

```text
http://127.0.0.1:8020
```

SQLite database:

```text
data/lifepalantir.sqlite3
```

## Current Scope

This first scaffold includes:

- a Palantir-style command UI;
- a stdlib Python backend;
- SQLite schema and seed data;
- subsystem registry;
- ontology object model;
- decision and action tracking;
- Claude/Codex development rules;
- design and memory documents.

## Repository Layout

```text
.
├── AGENTS.md
├── CLAUDE.md
├── MEMORY.md
├── design.md
├── docs/
│   ├── claudecode-development-standard.md
│   ├── database.md
│   └── palantir-design-standard.md
├── server.py
├── static/
│   ├── app.js
│   └── styles.css
└── data/
    └── .gitkeep
```
