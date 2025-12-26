from pathlib import Path

import pytest
from typer.testing import CliRunner

from uv_migrate.cli import app

runner = CliRunner()


def test_prevent_self_migration() -> None:
    # Get the path to the project's own pyproject.toml
    # tests/test_cli.py -> tests -> project_root
    project_root = Path(__file__).resolve().parent.parent
    own_pyproject = project_root / "pyproject.toml"

    # Run the migrate command pointing to its own pyproject.toml
    # Use 'migrate' command explicitly as it is the only command in the app
    result = runner.invoke(app, [str(own_pyproject)])

    assert result.exit_code == 1
    assert (
        "Error: Modifying the pyproject.toml of the uv-migrate project itself "
        "is not allowed." in result.stderr
    )


def test_prevent_default_self_migration(monkeypatch: pytest.MonkeyPatch) -> None:
    # Mock the current working directory to the project root
    project_root = Path(__file__).resolve().parent.parent
    monkeypatch.chdir(project_root)

    # Run the migrate command without arguments (defaults to pyproject.toml)
    result = runner.invoke(app, [])

    assert result.exit_code == 1
    assert (
        "Error: Modifying the pyproject.toml of the uv-migrate project itself "
        "is not allowed." in result.stderr
    )
