from pydantic import BaseModel, ConfigDict, Field, computed_field
from openfetch.core.models.graph import MetaData, Graph as CommonGraph
from openfetch.core.models.entries import (
    Node as BaseNode,
    Edge,
    NodeProperties as BaseProperties,
)
from enum import Enum


# TODO: Define your edge types here
class EdgeTypes(str, Enum):
    MemberOf = "ExampleMemberOf"


# TODO: Define your node types here
class NodeTypes(str, Enum):
    Asset = "ExampleAsset"
    Group = "ExampleGroup"


class NodeProperties(BaseProperties):
    # TODO: Add your custom required node properties here. These should be unique
    # to the service/collector and EVERY node should contain these properties.
    # However, specific node types can contain a set of extended properties.
    model_config = ConfigDict(extra="allow")

    # Examples:
    tenant: str


class Node(BaseNode):
    properties: NodeProperties

    # TODO: Override the base guid generation with a unique combination of properties which unique
    # identify your resource for the particular service. Name and node_type are always required
    @staticmethod
    def guid(name, node_type) -> str:
        return BaseNode.guid(name, node_type, ...)

    @computed_field
    @property
    def id(self) -> str:
        # TODO: Replace the following line with a unique combination of properties
        # that identify your resource.
        dyn_uid = self.guid(self.properties.name, self.kinds[0])
        return dyn_uid


class GraphEntries(BaseModel):
    nodes: list[Node] = []
    edges: list[Edge] = Field(default_factory=list)


class Graph(CommonGraph):
    graph: GraphEntries
    metadata: MetaData = Field(default_factory=MetaData)
