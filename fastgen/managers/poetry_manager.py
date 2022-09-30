from pathlib import Path
import os
from rich.console import Console
from ..options import Database
from .base_manager import Manager


console = Console()


class PoetryManager(Manager):
    """
    class to handle poetry related operations such as creating a poetry env
    creating a poetry project ...
    """

    def __init__(
        self,
        project_name: str,
        migrations: bool,
        database: Database,
        docker: bool,
        orm: bool,
    ) -> None:
        self.project_name = project_name
        self.migrations = migrations
        self.database = database
        self.docker = docker
        self.orm = orm

    def nav_to_dir(self, dir_name: str) -> None:
        return super().nav_to_dir(dir_name)

    def create_poetry_project(self):
        self.project_path = Path(self.project_name)
        self.inner_project_path = self.project_path / self.project_name
        # innert project path is the path of the app folder created inside the root directory
        # project_path
        # |__inner_project_path
        # |__ ...
        console.print("Creating Poetry Project ...", end="\r")
        os.system(f"poetry new {self.project_path} -q")
        console.print("Creating Poetry Project ... [green bold]SUCCESS[/]")
        self.init_env()
        self.create_files()

    def init_env(self):
        """
        we used `poetry env` command to create the venv without activating it
        which what happens if we use `poetry shell` which may run into some conflicts
        if you try to run the program when you already have an activated venv
        """
        console.print("Spawning Virtual Environment ...", end="\r")
        os.system("poetry env use python -q")
        console.print("Spawning Virtual Environment ... [green bold]SUCCESS[/]")

    def create_files(self):
        # create api stuff
        api_path = self.inner_project_path / "api"
        os.makedirs(api_path)
        self.generate_main_files(api_path=api_path)

        # create settings stuff
        settings_path = self.inner_project_path / "core"
        os.makedirs(settings_path)
        self.generate_settings_related_files(settings_path=settings_path)

        # create database stuff
        database_path = self.inner_project_path / "database"
        os.makedirs(database_path)
        self.generate_db_related_files(database_path=database_path, orm=self.orm)

        # create .env file
        self.generate_env_file(project_path=self.project_path)

        # create docker file
        if self.docker:
            self.generate_docker_file(project_path=self.project_path)

        os.chdir(self.project_path)

        # create migrations if True
        # migrations is put here due to weired behaviour of
        # alembic ini file which is created outside the project folder
        if self.migrations:
            os.system("alembic init migrations")

    def generate_main_files(self, api_path: Path):
        return super().generate_main_files(api_path)

    def generate_db_related_files(self, database_path: Path, orm: bool):
        return super().generate_db_related_files(database_path, orm)

    def generate_settings_related_files(self, settings_path: Path):
        return super().generate_settings_related_files(settings_path)

    def generate_env_file(self, project_path: Path):
        return super().generate_env_file(project_path)

    def generate_docker_file(self, project_path: Path):
        return super().generate_docker_file(project_path)
