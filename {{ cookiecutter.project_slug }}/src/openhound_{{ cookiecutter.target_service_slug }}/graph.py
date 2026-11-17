from dataclasses import dataclass

from openhound.core.models.entries_dataclass import Node as BaseNode
from openhound.core.models.entries_dataclass import NodeProperties as BaseProperties


@dataclass
class CollectorNodeProperties(BaseProperties):
    """Properties shared by collector nodes.

    Attributes:
        name: Resource name.
        displayname: Human-readable resource label.
        environmentid: OpenGraph ID of the collected organization.
        last_seen: Conversion timestamp inherited from OpenHound.
    """


@dataclass
class CollectorNode(BaseNode):
    """Graph node with an explicitly assigned stable string ID."""

    id: str

    def __post_init__(self) -> None:
        """Retain the stable API ID supplied by the asset."""
