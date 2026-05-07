---
name: openhound
description: Use for all OpenHound collector work, including planning, graph schema, source collection, assets, lookup/preproc, registration, and validation.
---

# OpenHound Skill

Use this skill for any OpenHound collector task.

Before editing collector code:

- Read `.agents/standards/openhound.md`.
- For broad collector work, also read `.agents/standards/workflow.md`.

## Route By Task

| Task | Reference |
|---|---|
| Plan a new collector from API docs, sample responses, or requirements | `references/plan-collector.md` |
| Define graph base classes, common properties, node IDs, or edge properties | `references/graph-schema.md` |
| Register `collect`, `preproc`, `convert`, metadata, or entry points | `references/register-extension.md` |
| Implement API clients, auth, DLT resources, transformers, or secrets | `references/source-collection.md` |
| Add or modify models, node assets, edge assets, kind constants, or exports | `references/add-asset.md` |
| Add DuckDB transforms, lookup methods, lookup registration, or `self._lookup` usage | `references/preproc-lookup.md` |
| Validate collector changes before finishing | `references/validate-extension.md` |

## Routing Rules

- If the task touches multiple areas, read every matching reference.
- If adding or changing collector behavior, always read `references/validate-extension.md` before finishing.
- If the task involves a new collector or broad redesign, start with `references/plan-collector.md`.
- If models use `self._lookup`, also read `references/preproc-lookup.md` and `references/register-extension.md`.
- If adding a new collected resource, usually read `references/source-collection.md`, `references/add-asset.md`, and `references/validate-extension.md`.

## Shared OpenHound Invariants

- Keep exactly one `OpenHound` app instance in `src/<pkg>/main.py`.
- Define kind strings only in `kinds/nodes.py` and `kinds/edges.py`.
- Import kind constants instead of hardcoding kind strings in models.
- Every collector emits one root/environment node.
- Every emitted node sets `environmentid`.
- Node IDs must be stable strings, not raw integer primary keys.
- Every OpenGraph property dataclass field must be documented in the class docstring `Attributes` section.
- Keep `EdgeDef(...)` declarations aligned with the asset that emits the edge.
- Prefer `yield` / `yield from` for edge emission.
- Run available validation checks before completion.
