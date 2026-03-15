from openfetch.core.app import OpenFetch
from openfetch.core.collect import CollectContext
from openfetch.core.convert import ConvertContext
from openfetch.core.lookup import LookupManager
from dlt.extract.source import DltSource

# Initialise the base app, specifying the name of the service and optional help for the CLI.
app = OpenFetch("{{ cookiecutter.target_service_slug }}", help="OpenGraph collector for {{ cookiecutter.target_service_slug }}")


# Register the collection process. The returned value should contain your custom
# DLT source (see source.py)
@app.collect()
def collect(ctx: CollectContext) -> DltSource:
    """Register a Typer CLI command that collects {{ cookiecutter.target_service_slug }} resources and stores them (filtered) on disk.

    Args:
        ctx (CollectContext): Returns DLT pipeline context.
    """
    from openfetch_{{ cookiecutter.target_service_slug }}.source import source as {{ cookiecutter.target_service_slug }}_source

    return {{ cookiecutter.target_service_slug }}_source()

@app.convert()
def convert(ctx: ConvertContext) -> DltSource:
    """Register a Typer CLI command that converts {{ cookiecutter.target_service_slug }} resources to OpenGraph.

    Args:
        ctx (CollectContext): Returns DLT pipeline context.
    """
    from openfetch_{{ cookiecutter.target_service_slug }}.source import source as {{ cookiecutter.target_service_slug }}_source

    return {{ cookiecutter.target_service_slug }}_source(), {}
