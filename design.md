# Life Palantir Design

## Product Definition

Life Palantir is a personal operational-intelligence platform. It gives Summer a
single command layer across equipment, body, food, and migration systems.

It is not a notes app, habit tracker, or generic dashboard. It is an operating
system for decisions, goals, assets, evidence, and actions.

## Design Reference

The design follows Palantir-inspired principles from public product positioning:

- enterprise operating system;
- ontology-centered data model;
- human-AI decision loops;
- operational workflows;
- secure, auditable action;
- integration across multiple systems.

This project must not copy Palantir logos, trademarks, proprietary visuals, or
private implementation details.

## UX Standard

The UI should feel like:

- a command center;
- an operational map;
- an evidence-backed decision surface;
- a control plane for subsystems.

The UI should not feel like:

- a consumer landing page;
- a wellness blog;
- a card-only dashboard template;
- a decorative dark-mode mockup.

## First Screen

The first screen must show:

- master system name;
- mission state;
- subsystem health;
- live decisions;
- next actions;
- ontology map.

## Visual Rules

- dark left rail;
- light workspace;
- low-radius panels;
- dense but readable layout;
- strong table and row design;
- restrained blue/teal/amber accents;
- monospaced labels for system states and identifiers;
- no oversized marketing hero;
- no fake metrics without seeded backing data.

## Data Model

Core objects:

- subsystem;
- ontology object;
- signal;
- decision;
- action item;
- integration;
- audit event.

## Delivery Phases

### Phase 1: Local Scaffold

- SQLite schema.
- Seed subsystem registry.
- Master dashboard.
- Decision creation.
- Action tracking.
- Development docs.

### Phase 2: Real Subsystem Integration

- import current repo metadata;
- map each subsystem to ontology objects;
- pull real documents and plans;
- add manual sync controls.

### Phase 3: Agentic Execution

- AI-agent task routing;
- recommendation review;
- action approval;
- recurring audits;
- goal-risk forecasting.

## Product Strategy & Competitiveness Analysis Report Standard

The project document set must include `Product Strategy & Competitiveness Analysis产品战略与竞争力分析报告.html`. This artifact is the canonical place for product strategy and competitiveness analysis. Until a real analysis is authored, an empty HTML placeholder with the exact standard filename is acceptable, but it must be visible from the project README.
