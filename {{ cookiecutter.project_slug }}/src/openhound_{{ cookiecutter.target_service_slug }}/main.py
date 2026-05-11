from openhound.core.app import OpenHound
from openhound.core.collect import CollectContext
from openhound.core.convert import ConvertContext
from openhound.core.lookup import LookupManager
from openhound.core.preproc import PreProcContext
from dlt.extract.source import DltSource
from .transforms import transforms

# Initialise the base app, specifying the name of the service and optional help for the CLI.
# Make sure to replace the source_kind
app = OpenHound("{{ cookiecutter.target_service_slug }}", source_kind="Kind", help="OpenGraph collector for {{ cookiecutter.target_service_slug }}")


# Register the collection process. The returned value should contain your custom
# DLT source (see source.py)
@app.collect()
def collect(ctx: CollectContext) -> DltSource:
    """Register a Typer CLI command that collects {{ cookiecutter.target_service_slug }} resources and stores them (filtered) on disk.

    Args:
        ctx (CollectContext): Returns DLT pipeline context.
    """
    from .source import source as {{ cookiecutter.target_service_slug }}_source

    return {{ cookiecutter.target_service_slug }}_source()



@app.preproc(transformer=transforms)
def preproc(ctx: PreProcContext):
    """Build a DuckDB lookup database from collected data."""
    return {
        "example_assets": "example_assets",
    }


@app.convert()
def convert(ctx: ConvertContext) -> DltSource:
    """Register a Typer CLI command that converts {{ cookiecutter.target_service_slug }} resources to OpenGraph.

    Args:
        ctx (CollectContext): Returns DLT pipeline context.
    """
    from .source import source as {{ cookiecutter.target_service_slug }}_source

    return {{ cookiecutter.target_service_slug }}_source(), {}
