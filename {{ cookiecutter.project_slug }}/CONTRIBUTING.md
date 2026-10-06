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
