# MEMORY.md

This repository-level memory records durable product decisions for
`lifepalantir`.

## Durable Decisions

- `lifepalantir` is the master user-facing system.
- `LifeToolSystem`, `TomeofSouls`, `Whattoeat`, and `Vancouver` are subsystems.
- The design direction is Palantir-inspired: operational intelligence, ontology,
  action loops, auditability, and dense decision surfaces.
- The first implementation uses Python stdlib + SQLite + static frontend to keep
  the project portable and easy to inspect.
- The first database is local-only and must not be treated as a cloud production
  system.

## Subsystem Contracts

### LifeToolSystem

Owns life equipment and services: Tesla, sunscreen clothing, socks, underwear,
razor, hospitals, shoes, and other verified high-quality goods and services.

### TomeofSouls

Owns human attributes and personal operating context: body state, identity,
beliefs, goals, health signals, and AI-agent memory.

### Whattoeat

Owns daily food execution: meal count, food selection, quantity, cooking method,
timing, and metabolic outcomes.

### Vancouver

Owns immigration and settlement management: documents, milestones, skills,
finance, city research, and readiness for Vancouver.

## Current Verification Standard

The platform is not done unless the server starts, API health passes, subsystem
data loads, and the browser UI can create a decision that persists in SQLite.
