from collections.abc import Iterator
from typing import Any

from openhound_{{ cookiecutter.target_service_slug }}.main import app
from openhound_{{ cookiecutter.target_service_slug }}.models import Asset, Organization
from openhound_{{ cookiecutter.target_service_slug }}.source_context import SourceContext


@app.transformer(name="assets", columns=Asset)
def assets(
    organization: Organization, ctx: SourceContext
) -> Iterator[dict[str, Any]]:
    """Collect assets and add their environment identifier."""
    for page in ctx.client.paginate(f"/organizations/{organization.id}/assets"):
        for record in page:
            yield {**record, "organization_id": organization.id}
