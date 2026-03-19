import duckdb

def create_joined_tables(con, schema: str = "{{ cookiecutter.target_service_slug }}"):
    """ Example to create another table. In this case, just an example of creating a single table out of two tables using union"""
    con.execute(f"""CREATE OR REPLACE TABLE {schema}.new_table AS 
        SELECT * FROM {schema}.example_assets
        UNION ALL
        SELECT * FROM {schema}.example_assets
    """)


def transforms(con: duckdb.DuckDBPyConnection, schema: str = "{{ cookiecutter.target_service_slug }}") -> None:
    """Apply all preprocessing transformations to the DuckDB lookup database.

    Args:
        con: The DuckDB connection to use for creating computed tables.
        schema: The DuckDB schema name containing the source tables.
    """
    create_joined_tables(con, schema)
