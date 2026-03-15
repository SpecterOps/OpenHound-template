from pydantic import BaseModel
from openfetch.core.asset import BaseAsset, EdgeDef
from openfetch.core.models.entries import Edge, EdgePath
from openfetch_{{ cookiecutter.target_service_slug }}.graph import NodeTypes, Node, NodeProperties, EdgeTypes
from openfetch_{{ cookiecutter.target_service_slug }}.main import app
from typing import Iterator


# Optional if you want to store additional fields
# as part of the OpenGraph node
class ExtendedProperties(NodeProperties):
    hostname: str


class AssetNode(Node):
    # Extends the base Node properties with additional fields, unique to our asset
    # as defined in ExtendedProperties
    properties: ExtendedProperties


# The resource decorator specifies that the model is an OpenGraph asset
# with nodes and/or edges
@app.asset(kind=NodeTypes.Asset,description="Example Asset",
    edges=[
        EdgeDef(
            start=NodeTypes.Asset,
            end=NodeTypes.Group,
            kind=EdgeTypes.MemberOf,
            description="Asset belongs to group",
        )
    ]
)
class Asset(BaseAsset):
    id: int
    name: str
    hostname: str
    groups: list[str]

    @property
    def as_node(self) -> "AssetNode":
        properties = ExtendedProperties(
            name=self.name, displayname=self.name, hostname=self.hostname
        )
        return AssetNode(properties=properties)

    @property
    def _groups_memberships(self) -> Iterator[Edge]:
        for group in self.groups:
            start = EdgePath(value=self.as_node.id, match_by="id")
            end = EdgePath(value=Node.guid(name=group, node_type=NodeTypes.Group), match_by="id")
            yield Edge(kind=EdgeTypes.MemberOf, start=start, end=end)

    @property
    def edges(self) -> Iterator[Edge]:
        yield from self._groups_memberships
