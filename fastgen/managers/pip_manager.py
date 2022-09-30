from pathlib import Path
import os
from rich.console import Console
from ..options import Database
from .base_manager import Manager
import textwrap
from .. import constants


console = Console()


class PipManager(Manager):
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
        database: Database,
        docker: bool,
    ) -> None:
        self.project_name = project_name
        self.migrations = migrations
        self.testing = testing
        self.database = database
        self.docker = docker

    def nav_to_dir(self, dir_name: str) -> None:
        return super().nav_to_dir(dir_name)

    def create_project(self):
        """
        entry point function for creating all sort of things (files , migrations ...)
        """
        console.print("Creating Project Structure ....", end="\r")
        self.project_path = Path(self.project_name)
        os.makedirs(self.project_path)

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
        self.generate_db_related_files(database_path=database_path)

        # create .env file
        self.generate_env_file(project_path=self.project_path)

        # create docker file
        if self.docker:
            self.generate_docker_file(project_path=self.project_path)

        console.print("Creating Project Structure .... [green bold]SUCCESS[/]")
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
        console.print("Spawning Virtual Environment .... ", end="\r")
        os.system("python -m venv .venv")
        console.print("Spawning Virtual Environment .... [green bold]SUCCESS[/]")

        console.print("Installing required dependencies ....", end="\r")
        os.system(f".\.venv\Scripts\python.exe -m pip install --upgrade pip -q")
        os.system(
            f".\.venv\Scripts\python.exe -m pip install fastapi python-dotenv\
            { 'pytest' if self.testing else ''} \
            {'alembic' if self.migrations else ''} -q"
        )
        console.print("Installing required dependencies .... [green bold]SUCCESS[/]")

    def generate_main_files(self, api_path: Path):
        return super().generate_main_files(api_path)

    def generate_db_related_files(self, database_path: Path):
        return super().generate_db_related_files(database_path)

    def generate_settings_related_files(self, settings_path: Path):
        return super().generate_settings_related_files(settings_path)

    def generate_env_file(self, project_path: Path):
        return super().generate_env_file(project_path)

    def generate_test_files(self, testing_path: Path):
        "generate testing files"
        with open(testing_path / "__init__.py", "x", encoding="utf-8") as f:
            ...
        with open(testing_path / "test_main.py", "x", encoding="utf-8") as f:
            f.write(textwrap.dedent(constants.TESTING))

    def generate_docker_file(self, project_path: Path):
        return super().generate_docker_file(project_path)
