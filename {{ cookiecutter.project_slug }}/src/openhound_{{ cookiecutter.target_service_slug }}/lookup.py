from functools import lru_cache

from duckdb import DuckDBPyConnection
from openhound.core.lookup import LookupManager


class CollectorLookup(LookupManager):
    def __init__(
        self,
        client: DuckDBPyConnection,
        schema: str = "{{ cookiecutter.target_service_slug }}",
    ) -> None:
        """Bind lookup queries to the preprocessed collector schema."""
        super().__init__(client, schema)

    @lru_cache  # noqa: B019 - Bounded lookup cache shared during conversion.
    def organization_name(self, organization_id: str) -> str | None:
        """Return the collected organization name, or None for an unknown ID."""
        return self._find_single_object(
            f"SELECT name FROM {self.schema}.organization_names WHERE id = ?",
            [organization_id],
        )
