from collections.abc import Iterator
from dataclasses import dataclass

from openhound.core.asset import NodeDef
from openhound.core.models.entries import Edge
from pydantic import Field

from openhound_{{ cookiecutter.target_service_slug }}.graph import (
    CollectorNode,
    CollectorNodeProperties,
)
from openhound_{{ cookiecutter.target_service_slug }}.kinds import nodes as nk
from openhound_{{ cookiecutter.target_service_slug }}.main import app
from openhound_{{ cookiecutter.target_service_slug }}.models.base import CollectorAsset


@dataclass
class GroupProperties(CollectorNodeProperties):
    """Directory group properties inherited from the collector base."""


@app.asset(
    node=NodeDef(
        kind=nk.GROUP,
        description="Directory group",
        icon="users",
        properties=GroupProperties,
    )
)
class Group(CollectorAsset):
    organization_id: str = Field(min_length=1)

    @property
    def as_node(self) -> CollectorNode:
        return CollectorNode(
            id=self.id,
            kinds=[nk.GROUP],
            properties=GroupProperties(
                name=self.name,
                displayname=self.name,
                environmentid=self.organization_id,
            ),
        )

    @property
    def edges(self) -> Iterator[Edge]:
        yield from ()
