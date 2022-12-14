import os
import textwrap
from abc import ABC
from abc import abstractmethod
from pathlib import Path

from ..blocks import docker_blocks
from ..blocks import env_blocks
from ..blocks import main_blocks
from ..blocks import pydantic_blocks
from ..enums.manager_enums import Database


class AbstractManager(ABC):
    def __init__(
        self,
        project_name: str,
        migrations: bool,
        database: Database,
        docker: bool,
        orm: bool,
        skip_install: bool,
    ) -> None:
        self.project_name = project_name
        self.migrations = migrations
        self.database = database
        self.docker = docker
        self.orm = orm
        self.skip_install = skip_install

    @abstractmethod
    def nav_to_dir(self, dir_name: Path) -> None:
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

    @abstractmethod
    def init_env(self):
        ...

    @abstractmethod
    def generate_main_files(self, api_path: Path):
        """
        generates main files for the project (main, deps, utils and schemas.py)
        """
        with open(api_path / "__init__.py", "x") as f:
            ...
        with open(api_path / "main.py", "x") as f:
            f.write(
                textwrap.dedent(main_blocks.MAIN_APP(project_name=self.project_name))
            )

        with open(api_path / "deps.py", "x") as f:
            ...

        os.mkdir(api_path / "utils")
        with open(api_path / "utils" / "__init__.py", "x") as f:
            ...

        os.mkdir(api_path / "schemas")
        with open(api_path / "schemas" / "__init__.py", "x") as f:
            ...

        os.mkdir(api_path / "routers")
        with open(api_path / "routers" / "__init__.py", "x") as f:
            ...

    @abstractmethod
    def generate_db_related_files(self, database_path: Path, orm: bool):
        """
        creates database.py file + db.sqlite file when `--database` is set to sqlite3
        """
        with open(database_path / "__init__.py", "x") as f:
            ...
        with open(database_path / "database.py", "x") as f:
            ...
        if orm:
            os.mkdir(database_path / "models.py")
            with open(database_path / "models.py" / "__init__.py", "x") as f:
                ...
        if self.database.value == "sqlite3":
            with open(database_path / "db.sqlite", "x") as f:
                ...

    @abstractmethod
    def generate_settings_related_files(self, settings_path: Path):
        """
        creates the config.py file with a class `Settings` to store environment variables
        """
        with open(settings_path / "__init__.py", "x", encoding="utf-8") as f:
            ...
        with open(settings_path / "config.py", "x", encoding="utf-8") as f:
            settings = pydantic_blocks.JWT_SETTINGS
            if self.database.value == "postgresql":
                settings += pydantic_blocks.POSTGRES_SETTINGS
            elif self.database.value == "mysql":
                settings += pydantic_blocks.MYSQL_SETTINGS
            f.write(pydantic_blocks.PYDANTIC_MAIN_SETTINGS(settings))

    @abstractmethod
    def generate_env_file(self, project_path: Path):
        """
        generate env file which contains all environment variables
        """
        jwt_env_variables = env_blocks.JWT_ENV_VARIABLES
        if self.database.value == "postgresql":
            jwt_env_variables += env_blocks.POSTGRES_ENV_VARIABLES
        elif self.database.value == "mysql":
            jwt_env_variables += env_blocks.MYSQL_ENV_VARIABLES
        with open(project_path / ".env", "x", encoding="utf-8") as f:
            f.write(textwrap.dedent(jwt_env_variables))

    @abstractmethod
    def generate_docker_file(self, project_path: Path):
        """
        generate Dockerfile and docker-compose file with respect to the database of choice
        """
        with open(project_path / "Dockerfile", "x", encoding="utf-8") as f:
            f.write(textwrap.dedent(docker_blocks.DOCKERFILE))
        if self.database.value != "sqlite3":
            with open(project_path / "docker-compose.yml", "x", encoding="utf-8") as f:
                if self.database.value == "postgresql":
                    docker_compose_base = docker_blocks.DOCKER_COMPOSE_BASE("postgres")
                    docker_compose_base += docker_blocks.POSTGRES_DOCKER_COMPOSE
                    f.write(textwrap.dedent(docker_compose_base))

                elif self.database.value == "mysql":
                    docker_compose_base = docker_blocks.DOCKER_COMPOSE_BASE("mysql")
                    docker_compose_base += docker_blocks.MYSQL_DOCKER_COMPOSE
                    f.write(textwrap.dedent(docker_compose_base))
