from abc import ABC, abstractmethod
from pathlib import Path
import os
import textwrap
from .. import constants


class Manager(ABC):
    @abstractmethod
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
            with open(database_path / "models.py", "x") as f:
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
            settings = constants.SETTINGS
            if self.database.value == "postgresql":
                settings += constants.POSTGRES_SETTINGS
            elif self.database.value == "mysql":
                settings += constants.MYSQL_SETTINGS
            f.write(constants.PYDANTIC_MAIN_SETTINGS(settings))

    @abstractmethod
    def generate_env_file(self, project_path: Path):
        """
        generate env file which contains all environment variables
        """
        jwt_env_variables = constants.JWT_ENV_VARIABLES
        if self.database.value == "postgresql":
            jwt_env_variables += constants.POSTGRES_ENV_VARIABLES
        elif self.database.value == "mysql":
            jwt_env_variables += constants.MYSQL_ENV_VARIABLES
        with open(project_path / ".env", "x", encoding="utf-8") as f:
            f.write(textwrap.dedent(jwt_env_variables))

    @abstractmethod
    def generate_docker_file(self, project_path: Path):
        """
        generate Dockerfile and docker-compose file with respect to the database of choice
        """
        with open(project_path / "Dockerfile", "x", encoding="utf-8") as f:
            f.write(textwrap.dedent(constants.DOCKERFILE))
        if self.database.value != "sqlite3":
            with open(project_path / "docker-compose.yml", "x", encoding="utf-8") as f:
                if self.database.value == "postgresql":
                    docker_compose_base = constants.DOCKER_COMPOSE_BASE("postgres")
                    docker_compose_base += constants.POSTGRES_DOCKER_COMPOSE
                    f.write(textwrap.dedent(docker_compose_base))

                elif self.database.value == "mysql":
                    docker_compose_base = constants.DOCKER_COMPOSE_BASE("mysql")
                    docker_compose_base += constants.MYSQL_DOCKER_COMPOSE
                    f.write(textwrap.dedent(docker_compose_base))
