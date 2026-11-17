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
