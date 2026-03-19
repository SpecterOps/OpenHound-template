from functools import lru_cache

from duckdb import DuckDBPyConnection
from openhound.core.lookup import LookupManager


class {{ cookiecutter.target_service_slug }}Lookup(LookupManager):
    def __init__(self, client: DuckDBPyConnection, schema: str = "{{ cookiecutter.target_service_slug }}"):
        super().__init__(client, schema)
        self.schema = schema
        self.client = client

    @lru_cache
    def one_single_item(self) -> str | None:
        """ An example to fetch 1 single item"""
        res = self._find_single_object(
            f"""SELECT node_id FROM {self.schema}.organizations"""
        )
        return res

    @lru_cache
    def all_items(self, my_filter: str):
        """ An example to fetch multiple items with a query filter"""
        return self.find_all_objects(
            f"""SELECT node_id FROM {self.schema}.applications WHERE some_filter = ?""",
            [my_filter],
        )
