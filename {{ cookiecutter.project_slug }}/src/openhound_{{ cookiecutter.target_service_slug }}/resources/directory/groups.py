from collections.abc import Iterator
from typing import Any

from openhound_{{ cookiecutter.target_service_slug }}.main import app
from openhound_{{ cookiecutter.target_service_slug }}.models import Group, Organization
from openhound_{{ cookiecutter.target_service_slug }}.source_context import SourceContext


@app.transformer(name="groups", columns=Group)
def groups(
    organization: Organization, ctx: SourceContext
) -> Iterator[dict[str, Any]]:
    """Collect groups and add their environment identifier."""
    for page in ctx.client.paginate(f"/organizations/{organization.id}/groups"):
        for record in page:
            yield {**record, "organization_id": organization.id}
