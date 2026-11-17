from dataclasses import dataclass

from dlt.sources.helpers.rest_client import RESTClient


@dataclass
class SourceContext:
    """Authenticated client shared by explicitly defined resources."""

    client: RESTClient
