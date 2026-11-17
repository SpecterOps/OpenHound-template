import ast
import os
import subprocess
import sys
import zipfile
from pathlib import Path

import pytest
from cookiecutter.main import cookiecutter

ROOT = Path(__file__).resolve().parents[1]


@pytest.fixture(
    scope="module",
    params=[
        {},
        {
            "project_name": "Example Cloud Collector",
            "target_service": "Example Cloud",
            "author": "Example Author",
            "author_email": "author@example.com",
        },
    ],
    ids=["default", "custom"],
)
def rendered(
    request: pytest.FixtureRequest, tmp_path_factory: pytest.TempPathFactory
) -> Path:
    """Render both default and customized service/package names."""
    return Path(
        cookiecutter(
            str(ROOT),
            no_input=True,
            output_dir=str(tmp_path_factory.mktemp("rendered")),
            extra_context=request.param,
        )
    )


@pytest.mark.parametrize(
    "relative_path",
    [
        "auth.py",
        "client.py",
        "source_context.py",
        "models/base.py",
        "lookup.py",
        "transforms.py",
        "sql/10_organization_names.sql",
        "resources/directory/groups.py",
        "resources/inventory/assets.py",
    ],
)
def test_rendered_structure(rendered: Path, relative_path: str) -> None:
    """Each expected application file is present in the rendered package."""
    package = next((rendered / "src").glob("openhound_*"))
    assert (package / relative_path).is_file()


@pytest.mark.parametrize(
    "relative_path",
    [
        "conftest.py",
        "test_api_requests.py",
        "test_data/api/organization.json",
        "test_data/api/groups.json",
        "test_data/api/assets.json",
    ],
)
def test_rendered_test_files(rendered: Path, relative_path: str) -> None:
    """Each expected test fixture and sample is included in the render."""
    assert (rendered / "tests" / relative_path).is_file()


def test_rendered_python(rendered: Path) -> None:
    """Generated Python parses and contains no remaining template expressions."""
    for path in rendered.rglob("*.py"):
        text = path.read_text()
        assert "{{" not in text
        ast.parse(text, filename=str(path))


def test_generated_checks(rendered: Path) -> None:
    """Run generated tests from sample collector"""
    env = {
        **os.environ,
        "PYTHONPATH": str(rendered / "src"),
        "RUNTIME__DLTHUB_TELEMETRY": "false",
    }

    args =  ["pytest", "-q", f"--basetemp={rendered.parent / 'pytest-state'}"]
    result = subprocess.run(
        [sys.executable, "-m", *args],
        check=False,
        cwd=rendered,
        env=env,
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0, result.stdout + result.stderr

