# AGENTS.md — OpenHound extension pattern documentation

This file documents the **OpenHound extension pattern**. Every extension (GitHub, Okta, Kubernetes, …) follows the same structure. Use this as a template when building a new one. Based on [DLT](https://dlthub.com/docs/intro) and the upstream `openhound` framework.

---

## Naming Conventions

Derive a **short uppercase prefix** from the service slug (two to four letters). Use it consistently across all class names and kind strings.

| Cookiecutter slug | Prefix | Example class | Example kind constant |
|---|---|---|---|
| `okta` | `OK` | `OKNode`, `OKNodeProperties` | `ASSET = "OK_Asset"` |
| `github` | `GH` | `GHNode`, `GHNodeProperties` | `REPO = "GH_Repository"` |
| `kubernetes` | `K8S` | `K8SNode`, `K8SNodeProperties` | `POD = "K8S_Pod"` |

Pattern: `<PREFIX>NodeProperties`, `<PREFIX>Node`, `<PREFIX>EdgeProperties`, `<PREFIX>Lookup`.

---

## Architecture: Three-Phase Pipeline

Every OpenHound extension exposes the same three CLI phases:

```
collect  →  preproc  →  convert
```

| Phase | Command | What it does                                                                                                       |
|-------|---------|--------------------------------------------------------------------------------------------------------------------|
| **collect** | `openhound collect <source> <output_path>` | Collects data from the upstream API; writes raw data as JSONL to `output/<source>/<table>/`                        |
| **preproc** | `openhound preproc <source> <input> lookup.duckdb` | Optional: Loads JSONL into DuckDB, runs SQL transforms to build computed tables needed during convert              |
| **convert** | `openhound convert <source> <input> <output>` | Reads JSONL + DuckDB lookup and emits BloodHound-compatible OpenGraph nodes/edges to `graph/<source>/<table>.json` |

All three phases are registered in `src/<pkg>/main.py` by decorating functions with `@app.collect()`, `@app.preproc()`, `@app.convert()` on an `OpenHound("<source>")` instance.

Entry point for dev: `uv run src/main.py <phase> <source> ...`

---

## Authentication

Each extension reads credentials from **DLT secrets** (`.dlt/secrets.toml`) under a `[sources.<source>]` section. The extension's `source()` function declares parameters as `dlt.secrets.value` and DLT injects them at runtime.

```toml
[sources.source.myservice]
token    = "xxx"
host     = "https://api.myservice.com"
org_name = "my-org"
```

Each value can also be set via environment variables (e.g. `SOURCES__SOURCE__MYSERVICE__TOKEN`), which is recommended for CI pipelines. Create a `SourceContext` dataclass that carries the authenticated client and any shared state. If a custom authentication flow is required, add a dedicated auth module (`auth.py`).

---

## Graph Types (`graph.py`)

`graph.py` defines the extension's dataclass types for nodes, node properties, and edge properties. These are used throughout `models/` and `lookup.py`.

### `<Slug>NodeProperties` — shared node property dataclass

A `@dataclass` extending `BaseProperties` (imported from `openhound.core.models.entries_dataclass`). Add fields that **every node** in this extension must include. Every field must include `metadata={"description": "..."}`, these become auto-generated documentation.

### `<Slug>Node` — node class

A `@dataclass` extending `BaseNode`. Sets `self.id` in `__post_init__` using a property from the node properties. Use the platform's native opaque/global node ID where available, never use a raw integer primary key since these can cause ID collisions across extensions. In some cases, services may not include unique IDs for all resources. A self-generated ID based on stable properties is also acceptable and sometimes preferred for reproducibility. These can be generated via `BaseNode.guid(propert1, propert2, propertie3)`, where BaseNode.guid accepts any number of arguments to generate a GUID.

### `<Slug>EdgeProperties` — edge property dataclass

A `@dataclass` extending `EdgeProperties`. Add fields shared across edges in this extension.

Full `graph.py` example:

```python
from dataclasses import dataclass, field
from openhound.core.models.entries_dataclass import EdgeProperties
from openhound.core.models.entries_dataclass import Node as BaseNode
from openhound.core.models.entries_dataclass import NodeProperties as BaseProperties


@dataclass
class EXNodeProperties(BaseProperties):
    node_id: str = field(metadata={"description": "The platform's native unique identifier."})


@dataclass
class EXNode(BaseNode):
    properties: EXNodeProperties
    kinds: list[str]
    id: str = field(init=False)

    def __post_init__(self):
        # Derive the OpenGraph node id from the platform's native identifier.
        self.id = self.properties.node_id


@dataclass
class EXEdgeProperties(EdgeProperties):
    reason: str | None = None
```

---

## Node & Edge Kind Constants

All kind strings for an extension live in the `kinds/` directory:

- `kinds/nodes.py` — node kind constants, e.g. `ASSET = "EX_Asset"`
- `kinds/edges.py` — edge kind constants, e.g. `MEMBER_OF = "EX_MemberOf"`

Always import from these modules — never hardcode kind strings in model files:

```python
from openhound_<pkg>.kinds import nodes as nk, edges as ek
```

For a new extension, prefix all constants with your own two-to-four letter prefix (e.g. `OK_` for Okta, `K8S_` for Kubernetes).

---

## Model Pattern (the core convention)

Every collected entity lives in `src/<pkg>/models/<name>.py` and must define **two** things:

### 1. `<Name>Properties` — entity-specific property dataclass

A `@dataclass` extending the extension's base `<Slug>NodeProperties`. Add fields unique to this entity. Every field must carry `metadata={"description": "..."}`.

For optional fields, prefer explicit nullable types with `None` defaults over placeholder empty strings when the value may be absent. This applies especially to auto-generated documentation fields such as `query_*` helpers and relational metadata:

```python
query_repositories: str | None = None
environment_name: str | None = None
group_name: str | None = field(
    default=None, metadata={"description": "The runner group display name."}
)
```

This keeps the schema honest and produces better auto documentation than using `""` as a sentinel for "not present".

```python
@dataclass
class AssetProperties(EXNodeProperties):
    hostname: str = field(metadata={"description": "The hostname of the asset."})
```

### 2. `<Name>(BaseAsset)` — the asset class

A Pydantic `BaseAsset` subclass decorated with `@app.asset(node=NodeDef(...), edges=[EdgeDef(...)])`. Note: `BaseAsset` is Pydantic; the properties classes (`<Name>Properties`) are plain dataclasses. The raw fields on `BaseAsset` mirror the collected JSONL schema. Must implement two properties:

- **`as_node`** — constructs the OpenGraph node from `self`; call `self._lookup.<method>()` to resolve cross-table data loaded during `preproc`
- **`edges`** — yields `Edge(kind=..., start=EdgePath(...), end=EdgePath(...))` for every edge this entity can generate. Conditional edges are common here and may use `self._lookup` as well.

```python
from dataclasses import dataclass, field
from openhound.core.asset import BaseAsset, EdgeDef, NodeDef
from openhound.core.models.entries import Edge, EdgePath
from openhound_<pkg>.graph import EXNodeProperties, EXNode
from openhound_<pkg>.kinds import nodes as nk, edges as ek
from openhound_<pkg>.main import app


@dataclass
class AssetProperties(EXNodeProperties):
    hostname: str = field(metadata={"description": "The hostname of the asset."})


@app.asset(
    node=NodeDef(kind=nk.ASSET, description="Example Asset", icon="cog"),
    edges=[EdgeDef(start=nk.ASSET, end=nk.GROUP, kind=ek.MEMBER_OF, description="Asset belongs to group")]
)
class Asset(BaseAsset):
    id: int          # raw field from collected JSONL
    name: str
    hostname: str
    groups: list[str]

    @property
    def as_node(self) -> EXNode:
        properties = AssetProperties(
            node_id=str(self.id), name=self.name, displayname=self.name, hostname=self.hostname
        )
        return EXNode(properties=properties, kinds=[nk.ASSET])

    @property
    def edges(self):
        for group in self.groups:
            yield Edge(
                kind=ek.MEMBER_OF,
                start=EdgePath(value=self.as_node.id, match_by="id"),
                end=EdgePath(value=group, match_by="id"),
            )
```

### Edge definition / emission alignment

Only declare `EdgeDef(...)` entries on the asset class that actually emits those edges in its `edges` property.

- If a node-bearing asset only creates the node, keep it as `@app.asset(node=NodeDef(...))` and return no edges.
- If relationships are modeled by a separate edge-only asset, put the `EdgeDef(...)` declarations on that edge-only asset instead.

This keeps auto-generated edge documentation aligned with the real emitter.

### Prefer yielding edges over building lists

Prefer generators (`yield` / `yield from`) for `edges` and edge helper properties instead of accumulating arrays and returning them. This is the standard pattern in the upstream changes and keeps edge composition readable:

```python
@property
def _contains_edge(self):
    yield Edge(...)

@property
def _access_edges(self):
    for target_id in self.target_ids:
        yield Edge(...)

@property
def edges(self):
    yield from self._access_edges
    yield from self._contains_edge
```

This is preferred over building `edges = []`, appending/extending, and returning the array.

**Using `self._lookup` in `as_node`**: when the node needs data from a different collected table (e.g. resolving a parent org ID), call the lookup manager:

```python
@property
def as_node(self) -> EXNode:
    org_node_id = self._lookup.org_id_for(self.org_name)  # resolved from DuckDB
    properties = AssetProperties(node_id=str(self.id), ..., org_id=org_node_id)
    return EXNode(properties=properties, kinds=[nk.ASSET])
```

> **Node ID rule**: Use the platform's native ID if possible, or derived from a stable combination of properties. Never use a raw integer primary key, these cause ID collisions across extensions.

See `cookiecutter-templates/source/{{ cookiecutter.project_slug }}/src/openhound_{{ cookiecutter.target_service_slug }}/models/asset.py` as the example.

---

## Source Resources (`source.py`)

`source.py` wires up all API collection using openhound decorators. Two decorator types:

- `@app.resource(name=..., columns=<Model>)` — Top level collection; receives a `SourceContext`. The `columns` parameter sets the `BaseAsset` subclass used to validate each yielded row.
- `@app.transformer(name=..., columns=<Model>)` —  first param contains the parent item yielded by the resource; second param is a `SourceContext`. Use for nested collection that depends on parent resources (e.g. collecting group memberships per user).

Chain them with DLT's pipe operator:

```python
repos_resource = repositories(ctx)
repos_resource | environments(ctx)   # environments is a transformer seeded per-repo
```

Wrap them in a `@dlt.source(name="<source>", max_table_nesting=0)` function that builds a `SourceContext` and returns a tuple of resources. Credentials are declared as `dlt.secrets.value` parameters on the source function:

```python
import dlt
from dataclasses import dataclass
from dlt.sources.rest_api import RESTClient, HeaderLinkPaginator
from dlt.sources.rest_api.auth import BearerTokenAuth
from openhound_<pkg>.models.import Asset
from openhound_<pkg>.models import AssetUser

@dataclass
class SourceContext:
    client: RESTClient


@app.resource(name="assets", parallelized=True, columns=Asset)
def assets(ctx: SourceContext):
    for item in ctx.client.paginate("/assets"):
        yield item

@app.transformer(name="asset_users", parallelized=True, columns=AssetUser)
def asset_users(asset, ctx: SourceContext):
    for item in ctx.client.paginate(f"/assets/{asset.id}/users"):
        yield item

@app.source(name="myservice", max_table_nesting=0)
def source(token=dlt.secrets.value, host=dlt.secrets.value):
    ctx = SourceContext(
        client=RESTClient(
            base_url=host,
            auth=BearerTokenAuth(token=token),
            paginator=HeaderLinkPaginator(),
        )
    )
    asset_resource = assets(ctx)
    return (
        asset_resource,
        asset_resource | asset_users(ctx),  # pipe operator seeds asset_users with each asset
    )
```
---

## Preproc Transforms (`transforms.py`)

`transforms.py` contains plain DuckDB SQL functions that create computed tables from the raw collected data. They run during `preproc` and their output is what the `LookupManager` subclass queries during `convert`.

```python
def create_joined_tables(con, schema: str = "myservice"):
    con.execute(f"CREATE OR REPLACE TABLE {schema}.my_table AS SELECT ...")

def transforms(con: duckdb.DuckDBPyConnection, schema: str = "myservice") -> None:
    create_joined_tables(con, schema)
```

The top-level `transforms` function is passed to `@app.preproc(transformer=transforms)` in `main.py`. Note, adding a transformer to preproc is entirely optional.

---

## Lookup (`preproc` → `convert` bridge)

Each extension defines a `LookupManager` subclass (e.g. `EXLookup` in `lookup.py`) that wraps a DuckDB connection. Methods use `@lru_cache` to avoid re-querying for repeated lookups. The lookup is injected into every `BaseAsset` as `self._lookup` during the convert phase.

**`preproc` must run before `convert`** or all lookup calls will return empty/None.

```python
class EXLookup(LookupManager):
    @lru_cache
    def group_id_for(self, name: str) -> str | None:
        return self._find_single_object(
            f"SELECT node_id FROM {self.schema}.groups WHERE name = ?", [name]
        )
```

The `preproc` function in `main.py` returns a dict, mapping resource names to DuckDB table names. Only tables listed here are loaded into the lookup DB.

---

## `main.py` — Phase Registration

`main.py` creates the `app` instance and registers the three phases. It is the entry point imported by model files (`from openhound_<pkg>.main import app`).

```python
from openhound.core.app import OpenHound
from openhound.core.collect import CollectContext
from openhound.core.convert import ConvertContext
from openhound.core.preproc import PreProcContext
from dlt.extract.source import DltSource
from .transforms import transforms

app = OpenHound("myservice", help="OpenGraph collector for MyService")


@app.collect()
def collect(ctx: CollectContext) -> DltSource:
    from .source import source as myservice_source
    return myservice_source()


@app.preproc(transformer=transforms)
def preproc(ctx: PreProcContext) -> dict[str, str]:
    # Maps DuckDB table name → JSONL table name.
    # Only tables listed here are loaded into the lookup DB.
    return {
        "assets": "assets",
    }


@app.convert(lookup=EXLookup)
def convert(ctx: ConvertContext) -> DltSource:
    from .source import source as myservice_source
    # Second element is a dict with additional static data that can be used by an Asset via self._extras["key"]
    # the (optional) lookup is injected as self._lookup on every Asset, so it can be used in as_node and edges properties to resolve cross-table relationships.
    return myservice_source(), {}
```

---

## Extension Metadata Files

A YAML file should be configured for extension discovery and registration:

### `extension.yaml`

Declares the extension's identity, credentials, and parameters for the OpenHound registry:

```yaml
name: myservice
version: 0.1.0
type: local
credentials:
  - name: token
    description: API token
    required: true
parameters:
  - name: org
    description: Organisation slug
    required: true
```

---

## Dev Workflow

```bash
uv sync                # install all deps incl. dev group
uv run pytest          # run tests
uv run ruff check src/ # lint
uv run mypy src/       # type-check
```

---

## Rules / Anti-patterns

| Don't | Do instead |
|---|---|
| Hardcode kind strings (`"EX_Asset"`) in model files | Import from `kinds/nodes.py` and `kinds/edges.py` |
| Use `id: int` as the OpenGraph node identifier | Set `self.id` in `__post_init__` from a stable string property |
| Call `self._lookup` methods in `convert` without running `preproc` first | Always run `preproc` before `convert`; document this in the extension README |
| Add fields to `<Slug>NodeProperties` without `metadata={"description": "..."}` | Every property field must carry a description |
| Import `app` from anywhere other than `openhound_<pkg>.main` | Keep one `app` instance per extension, always in `main.py` |
| Define node or edge kind strings outside `kinds/` | All kind strings belong in `kinds/nodes.py` or `kinds/edges.py` |

---

## Adding a New Entity — Checklist

1. Create `src/<pkg>/models/<name>.py` with the properties dataclass + `BaseAsset` subclass
2. Add kind constants to `kinds/nodes.py` and/or `kinds/edges.py`
3. Export from `src/<pkg>/models/__init__.py`
4. Add a `@dlt.resource` or `@dlt.transformer` function in `source.py`
5. Wire it into the `return (...)` tuple at the bottom of `source()`
6. If cross-table lookups are needed: add a SQL transform in `transforms.py`, register the table in the `preproc` dict in `main.py` and add a cached query method to the `LookupManager` subclass

---

## Key Files

| File | Role                                                                      |
|------|---------------------------------------------------------------------------|
| `src/<pkg>/main.py` | CLI registration — collect / preproc / convert; owns the `app` instance   |
| `src/<pkg>/source.py` | All OpenHound/DLT resources & transformers                                |
| `src/<pkg>/graph.py` | Extension-specific `Node`, `NodeProperties`, `EdgeProperties` dataclasses |
| `src/<pkg>/transforms.py` | DuckDB SQL transforms run during preproc                                  |
| `src/<pkg>/lookup.py` | `LookupManager` subclass with cached DuckDB queries                       |
| `src/<pkg>/models/` | One file per entity (properties dataclass + asset class)                  |
| `src/<pkg>/kinds/` | Node and edge kind string constants                                       |
| `extension.yaml` | Extension metadata, credentials, and parameters                           |
