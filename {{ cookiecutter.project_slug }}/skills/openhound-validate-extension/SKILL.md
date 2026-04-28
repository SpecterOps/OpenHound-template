---
name: openhound-validate-extension
description: Use before finishing OpenHound collector changes to run tests, linting, type checks, and structural sanity checks.
---

# OpenHound Validate Extension Skill

Use this skill before finishing changes to an OpenHound collector.

## Structural Checks

Review these before finishing:

- Kind strings are defined only in `kinds/nodes.py` and `kinds/edges.py`.
- Model files import kind constants instead of hardcoding strings.
- Node IDs are stable strings and not raw integer primary keys.
- Every OpenGraph property dataclass field includes docstrings with attribute description metadata.
- `EdgeDef(...)` declarations match edges actually yielded by the same asset class.
- Edge properties use `yield` or `yield from` unless a list is explicitly justified.
- Models using `self._lookup` have `@app.convert(lookup=...)` registered.
- Tables required by lookup methods are included in the `preproc` map or created by transforms.
- `source.py` credentials are declared with `dlt.secrets.value`.
- `extension.yaml` credentials and parameters match the source function inputs.
- `models/__init__.py` exports newly added models.

## Common Anti-Patterns

| Do not | Prefer |
|---|---|
| Hardcode `"EX_Asset"` in a model | Import `nk.ASSET` or `ek.RELATIONSHIP` from `kinds/`. |
| Use `id: int` as the OpenGraph node ID | Assign `self.id` from a stable string property or `BaseNode.guid(...)`. |
| Call `self._lookup` without preproc data | Register lookup and load or transform the required tables. |
| Add dataclass fields without descriptions | Add `metadata={"description": "..."}`. |
| Create multiple `OpenHound` app instances | Keep one app in `main.py`. |
| Declare edges on a different asset than the emitter | Put `EdgeDef(...)` on the emitting asset. |


## Final Response Guidance

When reporting completion, include:

- What nodes/edges are added or modified.
- What changes are made to the collection pipeline.
- Any other relevant changes.
- Any remaining risks or follow-up work.
