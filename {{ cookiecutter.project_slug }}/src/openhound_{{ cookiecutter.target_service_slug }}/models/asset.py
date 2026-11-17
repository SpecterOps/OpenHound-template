from collections.abc import Iterator
from dataclasses import dataclass

from openhound.core.asset import EdgeDef, NodeDef
from openhound.core.models.entries import Edge, EdgePath
from pydantic import Field

from openhound_{{ cookiecutter.target_service_slug }}.graph import (
    CollectorNode,
    CollectorNodeProperties,
)
from openhound_{{ cookiecutter.target_service_slug }}.kinds import edges as ek
from openhound_{{ cookiecutter.target_service_slug }}.kinds import nodes as nk
from openhound_{{ cookiecutter.target_service_slug }}.main import app
from openhound_{{ cookiecutter.target_service_slug }}.models.base import CollectorAsset


@dataclass
class AssetProperties(CollectorNodeProperties):
    """Asset graph properties.

    Attributes:
        hostname: DNS hostname of the asset.
        organization_name: Collected organization name resolved through lookup.
    """

    hostname: str
    organization_name: str | None = None


@app.asset(
    node=NodeDef(
        kind=nk.ASSET,
        description="Inventory asset",
        icon="cog",
        properties=AssetProperties,
    ),
    edges=[
        EdgeDef(
            start=nk.ASSET,
            end=nk.GROUP,
            kind=ek.MEMBER_OF,
            description="Asset belongs to group",
        )
    ],
)
class Asset(CollectorAsset):
    organization_id: str = Field(min_length=1)
    hostname: str
    groups: list[str] = Field(default_factory=list)

    @property
    def as_node(self) -> CollectorNode:
        return CollectorNode(
            id=self.id,
            kinds=[nk.ASSET],
            properties=AssetProperties(
                name=self.name,
                displayname=self.name,
                hostname=self.hostname,
                environmentid=self.organization_id,
                organization_name=self._lookup.organization_name(self.organization_id),
            ),
        )

    @property
    def edges(self) -> Iterator[Edge]:
        for group_id in self.groups:
            yield Edge(
                kind=ek.MEMBER_OF,
                start=EdgePath(value=self.id, match_by="id"),
                end=EdgePath(value=group_id, match_by="id"),
            )
