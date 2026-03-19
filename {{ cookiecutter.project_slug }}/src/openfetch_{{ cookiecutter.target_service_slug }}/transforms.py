import duckdb

def create_joined_tables(con, schema: str = "{{ cookiecutter.target_service_slug }}"):
    """ Example to create joined tables."""
    con.execute(f"""CREATE OR REPLACE TABLE ....""")


def transforms(con: duckdb.DuckDBPyConnection, schema: str = "{{ cookiecutter.target_service_slug }}") -> None:
    """Apply all preprocessing transformations to the DuckDB lookup database.

    Args:
        con: The DuckDB connection to use for creating computed tables.
        schema: The DuckDB schema name containing the source tables.
    """
    create_joined_tables(con, schema)
