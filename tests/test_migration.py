import pytest
import tomlkit

from uv_migrate.core import migrate_dependencies, migrate_metadata


def test_migrate_metadata():
    poetry_toml = """
[tool.poetry]
name = "test-project"
version = "0.1.0"
description = "A test project"
authors = ["John Doe <john@example.com>"]
license = "MIT"
readme = "README.md"

[tool.poetry.dependencies]
python = "^3.10"
"""
    doc = tomlkit.parse(poetry_toml)
    project = migrate_metadata(doc)

    assert project["name"] == "test-project"
    assert project["version"] == "0.1.0"
    assert project["description"] == "A test project"
    assert project["authors"] == ["John Doe <john@example.com>"]
    assert project["license"] == "MIT"
    assert project["readme"] == "README.md"
    assert project["requires-python"] == ">=3.10"


def test_migrate_dependencies():
    poetry_toml = """
[tool.poetry.dependencies]
python = "^3.10"
requests = "^2.31.0"
flask = { version = "^3.0.0", extras = ["async"] }

[tool.poetry.group.dev.dependencies]
pytest = "^8.0.0"
"""
    doc = tomlkit.parse(poetry_toml)
    results = migrate_dependencies(doc)

    deps = results["dependencies"]
    assert "requests>=2.31.0" in deps
    assert "flask[async]>=3.0.0" in deps

    dev_deps = results["dependency-groups"]["dev"]
    assert "pytest>=8.0.0" in dev_deps


if __name__ == "__main__":
    pytest.main([__file__])
