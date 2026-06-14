# Palantir-Inspired Design Standard

This project uses Palantir-inspired design principles, not Palantir branding.

## Product Principles

1. Ontology first.
2. Decisions must connect to evidence and action.
3. Every operation should show owner, state, risk, and next step.
4. The UI should support repeated daily use.
5. Data lineage matters more than decoration.
6. AI recommendations must remain reviewable by the user.

## Layout Pattern

- Left rail for global navigation.
- Command header for mission state.
- Status strip for key system health.
- Main surface split into:
  - subsystem registry;
  - ontology graph;
  - decision queue;
  - action ledger;
  - integration status.

## Visual Pattern

- Light workspace with dark operational rail.
- Thin borders.
- Radius <= 8px.
- Dense rows, not oversized cards.
- Monospace labels for IDs, states, and categories.
- Use color sparingly:
  - teal = live / active;
  - amber = review / pending;
  - red = risk / blocked;
  - blue = reference / evidence.

## Interaction Pattern

- Create decisions quickly.
- Convert decisions into actions.
- Inspect subsystem health.
- Follow links to source repositories.
- Keep state changes auditable.

## Anti-Patterns

- Marketing hero pages.
- Generic wellness illustrations.
- Decorative glowing backgrounds.
- Fake AI chat surfaces without workflow.
- Untraceable recommendations.
- Mixed subsystem data without ownership.
