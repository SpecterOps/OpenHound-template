# AGENTS.md - Agent Guidance

This file should always be used as the entrypoint for agents working in this repository. Keep it generic and concise.
Project-specific standards live under `.agents/standards/` and task-specific guidance lives in the relevant skill files
under `.agents/skills/`.

## Before Editing

- Read `CONTRIBUTING.md` for development setup, commands, and this repository's conventions.
- Read `.agents/standards/openhound.md` before making OpenHound collector changes.
- Read `.agents/standards/workflow.md` before developing a new collector or making broad collector changes.
- Load the `openhound` skill from `.agents/skills/openhound/` for task-specific workflows.

## Task Skill

Use `openhound` for all OpenHound collector work. The skill routes tasks to action-specific references.

| Task                                                                                   | Skill       | Reference |
|----------------------------------------------------------------------------------------|-------------|---|
| Plan a new collector from target service requirements or API docs                      | `openhound` | `.agents/skills/openhound/references/plan-collector.md` |
| Add or modify a collected asset/model                                                  | `openhound` | `.agents/skills/openhound/references/add-asset.md` |
| Implement API collection resources, transformers, auth and DLT source wiring           | `openhound` | `.agents/skills/openhound/references/source-collection.md` |
| Define base graph node/edge dataclasses and ID generation behavior                     | `openhound` | `.agents/skills/openhound/references/graph-schema.md` |
| Add DuckDB transforms or lookup methods                                                | `openhound` | `.agents/skills/openhound/references/preproc-lookup.md` |
| Wire phase registration (collect, preproc, convert), metadata, or package entry points | `openhound` | `.agents/skills/openhound/references/register-extension.md` |
| Validate a collector before finishing                                                  | `openhound` | `.agents/skills/openhound/references/validate-extension.md` |

## General Guidance

- Inspect relevant project guidance and existing patterns; reuse suitable code instead of duplicating it.
- Define the intended outcome and proportionate completion checks; keep the work focused and stop when they’re met.
- Prefer the simplest maintainable solution, without speculative features or unrelated changes.
- Meet applicable standards for correctness, security, readability, maintainability, and testing. Validate the result and report evidence and gaps.
- Preserve unrelated user work and local state. Ask when unresolved ambiguity could materially change the solution.
