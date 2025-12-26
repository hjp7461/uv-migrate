import shutil
from pathlib import Path
from typing import Annotated

import tomlkit
import typer

from .core import migrate_pyproject

app = typer.Typer(help="Poetry to uv Migration Tool")


@app.command()
def migrate(
    input_file: Annotated[
        Path, typer.Argument(help="Path to the Poetry pyproject.toml")
    ] = Path("pyproject.toml"),
    output_file: Annotated[
        Path | None,
        typer.Option("--output", "-o", help="Path to the new pyproject.toml"),
    ] = None,
    backup: Annotated[
        bool, typer.Option(help="Create a backup of the original file")
    ] = True,
) -> None:
    """
    Migrate a Poetry pyproject.toml to uv (PEP 621) format.
    """
    if not input_file.exists():
        typer.echo(f"Error: {input_file} does not exist.", err=True)
        raise typer.Exit(code=1)

    # Prevent migrating this project's own pyproject.toml
    own_pyproject = (
        Path(__file__).resolve().parent.parent.parent / "pyproject.toml"
    ).resolve()
    if input_file.resolve() == own_pyproject:
        typer.echo(
            "Error: Modifying the pyproject.toml of the uv-migrate project itself "
            "is not allowed.",
            err=True,
        )
        raise typer.Exit(code=1)

    # 3.2 Validate input file
    with open(input_file, encoding="utf-8") as f:
        content = f.read()
        try:
            doc = tomlkit.parse(content)
        except Exception as e:
            typer.echo(f"Error parsing {input_file}: {e}", err=True)
            raise typer.Exit(code=1) from e

    if (
        not isinstance(doc, dict)
        or "tool" not in doc
        or not isinstance(doc["tool"], dict)
        or "poetry" not in doc["tool"]
    ):
        typer.echo(
            "Error: [tool.poetry] section not found. Is this a Poetry project?",
            err=True,
        )
        raise typer.Exit(code=1)

    # 3.3 Backup
    if backup:
        backup_path = input_file.with_suffix(input_file.suffix + ".bak")
        shutil.copy2(input_file, backup_path)
        typer.echo(f"Backup created: {backup_path}")

    # Core migration
    try:
        new_doc = migrate_pyproject(input_file)
    except Exception as e:
        typer.echo(f"Error during migration: {e}", err=True)
        raise typer.Exit(code=1) from e

    # 3.1 & 3.4 Save and message
    target_path = output_file if output_file else input_file
    with open(target_path, "w", encoding="utf-8") as f:
        f.write(tomlkit.dumps(new_doc))

    typer.echo(f"Migration completed successfully! File saved to: {target_path}")
    typer.echo("Next step: Run 'uv lock' to generate the lockfile.")


if __name__ == "__main__":
    app()
