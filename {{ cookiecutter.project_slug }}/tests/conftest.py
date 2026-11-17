import json
from collections.abc import Iterator
from pathlib import Path
from typing import Any
from urllib.parse import urlsplit

import httpx
import pytest
import requests
from dlt.sources.helpers.rest_client import RESTClient
from fastapi import FastAPI, Request
from fastapi.testclient import TestClient
from starlette.middleware.base import RequestResponseEndpoint
from starlette.responses import Response

TEST_DATA_DIR = Path(__file__).parent / "test_data" / "api"


def load_json(name: str) -> dict[str, Any]:
    """Read one sample API response."""
    return json.loads((TEST_DATA_DIR / f"{name}.json").read_text(encoding="utf-8"))


def paginate_response(
    request: Request, data: dict[str, Any], page: int = 1, page_size: int = 2
) -> dict[str, Any]:
    """Slice sample items and include a next URL only when another page exists."""
    rows = data["items"]
    start = (page - 1) * page_size
    content = {"items": rows[start : start + page_size]}
    if start + page_size < len(rows):
        content["next"] = str(request.url.include_query_params(page=page + 1))
    return content


@pytest.fixture
def mock_api() -> FastAPI:
    """Create three sample-backed routes and fresh request history."""
    app = FastAPI()
    app.state.requests = []

    @app.middleware("http")
    async def record_request(
        request: Request, call_next: RequestResponseEndpoint
    ) -> Response:
        """Record the path, query parameters, and prepared authorization header."""
        app.state.requests.append(
            {
                "path": request.url.path,
                "query": dict(request.query_params),
                "authorization": request.headers.get("authorization"),
            }
        )
        return await call_next(request)

    @app.get("/organization")
    async def organization() -> dict[str, Any]:
        """Return the sample organization."""
        return load_json("organization")

    @app.get("/organizations/{organization_id}/groups")
    async def groups(
        organization_id: str, request: Request, page: int = 1
    ) -> dict[str, Any]:
        """Return the sample directory groups."""
        return paginate_response(request, load_json("groups"), page)

    @app.get("/organizations/{organization_id}/assets")
    async def assets(
        organization_id: str, request: Request, page: int = 1
    ) -> dict[str, Any]:
        """Return sample assets using the shared pagination helper."""
        return paginate_response(request, load_json("assets"), page)

    return app


@pytest.fixture
def mock_service(
    mock_api: FastAPI, monkeypatch: pytest.MonkeyPatch
) -> Iterator[TestClient]:
    """Route prepared DLT requests through TestClient without network access."""
    with TestClient(mock_api, base_url="https://collector.localhost") as client:

        def send_request(
            rest_client: RESTClient, request: requests.Request, **kwargs: Any
        ) -> httpx.Response:
            """Preserve the real request and reject unexpected external hosts."""
            prepared = rest_client.session.prepare_request(request)
            assert prepared.url is not None
            assert prepared.method is not None
            url = urlsplit(prepared.url)
            assert (url.scheme, url.netloc) == ("https", "collector.localhost"), (
                f"Unexpected external request: {prepared.url}"
            )
            return client.request(
                method=prepared.method,
                url=prepared.url,
                headers=dict(prepared.headers),
                content=prepared.body,
                follow_redirects=False,
            )

        monkeypatch.setattr(RESTClient, "_send_request", send_request)
        yield client
