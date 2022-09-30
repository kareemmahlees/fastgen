from typing import Optional
import typer
from rich.console import Console
from pathlib import Path
from .managers import pip_manager, poetry_manager
from .options import PackageManager, Database

app = typer.Typer(
    help="Start FastAPI Projects in Lightning Speed",
    # pretty_exceptions_enable=True,
    # pretty_exceptions_show_locals=False,
)
console = Console()


@app.command()
def new(
    project_name: str = typer.Argument(
        default=...,
        metavar="⭐ Project Name",
    ),
    dir: Optional[Path] = typer.Option(
        default=None,
        show_default="Current Working Directory",
        metavar="📁 Directory Path",
        help="Where You Want To Start The Project",
    ),
    package_manager: PackageManager = typer.Option(
        default=PackageManager.pip.value,
        metavar="📦 Package Manager",
        help="Choices are pip , poetry ",
    ),
    migrations: bool = typer.Option(default=False, metavar="🚀 Alembic Migrations"),
    docker: bool = typer.Option(default=False, metavar="🐋 Docker"),
    testing: bool = typer.Option(default=False, metavar="💉 Tests"),
    database: Database = typer.Option(
        default=Database.postgresql.value,
        metavar="📅 Database",
        help="Choices are sqlite3,postgresql,mysql",
    ),
):
    if package_manager == PackageManager.pip:
        pipmanager = pip_manager.PipManager(
            project_name=project_name,
            migrations=migrations,
            testing=testing,
            database=database,
            docker=docker,
        )
        if dir is not None:
            pipmanager.nav_to_dir(dir)
        pipmanager.create_project()
        pipmanager.init_env()
    elif package_manager == PackageManager.poetry:
        poetrymanager = poetry_manager.PoetryManager(
            project_name=project_name,
            migrations=migrations,
            database=database,
            docker=docker,
        )
        if dir is not None:
            poetrymanager.nav_to_dir(dir)
        poetrymanager.create_poetry_project()


@app.command()
def info():
    console.print(
        """
    ⚡[yellow bold]FastGen[/], Start FastAPI Projects In Lightning Speed
    built with [bold]typer[/], to help with [green bold]FastAPI[/]

    Developed By Kareem Ebrahim (2022)
    https://github.com/kareemmahlees

    Quickly Generate FastAPI Project Template With Migrations , Docker , Tests, Database and more

    Want to help the project ?
    ⭐ Star it on github : https://github.com/kareemmahlees/fastgen
    """
    )


if __name__ == "__main__":
    app()
