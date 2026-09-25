# Contributing

## Development setup

### Install the required tools

Development requires the following tools. Install them with your platform's package manager.

- [uv](https://docs.astral.sh/uv/) — Python and dependency management
- [Git](https://git-scm.com/) — version control
- [DuckDB](https://duckdb.org/) — querying collected data
- [Visual Studio Code](https://code.visualstudio.com/) — recommended editor
- [Node.js](https://nodejs.org/) — only needed to install agent skills

### Clone the repository with submodules

`git clone --recurse-submodules <URL>`

If you already cloned without submodules, run `git submodule update --init`.

### Install agent skills

If you use a coding agent (Claude Code or Codex), install the shared agent skills
(the documentation skills from `og-docs-automation` and the skills from the
OpenHound template).

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

## Browsing the lookup database

Open the local `lookup.duckdb` database in the DuckDB UI:

```bash
duckdb -ui lookup.duckdb
```

## Conventions

- Use type hints to annotate new functions, methods, properties, variables, constants, etc.
- All modules, classes, methods, OpenHound assets, DLT resources, and transformers should have
  concise docstrings, including private ones.
- Comments should explain why code is shaped a certain way, not repeat what the next line does.
  Prefer a named helper over a long explanatory comment when the logic is reused.
