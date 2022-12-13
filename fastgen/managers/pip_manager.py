import os
import textwrap
from pathlib import Path

from rich.console import Console
from rich.progress import Progress
from rich.progress import SpinnerColumn
from rich.progress import TextColumn

from ..blocks import main_blocks
from ..enums import manager_enums
from .base_manager import AbstractManager

console = Console()


class PipManager(AbstractManager):
    """
    class to handle pip related operations such as creating folders and files ,
    spawning virtual environments , creating migrations , dockerizing and
    creating env file
    """

    def __init__(
        self,
        project_name: str,
        migrations: bool,
        testing: bool,
        database: manager_enums.Database,
        docker: bool,
        orm: bool,
        skip_install: bool,
    ) -> None:
        self.testing = testing
        super().__init__(project_name, migrations, database, docker, orm, skip_install)

    def nav_to_dir(self, dir_name: Path) -> None:
        return super().nav_to_dir(dir_name)

    def create_project(self):
        """
        entry point function for creating all sort of things (files , migrations ...)
        """
        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            transient=True,
        ) as progress:
            progress.add_task(description="Creating Project Structure ....", total=7)
            self.project_path = Path(self.project_name)
            os.makedirs(self.project_path)

            # install the reqiured dependencies first
            self.init_env()

            # create test stuff
            if self.testing:
                test_path = self.project_path / "test"
                os.makedirs(test_path)
                self.generate_test_files(testing_path=test_path)

            # create api stuff
            api_path = self.project_path / "app" / "api"
            os.makedirs(api_path)
            self.generate_main_files(api_path=api_path)

            # create settings stuff
            settings_path = self.project_path / "app" / "core"
            os.makedirs(settings_path)
            self.generate_settings_related_files(settings_path=settings_path)

            # create database stuff
            database_path = self.project_path / "app" / "database"
            os.makedirs(database_path)
            self.generate_db_related_files(database_path=database_path, orm=self.orm)

            # create .env file
            self.generate_env_file(project_path=self.project_path)

            # create docker file
            if self.docker:
                self.generate_docker_file(project_path=self.project_path)

            # todo create readme file

        console.print("[green bold]SUCCESS[/]: Create Project Structure")

        os.chdir(self.project_path)

        # create migrations if True
        # migrations is put here due to weired behaviour of
        # alembic ini file which is created outside the project folder
        if self.migrations:
            os.system("alembic init migrations")

    def init_env(self):
        """
        spawn a pip virtual environment inside the directory when `--package-manager` is set to `pip`
        and installing the required dependencies (fastapi, pytest, alembic, python-dotenv)
        """
        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            transient=True,
        ) as progress:
            progress.add_task(description="Spawning Virtual Environment .... ", total=1)
            os.system("python -m venv .venv")
        console.print("[green bold]SUCCESS[/]: Spawn Virtual Environment ....")

        if not self.skip_install:
            with Progress(
                SpinnerColumn(),
                TextColumn("[progress.description]{task.description}"),
                transient=True,
            ) as progress:
                progress.add_task(
                    description="Installing required dependencies ....", total=2
                )
            os.system(f".\.venv\Scripts\python.exe -m pip install --upgrade pip -q")
            os.system(
                f".\.venv\Scripts\python.exe -m pip install fastapi python-dotenv\
                { 'pytest' if self.testing else ''} \
                {'alembic' if self.migrations else ''} -q"
            )
            console.print("[green bold]SUCCESS[/]: Installe required dependencies ....")

    def generate_main_files(self, api_path: Path):
        return super().generate_main_files(api_path)

    def generate_db_related_files(self, database_path: Path, orm: bool):
        return super().generate_db_related_files(database_path, orm=orm)

    def generate_settings_related_files(self, settings_path: Path):
        return super().generate_settings_related_files(settings_path)

    def generate_env_file(self, project_path: Path):
        return super().generate_env_file(project_path)

    def generate_test_files(self, testing_path: Path):
        "generate testing files"
        with open(testing_path / "__init__.py", "x", encoding="utf-8") as f:
            ...
        with open(testing_path / "test_main.py", "x", encoding="utf-8") as f:
            f.write(textwrap.dedent(main_blocks.MAIN_TESTING))

    def generate_docker_file(self, project_path: Path):
        return super().generate_docker_file(project_path)
