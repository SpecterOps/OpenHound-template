from typing import ClassVar

from dlt.common.libs.pydantic import DltConfig
from openhound.core.asset import BaseAsset
from pydantic import Field

from openhound_{{ cookiecutter.target_service_slug }}.lookup import CollectorLookup


class CollectorAsset(BaseAsset):
    """Base asset fields with a lookup type override, specific to the custom collector"""

    dlt_config: ClassVar[DltConfig] = {"return_validated_models": True}

    _lookup: CollectorLookup

    id: str = Field(min_length=1)
    name: str
