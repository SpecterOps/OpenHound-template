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

    # Test which resource group to collect
    if collection not in ("all", "directory", "inventory"):
        raise ValueError(f"Unsupported collection mode: {collection}")


    # Set the source context with a REST client to be used by our resources
    ctx = SourceContext(client=build_client(credentials))

    # Define the root organization resource that is used for input for child resources
    organization_resource = organization(ctx)

    # By default, always collect the organization resource and directory resources
    resources = (
        organization_resource,
        *directory.all_resources(organization_resource, ctx),
    )

    # If collection type is all or inventory, also add our inventory resources
    if collection in ("all", "inventory"):
        resources += inventory.all_resources(organization_resource, ctx)

    # Return all resources we want to collect
    return resources
