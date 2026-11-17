from typing import Literal

import dlt
from dlt.extract.resource import DltResource

from openhound_{{ cookiecutter.target_service_slug }}.auth import BasicCredentials, TokenCredentials
from openhound_{{ cookiecutter.target_service_slug }}.client import build_client
from openhound_{{ cookiecutter.target_service_slug }}.main import app
from openhound_{{ cookiecutter.target_service_slug }}.resources import directory, inventory
from openhound_{{ cookiecutter.target_service_slug }}.resources.organization import organization
from openhound_{{ cookiecutter.target_service_slug }}.source_context import SourceContext


@app.source(name="{{ cookiecutter.target_service_slug }}", max_table_nesting=0)
def source(
    credentials: TokenCredentials | BasicCredentials = dlt.secrets.value,
    collection: Literal["all", "directory", "inventory"] = "all",
) -> tuple[DltResource, ...]:
    """Build clients once and select resource groups without dynamic registration."""
    if collection not in ("all", "directory", "inventory"):
        raise ValueError(f"Unsupported collection mode: {collection}")

    ctx = SourceContext(client=build_client(credentials))
    organization_resource = organization(ctx)
    resources = (
        organization_resource,
        *directory.all_resources(organization_resource, ctx),
    )
    if collection in ("all", "inventory"):
        resources += inventory.all_resources(organization_resource, ctx)
    return resources
