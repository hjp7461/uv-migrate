from pathlib import Path
from typing import Any

import tomlkit
from tomlkit.items import Array, Table


def migrate_metadata(poetry_config: dict[str, Any]) -> dict[str, Any]:
    """Migrate Poetry metadata to PEP 621 (project section)."""
    poetry = poetry_config.get("tool", {}).get("poetry", {})
    project = tomlkit.table()

    # Basic metadata
    if "name" in poetry:
        project["name"] = poetry["name"]
    if "version" in poetry:
        project["version"] = poetry["version"]
    if "description" in poetry:
        project["description"] = poetry["description"]
    if "authors" in poetry:
        project["authors"] = poetry["authors"]
    if "license" in poetry:
        project["license"] = poetry["license"]
    if "readme" in poetry:
        project["readme"] = poetry["readme"]

    # Python version (requires-python)
    dependencies = poetry.get("dependencies", {})
    python_version = dependencies.get("python")
    if python_version:
        # Convert Poetry style (e.g., ^3.10) to PEP 440 (e.g., >=3.10)
        # Simplified conversion for common cases
        version_str = str(python_version)
        if version_str.startswith("^"):
            project["requires-python"] = ">=" + version_str[1:]
        elif version_str.startswith("~"):
            # ~3.10 -> >=3.10, <3.11 (simple approximation)
            project["requires-python"] = ">=" + version_str[1:]
        else:
            project["requires-python"] = version_str

    return project


def migrate_dependencies(poetry_config: dict[str, Any]) -> dict[str, Any]:
    """Migrate Poetry dependencies to project.dependencies and optional-dependencies."""
    poetry = poetry_config.get("tool", {}).get("poetry", {})
    results = {
        "dependencies": tomlkit.array(),
        "optional-dependencies": tomlkit.table(),
        "dependency-groups": tomlkit.table(),
    }

    # Helper to convert poetry dependency to PEP 508 string
    def convert_dep(dep_name: str, version_spec: Any) -> str:
        if isinstance(version_spec, str):
            # Simple conversion ^3.10 -> >=3.10
            if version_spec.startswith("^") or version_spec.startswith("~"):
                return f"{dep_name}>={version_spec[1:]}"
            return f"{dep_name}{version_spec}"
        if isinstance(version_spec, dict):
            # Handle complex dependencies like {version = "^2.0", extras = ["ssh"]}
            v = version_spec.get("version", "")
            if v.startswith("^") or v.startswith("~"):
                v = ">=" + v[1:]

            extras = version_spec.get("extras", [])
            extras_str = f"[{','.join(extras)}]" if extras else ""

            return f"{dep_name}{extras_str}{v}"
        return dep_name

    # project.dependencies (tool.poetry.dependencies)
    deps = poetry.get("dependencies", {})
    dependencies = results["dependencies"]
    if isinstance(dependencies, Array):
        for name, version in deps.items():
            if name.lower() == "python":
                continue
            dependencies.add_line(convert_dep(name, version))

    # dependency-groups (tool.poetry.group.dev.dependencies)
    groups = poetry.get("group", {})
    if "dev" in groups:
        dev_deps = groups["dev"].get("dependencies", {})
        dev_group = tomlkit.array()
        for name, version in dev_deps.items():
            dev_group.add_line(convert_dep(name, version))
        dependency_groups = results["dependency-groups"]
        if isinstance(dependency_groups, Table):
            dependency_groups["dev"] = dev_group

    return results


def migrate_scripts_and_build(poetry_config: dict[str, Any]) -> dict[str, Any]:
    """Migrate Poetry scripts and build system."""
    poetry = poetry_config.get("tool", {}).get("poetry", {})
    results: dict[str, Any] = {}

    # 3.3 Scripts (tool.poetry.scripts -> project.scripts)
    if "scripts" in poetry:
        results["scripts"] = poetry["scripts"]

    # 3.4 Build System (Update to hatchling as recommended for uv)
    results["build-system"] = {
        "requires": ["hatchling"],
        "build-backend": "hatchling.build",
    }

    # 3.5 Sources (tool.poetry.source -> tool.uv.sources)
    if "source" in poetry:
        uv_sources = tomlkit.table()
        for source in poetry["source"]:
            name = source.get("name")
            url = source.get("url")
            if name and url:
                uv_sources[name] = {"url": url}
        if uv_sources:
            results["uv-sources"] = uv_sources

    return results


def migrate_pyproject(input_path: Path) -> tomlkit.TOMLDocument:
    with open(input_path, encoding="utf-8") as f:
        doc = tomlkit.parse(f.read())

    new_doc = tomlkit.document()

    # 2.1 Metadata
    project_metadata = migrate_metadata(doc)
    new_doc["project"] = project_metadata

    # 2.2 Dependencies
    dep_results = migrate_dependencies(doc)
    project = new_doc["project"]
    if isinstance(project, Table) and dep_results["dependencies"]:
        project["dependencies"] = dep_results["dependencies"]

    if dep_results["dependency-groups"]:
        new_doc["dependency-groups"] = dep_results["dependency-groups"]

    # 2.3 Scripts & Build System & Sources
    extra_configs = migrate_scripts_and_build(doc)
    if "scripts" in extra_configs and isinstance(project, Table):
        project["scripts"] = extra_configs["scripts"]

    new_doc["build-system"] = extra_configs["build-system"]

    if "uv-sources" in extra_configs:
        if "tool" not in new_doc:
            new_doc["tool"] = tomlkit.table()
        tool = new_doc["tool"]
        if isinstance(tool, Table):
            tool["uv"] = tomlkit.table()
            uv = tool["uv"]
            if isinstance(uv, Table):
                uv["sources"] = extra_configs["uv-sources"]

    return new_doc
