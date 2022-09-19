from typing import Optional
import typer
from rich.console import Console
from pathlib import Path
from .managers import pip_manager
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
        help="Choices are pip , poetry (comming soon)",
    ),
    migrations: bool = typer.Option(
        default=False, metavar="🚀 Alembic Migrations", encoding="utf-8"
    ),
    docker: bool = typer.Option(default=False, metavar="🐋 Docker", encoding="utf-8"),
    testing: bool = typer.Option(default=False, metavar="💉 Tests", encoding="utf-8"),
    database: Database = typer.Option(
        default=Database.postgresql.value,
        metavar="📅 Database",
        help="Choices are sqlite3,postgresql,mysql",
    ),
):

    match package_manager:
        case PackageManager.pip:
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
        case PackageManager.poetry:
            # * Comming Soon
            ...


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
