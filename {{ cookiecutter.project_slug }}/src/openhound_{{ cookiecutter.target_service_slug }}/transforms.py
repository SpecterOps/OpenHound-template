"""Execute SQL preprocessing transformations in their declared order."""

from pathlib import Path

from duckdb import DuckDBPyConnection

SQL_TRANSFORMS_PATH = Path(__file__).parent / "sql"
SQL_TRANSFORMS_FILES = ("10_organization_names.sql",)
SCHEMA_PLACEHOLDER = "__SCHEMA__"


def transforms(
    connection: DuckDBPyConnection,
    schema: str = "{{ cookiecutter.target_service_slug }}",
) -> None:
    """Run packaged SQL files against the internal collector schema."""
    for filename in SQL_TRANSFORMS_FILES:
        query = (
            (SQL_TRANSFORMS_PATH / filename)
            .read_text(encoding="utf-8")
            .replace(SCHEMA_PLACEHOLDER, schema)
        )
        connection.execute(query)
