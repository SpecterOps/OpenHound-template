from collections.abc import Iterator
from typing import Any

from openhound_{{ cookiecutter.target_service_slug }}.main import app
from openhound_{{ cookiecutter.target_service_slug }}.models import Organization
from openhound_{{ cookiecutter.target_service_slug }}.source_context import SourceContext


@app.resource(name="organizations", columns=Organization)
def organization(ctx: SourceContext) -> Iterator[dict[str, Any]]:
    """Yield the single organization returned by this environment's API."""
    for page in ctx.client.paginate("/organization"):
        yield from page
