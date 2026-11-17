# Contributing

## Development setup

### Install the required tools

Development requires the following tools. Install them with your platform's package manager.

- [uv](https://docs.astral.sh/uv/) — Python and dependency management
- [Git](https://git-scm.com/) — version control
- [DuckDB](https://duckdb.org/) — querying collected data
- [Visual Studio Code](https://code.visualstudio.com/) — recommended editor

### Optional OG docs tooling

The OG docs automation submodule uses PowerShell scripts. Install PowerShell
5.1+ only if you generate or validate docs; custom icon rendering requires
PowerShell 7+. On PowerShell 7+, run scripts with `pwsh`; on Windows PowerShell
5.1, use `powershell`.

### Clone the repository with submodules

Clone the repository with its URL:

```bash
git clone --recurse-submodules <repository-url>
```

If you already cloned without submodules, run `git submodule update --init --recursive`.

When setting up a newly generated project in Git, register the OG docs automation submodule before the first commit:

```bash
git submodule add https://github.com/SpecterOps/og-docs-automation.git docs/og-docs-automation
```

### Install OpenHound agent skills

Use the
[`skills` npm package](https://github.com/vercel-labs/skills) to install and manage skills for your coding agent.

```bash
npx skills add SpecterOps/skills/plugins/bloodhound/skills/openhound-development
```

### Install Python dependencies

uv downloads the required Python version and creates the virtual environment automatically:

```bash
uv sync --group dev
```

### Enable pre-commit hooks

Enable the repository's pre-commit hooks so lint issues are caught before you push:

```bash
uv run pre-commit install
```

The hooks run Mypy over `src/` when source files or `pyproject.toml` change. To
run the same type check directly:

```bash
uv run mypy
```

## Collector development

If you use a coding agent, use the `openhound` development skill for collector
architecture and implementation guidance. Installation instructions are above.

See the [README's architecture overview](README.md#architecture) for the project layout.

### SQL transformations

- Register SQL files in `SQL_TRANSFORMS_FILES` in `transforms.py`, in execution order.
- Use `__SCHEMA__` for the collector schema.
- Include required raw tables in the preprocessing map in `main.py`.

## Validation

Run these checks before submitting changes:

```console
uv run pytest
uv run ruff check src tests
uv run mypy
```

Mock API calls and use test-only credentials. Tests must not
require live services or expose secrets.

The HTTP integration fixtures in `tests/conftest.py` route DLT requests
through FastAPI's `TestClient`, using sample responses in `tests/test_data/api/`.
The test functions cover multiple auth modes, JSON pagination, shared parent pipes,
and DLT model validation with the real collector client. No server process or
network access is needed; requests to other hosts are rejected.
Add routes and samples as the collector grows.

## Browsing the lookup database

After preprocessing, open the local `lookup.duckdb` database in the DuckDB UI:

```bash
duckdb -ui lookup.duckdb
```

## Conventions

- Use type hints to annotate new functions, methods, properties, variables, constants, etc.
- All modules, classes, methods, OpenHound assets, DLT resources, and transformers should have
  concise docstrings, including private ones.
- Comments should explain why code is shaped a certain way, not repeat what the next line does.
  Prefer a named helper over a long explanatory comment when the logic is reused.
