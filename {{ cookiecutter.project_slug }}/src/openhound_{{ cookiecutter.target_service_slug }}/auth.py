from dlt.common.configuration import configspec
from dlt.common.configuration.specs import CredentialsConfiguration
from dlt.common.typing import TSecretStrValue
from dlt.sources.helpers.rest_client.auth import (
    BearerTokenAuth,
    HttpBasicAuth,
)


@configspec
class ServiceCredentials(CredentialsConfiguration):
    """Shared, non-secret API configuration inherited by auth-specific classes"""

    api_url: str = "https://api.example.com"


@configspec
class TokenCredentials(ServiceCredentials):
    """Authenticate with an API bearer token."""

    # DLT uses None for required configuration fields that are not yet resolved.
    token: TSecretStrValue = None  # type: ignore[assignment]

    @property
    def auth(self) -> BearerTokenAuth:
        """Build the bearer authentication adapter for this credential type."""
        return BearerTokenAuth(token=self.token)


@configspec
class BasicCredentials(ServiceCredentials):
    """Authenticate with an API username and password."""

    username: str = None  # type: ignore[assignment]
    password: TSecretStrValue = None  # type: ignore[assignment]

    @property
    def auth(self) -> HttpBasicAuth:
        """Build the basic authentication adapter for this credential type."""
        return HttpBasicAuth(username=self.username, password=self.password)
