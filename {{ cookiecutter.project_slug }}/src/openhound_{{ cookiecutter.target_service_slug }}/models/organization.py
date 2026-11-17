from collections.abc import Iterator
from dataclasses import dataclass

from openhound.core.asset import NodeDef
from openhound.core.models.entries import Edge

from openhound_{{ cookiecutter.target_service_slug }}.graph import (
    CollectorNode,
    CollectorNodeProperties,
)
from openhound_{{ cookiecutter.target_service_slug }}.kinds import nodes as nk
from openhound_{{ cookiecutter.target_service_slug }}.main import app
from openhound_{{ cookiecutter.target_service_slug }}.models.base import CollectorAsset


@dataclass
class OrganizationProperties(CollectorNodeProperties):
    """Environment root properties inherited from the collector base."""


@app.asset(
    node=NodeDef(
        kind=nk.ORGANIZATION,
        description="Collected environment",
        icon="building",
        properties=OrganizationProperties,
    )
)
class Organization(CollectorAsset):

    @property
    def as_node(self) -> CollectorNode:
        return CollectorNode(
            id=self.id,
            kinds=[nk.ORGANIZATION],
            properties=OrganizationProperties(
                name=self.name, displayname=self.name, environmentid=self.id
            ),
        )

    @property
    def edges(self) -> Iterator[Edge]:
        """The environment root has no outgoing relationships."""
        yield from ()
