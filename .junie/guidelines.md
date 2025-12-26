### Project Overview
`uv-migrate` is a tool designed to migrate Poetry-based `pyproject.toml` files to the `uv` (PEP 621) standard. It is built using Python, `tomlkit` for TOML manipulation, and `typer` for the CLI interface.

### Build/Configuration Instructions
The project uses `uv` for dependency management and build processes.

#### Prerequisites
- `uv` installed on your system.
- Python 3.13 or higher.

#### Setup and Installation
To install the tool for development or local use:
```bash
uv tool install .
```
Or to install in editable mode for development:
```bash
uv run pip install -e .
```

### Testing Information
Tests are written using `pytest` and are located in the `tests/` directory.

#### Running Tests
To run the entire test suite, use the following command (setting `PYTHONPATH` to include `src` ensures modules are found correctly):
```bash
PYTHONPATH=src uv run pytest
```

#### Adding New Tests
When adding new tests, follow these guidelines:
1. Create a new test file in the `tests/` directory with the `test_` prefix (e.g., `tests/test_feature.py`).
2. Import the necessary functions from `uv_migrate`.
3. Use `pytest` assertions to verify behavior.
4. Mock or provide sample TOML strings using `tomlkit` to simulate Poetry configurations.

#### Example Test
Here is a simple test case demonstrating how to test the metadata migration:
```python
import pytest
import tomlkit
from uv_migrate.core import migrate_metadata

def test_metadata_migration_demo():
    # Sample Poetry TOML
    poetry_toml = """
[tool.poetry]
name = "demo-project"
version = "1.0.0"
description = "A demo project"
"""
    doc = tomlkit.parse(poetry_toml)
    # Perform migration
    project = migrate_metadata(doc)
    
    # Assertions
    assert project["name"] == "demo-project"
    assert project["version"] == "1.0.0"
    assert project["description"] == "A demo project"
```

### Additional Development Information

#### Code Style and Quality
The project enforces strict code style and type checking using `ruff` and `mypy`.

- **Linting and Formatting**: Use `ruff` for linting and formatting. Configuration is in `pyproject.toml`.
  ```bash
  uv run ruff check .
  uv run ruff format .
  ```
- **Type Checking**: Use `mypy` for static type analysis.
  ```bash
  uv run mypy src
  ```

#### Development Workflow
1. Use `src/` directory for all source code.
2. Maintain PEP 621 compliance for the project's own `pyproject.toml`.
3. When modifying core logic in `src/uv_migrate/core.py`, ensure that all existing tests pass and add new ones if necessary.
