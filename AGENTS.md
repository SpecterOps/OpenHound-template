# AGENTS.md — openfetch extension pattern documentation

This file documents the **OpenFetch extension pattern**. Every extension (GitHub, Okta, Kubernetes, …) follows the same structure — use this as a template when building a new one. Based on [DLT](https://dlthub.com/docs/intro) and the upstream `openfetch` framework.

---

## Architecture: Three-Phase Pipeline

Every OpenFetch extension exposes the same three CLI phases:

```
collect  →  preproc  →  convert
```

| Phase | Command | What it does                                                                                                              |
|-------|---------|---------------------------------------------------------------------------------------------------------------------------|
| **collect** | `openfetch collect <source> <output_path>` | Hits the upstream API; writes raw data as JSONL to `output/<source>/<table>/`                                             |
| **preproc** | `openfetch preproc <source> <input> lookup.duckdb` | Optional phase: Loads JSONL into DuckDB, runs SQL transforms to build computed tables needed during convert               |
| **convert** | `openfetch convert <source> <input> <output>` | Reads JSONL + Optional DuckDB lookup → emits BloodHound-compatible OpenGraph nodes/edges to `graph/<source>/<table>.json` |

All three phases are registered in `src/<pkg>/main.py` by decorating functions with `@app.collect()`, `@app.preproc()`, `@app.convert()` on an `OpenFetch("<source>")` instance.

Entry point for dev: `uv run src/main.py <phase> <source> ...`

---

## Authentication

Each extension reads credentials from **DLT secrets** (`.dlt/secrets.toml`) under a `[sources.<source>]` section. The extension's `source()` function declares parameters as `dlt.secrets.value` and DLT injects them at runtime.

GitHub example

```toml
[sources.source.github]
client_id = "xxx"
app_id    = "123456"
key_path  = "/path/to/private-key.pem"
org_name  = "my-org"
```

Each configuration or secret can also be configured using environment variables (e.g. `SOURCES__SOURCE__GITHUB__CLIENT_ID`), which is recommended for CI pipelines. Create a `SourceContext` dataclass that carries the authenticated client and any shared state. If a custom authentication flow is required, add a dedicated auth module (`auth.py`). 

---

## Model Pattern (the core convention)

Every collected entity lives in `src/<pkg>/models/<name>.py` and must define **two** things:

### 1. `<Prefix><Name>Properties` — node property dataclass

A `@dataclass` extending the extension's base `NodeProperties` class (e.g. `GHNodeProperties`). Every property must carry `metadata={"description": "..."}` — these become auto-generated documentation.

```python
@dataclass
class GHRepositoryProperties(GHNodeProperties):
    full_name: str = field(default="", metadata={"description": "The fully qualified name (e.g., `org/repo`)."})
    visibility: str | None = field(default=None, metadata={"description": "The visibility level: `public`, `private`, or `internal`."})
```

### 2. `<Name>(BaseAsset)` — the asset class

A Pydantic `BaseAsset` subclass decorated with `@app.asset(node=NodeDef(...), edges=[EdgeDef(...)])`. Must implement two properties:

- **`as_node`** — constructs and returns the typed node; use `self._lookup.*` for cross-table data resolved during convert
- **`edges`** — yields `Edge(kind=..., start=EdgePath(...), end=EdgePath(...))` for every relationship this entity owns

```python
@app.asset(node=NodeDef(kind=nk.REPOSITORY, ...), edges=[EdgeDef(start=nk.ORGANIZATION, end=nk.REPOSITORY, kind=ek.OWNS, ...)])
class Repository(BaseAsset):
    node_id: str
    ...
    @property
    def as_node(self) -> GHNode: ...

    @property
    def edges(self):
        yield Edge(kind=ek.OWNS, start=EdgePath(value=self.owner_id, match_by="id"), ...)
```

> **Node ID rule**: Use a unique combination of properties to generate a unique and reproducable ID or use the source platform's native opaque/global node ID as the OpenGraph node identifier. Never use an integer primary key since these can cause conflicts with other OpenFetch extensions.

See `cookiecutter-templates/source/openfetch_{{ cookiecutter.target_service_slug }}/models/asset.py` as the canonical example.

---

## Node & Edge Kind Constants

All kind strings for an extension live in its `kinds/` package:

- `kinds/nodes.py` — node kind constants, e.g. `REPOSITORY = "GH_Repository"`
- `kinds/edges.py` — edge kind constants, e.g. `OWNS = "GH_Owns"`

Always import from these modules — never hardcode kind strings in model files:

```python
from <pkg>.kinds import nodes as nk, edges as ek
```

For a new extension, prefix all constants with your own two-to-four letter prefix (e.g. `OK_` for Okta, `K8S_` for Kubernetes).

---

## Source Resources (source.py)

`source.py` is the single file that wires up all API collection. Two decorator types:

- `@app.resource(name=..., columns=<Model>)` — top-level paginated collection; receives a `SourceContext`
- `@app.transformer(name=..., columns=<Model>)` — fan-out from a parent resource; first param is one parent item

Chain them with DLT's pipe operator:

```python
repos_resource = repositories(ctx)
repos_resource | environments(ctx)   # environments is a transformer seeded per-repo
```

REST pagination uses `ctx.client` (`RESTClient` with `HeaderLinkPaginator`). For APIs that use cursor-based pagination over a non-standard protocol (e.g. GraphQL), implement a custom paginator (see `helpers.py` → `GraphQLCursorPaginator`).

---

## Optiona; Preproc Transforms

`transforms.py` contains plain DuckDB SQL functions that create computed tables from the raw collected data. They run during `preproc` and their output is what `<Extension>Lookup` queries during `convert`.

```python
def my_computed_table(con, schema: str = "<source>"):
    con.execute(f"CREATE OR REPLACE TABLE {schema}.my_table AS SELECT ...")

def transforms(con, schema):   # this function is passed to @app.preproc(transformer=transforms)
    my_computed_table(con, schema)
```

---

## Lookup (preproc → convert bridge)

Each extension defines a `LookupManager` subclass (e.g. `GithubLookup` in `lookup.py`) that wraps a DuckDB connection. Methods use `@lru_cache` to avoid re-querying for repeated lookups. The lookup is injected into every `BaseAsset` as `self._lookup` during the convert phase.

**`preproc` must run before `convert`** or all lookup calls will return empty/None.

The `preproc` phase function in `main.py` returns a dict mapping DuckDB table names to JSONL table names — only tables listed here are loaded into the lookup DB.

---

## Dev Workflow

```bash
uv sync                        # install all deps incl. dev group
uv run pytest                  # run tests
uv run ruff check src/         # lint
uv run mypy src/               # type-check
uv run zensical serve          # preview docs (uses zensical.toml)
```

Validate output against a known-good baseline:
```bash
uv run scripts/compare_outputs.py <baseline.json> output/splithound/
```

---

## Adding a New Entity — Checklist

1. Create `src/<pkg>/models/<name>.py` with the properties dataclass + `BaseAsset` subclass
2. Add kind constants to `kinds/nodes.py` and/or `kinds/edges.py`
3. Export from `src/<pkg>/models/__init__.py`
4. Add a `@app.resource` or `@app.transformer` function in `source.py`
5. Wire it into the `return (...)` tuple at the bottom of `source()`
6. If cross-table lookups are needed: add a SQL transform in `transforms.py`, register the table in the `preproc` dict in `main.py`, and add a cached query method to the `LookupManager` subclass

---

## Key Files at a Glance

| File | Role |
|------|------|
| `src/<pkg>/main.py` | CLI registration — collect / preproc / convert |
| `src/<pkg>/source.py` | All API resources & transformers |
| `src/<pkg>/auth.py` | Auth flow (token exchange, session management) |
| `src/<pkg>/graph.py` | Extension-specific `Node`, `NodeProperties`, `EdgeProperties` base types |
| `src/<pkg>/transforms.py` | DuckDB SQL transforms run during preproc |
| `src/<pkg>/lookup.py` | `LookupManager` subclass with cached DuckDB queries |
| `src/<pkg>/models/` | One file per entity (properties dataclass + asset class) |
| `src/<pkg>/kinds/` | Node and edge kind string constants |
