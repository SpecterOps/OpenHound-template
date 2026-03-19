from dataclasses import dataclass
from .main import app

from .models.asset import Asset


@dataclass
class SourceContext:
    # Example to add RESTclient to context
    # client: RESTClient
    tenant: str


@app.resource(name="example_assets", parallelized=True, columns=Asset)
def example_assets(ctx: SourceContext):
    """DLT resource, fetches example assets.

    Yields:
        (Asset): The example asset.
    """

    # Example API call, returning individual assets
    # response = ctx.client.get("/example").json()
    # for asset in response["assets"]:
    #     yield asset

    # TODO: Replace with your actual collection logic
    # yield 100 dummy assets as an example
    for num in range(0, 100):
        yield {
            "id": num,
            "name": f"my_asset_{num}",
            "hostname": f"my_hostname_{num}",
            "tenant": ctx.tenant,
            "groups": ["1", "2", "3"],
        }


@app.source(name="{{ cookiecutter.target_service_slug }}", max_table_nesting=0)
def source():
    """DLT source, defines {{ cookiecutter.target_service_slug }} collection resources and transformers.
    Add ctx.config/secret.value to method arguments to force specific config values, ex:

    def source(token=dlt.secrets.value, host=dlt.secrets.value)

    Args:
        token (str): The {{ cookiecutter.target_service_slug }} password used for authentication.
        host (str): The base {{ cookiecutter.target_service_slug }} URL used for API calls.

    Returns:
        (tuple[example_assets]): A tuple of DLT resources/transformers registered for the {{ cookiecutter.target_service_slug }} source.

    """

    ctx = SourceContext(
        # Example restclient
        # client=RESTClient(
        #     base_url=host,
        #     headers={"accept": "application/json"},
        #     auth=BearerTokenAuth(token=token),
        #     paginator=SinglePagePaginator(),
        # ),
        tenant="tenantname",
    )

    return (example_assets(ctx),)
