from pathlib import Path
from typing import Optional

import typer
from rich.console import Console

from .apps.generator_app import generator_app
from .enums.generator_enums import Components
from .enums.manager_enums import Database
from .enums.manager_enums import PackageManager
from .managers import pip_manager
from .managers import poetry_manager

app = typer.Typer(
    help="A CLI for your next FastAPI project", pretty_exceptions_show_locals=False
)

app.add_typer(generator_app, name="g")

console = Console()


@app.command(help="Scaffold new project")
def new(
    project_name: str = typer.Argument(
        default=...,
        metavar="⭐ Project Name",
    ),
    dir: Optional[Path] = typer.Option(
        default=None,
        show_default="Current Working Directory",  # type: ignore
        metavar="📁 Directory Path",
        help="Where You Want To Start The Project",
    ),
    package_manager: PackageManager = typer.Option(
        default=PackageManager.pip.value,
        metavar="📦 Package Manager",
        help="Choices are pip , poetry ",
        show_choices=True,
    ),
    migrations: bool = typer.Option(default=False, metavar="🚀 Alembic Migrations"),
    docker: bool = typer.Option(default=False, metavar="🐋 Docker"),
    testing: bool = typer.Option(default=True, metavar="💉 Tests"),
    database: Database = typer.Option(
        default=Database.postgresql.value,
        metavar="📅 Database",
        help="Choices are sqlite3,postgresql,mysql",
        show_choices=True,
    ),
    orm: bool = typer.Option(default=False, metavar="⚙️ ORM"),
    skip_install: bool = typer.Option(
        default=False, help="Skip installation process"
    ),  # todo needs some work
):
    console.print(
        """[yellow bold]
      \t\t\t        /|
      \t\t\t       / |
      \t\t\t      /  |
      \t\t\t     /   |
      \t\t\t    /    |
      \t\t\t   /     |
      \t\t\t  /      |________
      \t\t\t /_______        /
      \t\t\t         |      /
      \t\t\t         |     /
      \t\t\t         |    /
      \t\t\t         |   /
      \t\t\t         |  /
      \t\t\t         | /
      \t\t\t         |/
      \t\t\t            [/]"""
    )
    if package_manager == PackageManager.pip:
        pipmanager = pip_manager.PipManager(
            project_name=project_name,
            migrations=migrations,
            testing=testing,
            database=database,
            docker=docker,
            orm=orm,
            skip_install=skip_install,
        )
        if dir is not None:
            pipmanager.nav_to_dir(dir)
        pipmanager.init_env()
        pipmanager.create_project()
    elif package_manager == PackageManager.poetry:
        poetrymanager = poetry_manager.PoetryManager(
            project_name=project_name,
            migrations=migrations,
            database=database,
            docker=docker,
            orm=orm,
            skip_install=skip_install,
        )
        if dir is not None:
            poetrymanager.nav_to_dir(dir)
        poetrymanager.create_poetry_project()


@app.command(help="Show FastGen info")
def info():
    console.print(
        """
    ⚡[yellow bold]FastGen[/], A CLI for your next FastAPI project
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
