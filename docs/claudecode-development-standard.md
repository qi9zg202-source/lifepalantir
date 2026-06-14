# Claude Code Development Standard

## Objective

Agents working in this repository must produce finished, verified work, not
partial drafts.

## Required Flow

1. Read local instructions.
2. Inspect current repo state.
3. Define done criteria.
4. Make focused changes.
5. Run verification.
6. Report only confirmed results.

## Done Criteria

For app changes:

- server starts;
- API health passes;
- homepage renders;
- key interaction works;
- persistence is verified;
- docs match implementation.

For design changes:

- visual system stays consistent;
- desktop and mobile layouts are checked;
- no horizontal overflow;
- no placeholder language unless clearly marked as future work.

## Forbidden

- Do not overwrite user work.
- Do not claim success without verification.
- Do not introduce secrets.
- Do not copy third-party branding assets.
- Do not leave debug files or screenshots in the repo.
