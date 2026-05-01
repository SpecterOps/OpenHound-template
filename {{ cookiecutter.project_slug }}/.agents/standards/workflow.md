# OpenHound Collector Development Workflow

Use this workflow when developing a new OpenHound collector or making broad collector changes. This file describes the order of work only. Implementation details belong in the relevant skill files under `.agents/skills/`.

## Development Flow

1. Understand the target service.
   - Identify credentials, API base URL, pagination model, primary resources, stable IDs, and relationships.
   - Read `.agents/standards/openhound.md` before changing collector code.
   - Use `.agents/skills/openhound-plan-collector/SKILL.md`.

2. Define the collector graph shape.
   - Decide the source prefix, node kinds, edge kinds, common node properties, and node ID strategy.
   - Use `.agents/skills/openhound-graph-schema/SKILL.md`.

3. Register the extension and pipeline phases.
   - Wire `collect`, optional `preproc`, `convert`, extension metadata, and package entry points.
   - Use `.agents/skills/openhound-register-extension/SKILL.md`.

4. Implement source collection.
   - Add or update API clients, source context, DLT resources, transformers, auth, and secrets.
   - Use `.agents/skills/openhound-source-collection/SKILL.md`.

5. Add collected assets and relationships.
   - Add Pydantic asset models, graph property dataclasses, kind constants, exports, `as_node`, and `edges`.
   - Use `.agents/skills/openhound-add-asset/SKILL.md`.

6. Add preprocessing and lookup only when needed.
   - Use this when conversion needs cross-table joins, derived tables, or relationship resolution from collected data.
   - Use `.agents/skills/openhound-preproc-lookup/SKILL.md`.

7. Validate the collector.
   - Check structure, run available tests and static checks, and confirm collect/preproc/convert behavior where possible.
   - Use `.agents/skills/openhound-validate-extension/SKILL.md`.

## Working Rules

- Keep `AGENTS.md` as the entrypoint and `.agents/standards/openhound.md` as the source of OpenHound rules.
- Use a uv virtual environment outside the repository for validation commands to avoid modifying the user's local `.venv`.
