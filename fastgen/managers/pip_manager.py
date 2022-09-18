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
        """
        executed when user defines a `--dir` value
        ### Raises:
            FileNotFoundError: if directory doesn't exist or invalid name
        """
        dir_path = Path(dir_name)
        if not dir_path.exists():
            raise FileNotFoundError(
                f"Folder {dir_path.name} doesn't exist , please provide a valid folder name"
            )
        os.chdir(dir_path)

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
        """
        generates main files for the project (main, deps, utils and schemas.py)
        """
        with open(api_path / "__init__.py", "x") as f:
            ...
        with open(api_path / "main.py", "x") as f:
            f.write(textwrap.dedent(constants.MAIN_APP(project_name=self.project_name)))

        with open(api_path / "deps.py", "x") as f:
            ...
        with open(api_path / "utils.py", "x") as f:
            ...
        with open(api_path / "schemas.py", "x") as f:
            f.write(
                textwrap.dedent(
                    """
                from pydantic import BaseModel
                """
                )
            )

    def generate_db_related_files(self, database_path: Path):
        """
        creates database.py file + db.sqlite file when `--database` is set to sqlite3
        """
        with open(database_path / "__init__.py", "x") as f:
            ...
        with open(database_path / "database.py", "x") as f:
            ...
        # * will be added when orms are supported
        # with open(databse_path / "models.py", "x") as f:
        #     ...
        if self.database.value == "sqlite3":
            with open(database_path / "db.sqlite", "x") as f:
                ...

    def generate_settings_related_files(self, settings_path: Path):
        """
        creates the config.py file with a class `Settings` to store environment variables
        """
        with open(settings_path / "__init__.py", "x",encoding="utf-8") as f:
            ...
        with open(settings_path / "config.py", "x",encoding="utf-8") as f:
            settings = constants.SETTINGS
            if self.database.value == "postgresql":
                settings += constants.POSTGRES_SETTINGS
            elif self.database.value == "mysql":
                settings += constants.MYSQL_SETTINGS
            f.write(constants.PYDANTIC_MAIN_SETTINGS(settings))

    def generate_env_file(self, project_path: Path):
        """
        generate env file which contains all environment variables
        """
        jwt_env_variables = constants.JWT_ENV_VARIABLES
        if self.database.value == "postgresql":
            jwt_env_variables += constants.POSTGRES_ENV_VARIABLES
        elif self.database.value == "mysql":
            jwt_env_variables += constants.MYSQL_ENV_VARIABLES
        with open(project_path / ".env", "x",encoding="utf-8") as f:
            f.write(textwrap.dedent(jwt_env_variables))

    def generate_test_files(self, testing_path: Path):
        "generate testing files"
        with open(testing_path / "__init__.py", "x",encoding="utf-8") as f:
            ...
        with open(testing_path / "test_main.py", "x",encoding="utf-8") as f:
            f.write(textwrap.dedent(constants.TESTING))

    def generate_docker_file(self, project_path: Path):
        """
        generate Dockerfile and docker-compose file with respect to the database of choice  
        """
        with open(project_path / "Dockerfile", "x",encoding="utf-8") as f:
            f.write(textwrap.dedent(constants.DOCKERFILE))
        if self.database.value != "sqlite3":
            with open(project_path/"docker-compose.yml","x",encoding="utf-8") as f:
                if self.database.value == "postgresql":
                    docker_compose_base = constants.DOCKER_COMPOSE_BASE("postgres")
                    docker_compose_base += constants.POSTGRES_DOCKER_COMPOSE
                    f.write(textwrap.dedent(docker_compose_base))

                elif self.database.value == "mysql":
                    docker_compose_base = constants.DOCKER_COMPOSE_BASE("mysql")
                    docker_compose_base += constants.MYSQL_DOCKER_COMPOSE
                    f.write(textwrap.dedent(docker_compose_base))


