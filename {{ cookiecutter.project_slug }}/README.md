# OpenGraph collector for {{ cookiecutter.target_service }}

This template demonstrates multiple authentication methods, category-based API
collection, and conversion into BloodHound-compatible OpenGraph nodes and edges.
**It targets an example API, not a working {{ cookiecutter.target_service }} integration.**
Replace the endpoints, response models, pagination, authentication options, and
`EX_` graph-kind prefix before collecting a real service.

## Setup

Requires Python 3.13 and [uv](https://docs.astral.sh/uv/).

```console
uv sync --group dev
uv pip install -e .
```

See [CONTRIBUTING.md](CONTRIBUTING.md) for development tools and agent guidance.

## Adapt this template to your service

The Python paths below are relative to `src/openhound_{{ cookiecutter.target_service_slug }}/`.

| Files | What to change |
| --- | --- |
| `auth.py` | Replace the example credentials and authentication adapters with authentication methods supported by your service. |
| `client.py` | Set the API URL, response data selector, and pagination behavior. |
| `resources/`, `source_context.py`, `source.py` | Replace example endpoints and resource categories; pass shared service context to child resources. |
| `models/base.py`, `models/` | Match actual API fields and define the nodes, properties, and relationships to emit. |
| `kinds/`, `graph.py` | Replace the `EX_` prefix and review graph properties and identifiers. |
| `main.py`, `lookup.py`, `transforms.py`, `sql/` | Replace the organization-name enrichment example, or remove preprocessing if unnecessary. Keep phase registration aligned. |
| Project-root `extension.yaml` | Update metadata, credential descriptions, parameters, and references. |
| Project-root `tests/` | Replace JSON samples, FastAPI routes, and assertions with your service's API behavior. |
| Project-root `README.md` | Replace example configuration, permissions, commands, and output descriptions with real usage instructions. |

Changing `api_url` alone does **not** make this a working integration.

## Authentication

Create `~/.dlt/secrets.toml` with **one** of these configurations. Never commit it.

### Bearer token

```toml
[sources.source.{{ cookiecutter.target_service_slug }}.credentials]
api_url = "https://api.example.com"
token = "replace-me"
```

### HTTP basic authentication

```toml
[sources.source.{{ cookiecutter.target_service_slug }}.credentials]
api_url = "https://api.example.com"
username = "replace-me"
password = "replace-me"
```

Only the selected mode's fields are required. Use HTTPS for real services.
Environment variables use the same nested path, for example
`SOURCES__SOURCE__{{ cookiecutter.target_service_slug | upper }}__CREDENTIALS__TOKEN`.

## Collection, preprocessing, and conversion

Optionally configure the collection group in `~/.dlt/config.toml`:

```toml
[sources.source.{{ cookiecutter.target_service_slug }}]
collection = "all" # all, directory, or inventory
```

```console
uv run openhound collect {{ cookiecutter.target_service_slug }} ./collected
uv run openhound preprocess {{ cookiecutter.target_service_slug }} ./collected/{{ cookiecutter.target_service_slug }} ./lookup.duckdb
uv run openhound convert {{ cookiecutter.target_service_slug }} ./collected/{{ cookiecutter.target_service_slug }} ./graph --lookup-file ./lookup.duckdb
```

The example emits one organization root, groups, assets, and asset-to-group
membership edges. Every node's `environmentid` is the root's graph ID.

Run preprocessing before conversion to build `lookup.duckdb` from the collected
organizations. Asset nodes use this lookup for their `organization_name` property;
an unknown organization leaves it unset (`None`).

Preprocessing and conversion read collected files and do not contact the API.

### Example API

All endpoints return `{"items": [...], "next": "https://..."}` and omit `next` on
the last page. The single environment root is used by all child-transformers.

| Endpoint | Required example fields | Raw table |
| --- | --- | --- |
| `/organization` | `id`, `name` (one organization) | `organizations` |
| `/organizations/{id}/groups` | `id`, `name` | `groups` |
| `/organizations/{id}/assets` | `id`, `name`, `hostname`, optional `groups` (group IDs) | `assets` |

This example uses stable, unique, nonempty API string IDs directly for nodes and
membership endpoints.

## Architecture

```text
src/openhound_{{ cookiecutter.target_service_slug }}/
├── main.py                 # Single app and phase registration
├── source.py               # Context creation and resource-group selection
├── auth.py                 # Credential classes and auth adapters
├── client.py               # RESTClient construction and pagination
├── source_context.py       # Shared authenticated collection client
├── resources/
│   ├── organization.py     # Environment root
│   ├── directory/          # Groups and directory resource assembly
│   └── inventory/          # Assets and inventory resource assembly
├── models/                 # Raw validation and node/edge conversion per entity
├── graph.py                # Shared graph types
├── lookup.py               # Cached organization-name lookup
├── transforms.py           # Explicit, ordered SQL-file execution
├── sql/
│   └── 10_organization_names.sql
└── kinds/                  # Node and relationship constants
```
