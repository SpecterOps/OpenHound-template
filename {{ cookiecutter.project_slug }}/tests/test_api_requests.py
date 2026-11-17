from collections import Counter

from fastapi import FastAPI
from fastapi.testclient import TestClient

from openhound_{{ cookiecutter.target_service_slug }}.auth import (
    BasicCredentials,
    TokenCredentials,
)
from openhound_{{ cookiecutter.target_service_slug }}.client import build_client
from openhound_{{ cookiecutter.target_service_slug }}.models import Asset, Group, Organization
from openhound_{{ cookiecutter.target_service_slug }}.source import source


def test_token_authentication(mock_api: FastAPI, mock_service: TestClient) -> None:
    """Token credentials send a bearer header recorded by the mock API."""
    credentials = TokenCredentials(
        api_url=str(mock_service.base_url), token="test-token"
    )
    response = build_client(credentials).get("/organization")
    assert response.status_code == 200
    assert mock_api.state.requests == [
        {"path": "/organization", "query": {}, "authorization": "Bearer test-token"}
    ]


def test_basic_authentication(mock_api: FastAPI, mock_service: TestClient) -> None:
    """Username and password credentials send the recorded basic-auth header."""
    credentials = BasicCredentials(
        api_url=str(mock_service.base_url),
        username="test-user",
        password="test-password",
    )
    response = build_client(credentials).get("/organization")
    assert response.status_code == 200
    assert mock_api.state.requests == [
        {
            "path": "/organization",
            "query": {},
            "authorization": "Basic dGVzdC11c2VyOnRlc3QtcGFzc3dvcmQ=",
        }
    ]


def test_organization_collection(mock_api: FastAPI, mock_service: TestClient) -> None:
    """Collect the organization as a validated model with one root request."""
    credentials = TokenCredentials(
        api_url=str(mock_service.base_url), token="test-token"
    )
    organizations = list(
        source(credentials=credentials).with_resources("organizations")
    )
    assert len(organizations) == 1
    assert isinstance(organizations[0], Organization)
    assert organizations[0].id == "org-a"
    assert [entry["path"] for entry in mock_api.state.requests] == ["/organization"]


def test_groups_collection(mock_api: FastAPI, mock_service: TestClient) -> None:
    """Collect validated groups with their organization identifier."""
    credentials = TokenCredentials(
        api_url=str(mock_service.base_url), token="test-token"
    )
    groups = list(source(credentials=credentials).with_resources("groups"))
    assert all(isinstance(group, Group) for group in groups)
    assert [group.id for group in groups] == ["group-a", "group-b"]
    assert all(group.organization_id == "org-a" for group in groups)
    assert Counter(entry["path"] for entry in mock_api.state.requests) == {
        "/organization": 1,
        "/organizations/org-a/groups": 1,
    }


def test_assets_collection(mock_api: FastAPI, mock_service: TestClient) -> None:
    """Collect validated assets across pages and propagate their organization ID."""
    credentials = TokenCredentials(
        api_url=str(mock_service.base_url), token="test-token"
    )
    assets = list(source(credentials=credentials).with_resources("assets"))
    assert all(isinstance(asset, Asset) for asset in assets)
    assert [asset.id for asset in assets] == ["asset-a", "asset-b", "asset-c"]
    assert all(asset.organization_id == "org-a" for asset in assets)
    assert Counter(entry["path"] for entry in mock_api.state.requests) == {
        "/organization": 1,
        "/organizations/org-a/assets": 2,
    }
    asset_requests = [
        entry
        for entry in mock_api.state.requests
        if entry["path"] == "/organizations/org-a/assets"
    ]
    assert asset_requests[0]["query"] == {}
    assert asset_requests[1]["query"] == {"page": "2"}
