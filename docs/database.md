# Database Design

SQLite file:

```text
data/lifepalantir.sqlite3
```

## Tables

### subsystems

Master registry of the four life-management subsystems.

Fields:

- `id`
- `name`
- `repo_url`
- `domain`
- `mission`
- `status`
- `priority`
- `owner`
- `created_at`
- `updated_at`

### ontology_objects

Objects managed by the life ontology.

Fields:

- `id`
- `subsystem_id`
- `object_type`
- `name`
- `description`
- `state`
- `confidence`
- `source_ref`
- `created_at`
- `updated_at`

### signals

Evidence and metrics flowing into the platform.

Fields:

- `id`
- `subsystem_id`
- `object_id`
- `signal_type`
- `name`
- `value`
- `unit`
- `recorded_at`
- `source_ref`

### decisions

Decision records created by the user or an agent.

Fields:

- `id`
- `title`
- `subsystem_id`
- `decision_type`
- `rationale`
- `status`
- `confidence`
- `impact`
- `next_action`
- `created_at`
- `updated_at`

### action_items

Execution tasks linked to decisions or subsystems.

Fields:

- `id`
- `decision_id`
- `subsystem_id`
- `title`
- `owner`
- `status`
- `due_date`
- `created_at`
- `updated_at`

### integrations

External systems and repositories.

Fields:

- `id`
- `subsystem_id`
- `name`
- `kind`
- `endpoint`
- `status`
- `last_checked_at`

### audit_events

Trace of state changes.

Fields:

- `id`
- `actor`
- `event_type`
- `entity_type`
- `entity_id`
- `summary`
- `created_at`
