from dlt.extract.resource import DltResource

from openhound_{{ cookiecutter.target_service_slug }}.resources.inventory.assets import assets
from openhound_{{ cookiecutter.target_service_slug }}.source_context import SourceContext


def all_resources(root: DltResource, ctx: SourceContext) -> tuple[DltResource, ...]:
    return (root | assets(ctx),)
