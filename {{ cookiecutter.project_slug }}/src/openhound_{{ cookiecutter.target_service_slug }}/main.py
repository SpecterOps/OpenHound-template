from typing import Any, cast

from dlt.extract.source import DltSource
from openhound.core.app import OpenHound
from openhound.core.collect import CollectContext
from openhound.core.convert import ConvertContext
from openhound.core.preproc import PreProcContext

from openhound_{{ cookiecutter.target_service_slug }}.kinds import nodes as nk
from openhound_{{ cookiecutter.target_service_slug }}.lookup import CollectorLookup
from openhound_{{ cookiecutter.target_service_slug }}.transforms import transforms

app = OpenHound(
    "{{ cookiecutter.target_service_slug }}",
    source_kind=nk.BASE,
    help="OpenGraph collector for {{ cookiecutter.target_service }}",
)


@app.collect()
def collect(ctx: CollectContext):
    """Collect configured API resources into raw JSONL tables."""
    from openhound_{{ cookiecutter.target_service_slug }}.source import source

    return source()


@app.preproc(transformer=transforms)
def preproc(ctx: PreProcContext) -> dict[str, str]:
    """Load raw organizations before building the SQL lookup table."""
    return {"organizations": "organizations"}


@app.convert(lookup=CollectorLookup)
def convert(ctx: ConvertContext) -> tuple[DltSource, dict[str, Any]]:
    """Convert collected rows and enrich assets with organization names."""
    from openhound_{{ cookiecutter.target_service_slug }}.source import source

    return source()
