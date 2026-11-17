from dlt.sources.helpers.rest_client import RESTClient
from dlt.sources.helpers.rest_client.paginators import JSONLinkPaginator

from openhound_{{ cookiecutter.target_service_slug }}.auth import BasicCredentials, TokenCredentials


def build_client(credentials: TokenCredentials | BasicCredentials) -> RESTClient:
    """Configure the example API's items/next response pagination settings."""
    return RESTClient(
        base_url=credentials.api_url,
        auth=credentials.auth,
        data_selector="items",
        paginator=JSONLinkPaginator(next_url_path="next"),
    )
