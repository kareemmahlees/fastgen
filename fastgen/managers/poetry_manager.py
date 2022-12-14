import os
from pathlib import Path

from rich.console import Console
from rich.progress import Progress
from rich.progress import SpinnerColumn
from rich.progress import TextColumn

from ..enums import manager_enums
from .base_manager import AbstractManager

console = Console()


class PoetryManager(AbstractManager):
    """
    class to handle poetry related operations such as creating a poetry env
    creating a poetry project ...
    """

    def __init__(
        self,
        project_name: str,
        migrations: bool,
        database: manager_enums.Database,
        docker: bool,
        orm: bool,
        skip_install: bool,
    ) -> None:
        super().__init__(project_name, migrations, database, docker, orm, skip_install)

    def nav_to_dir(self, dir_name: Path) -> None:
        return super().nav_to_dir(dir_name)

    def create_poetry_project(self):
        self.project_path = Path(self.project_name)
        self.inner_project_path = self.project_path / self.project_name
        # innert project path is the path of the app folder created inside the root directory
        # project_path
        # |__inner_project_path
        # |__ ...

        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            transient=True,
        ) as progress:
            progress.add_task(description="Creating Poetry Project ...", total=1)
            os.system(f"poetry new {self.project_path} -q")
        console.print("[green bold]SUCCESS[/]: Create Poetry Project ...")
        self.init_env()
        self.create_files()

    def init_env(self):
        """
        we used `poetry env` command to create the venv without activating it
        which what happens if we use `poetry shell` which may run into some conflicts
        if you try to run the program when you already have an activated venv
        """
        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            transient=True,
        ) as progress:
            progress.add_task(description="Spawning Virtual Environment ...", total=1)
            os.system("poetry env use python -q")
            os.system(f"poetry add fastapi python-dotenv")
        console.print("[green bold]SUCCESS[/]: Spawn Virtual Environment ...")

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
