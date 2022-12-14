from abc import ABC
from abc import abstractmethod
from pathlib import Path
from typing import Optional

from ..constants import path_constants
from ..enums.generator_enums import Components
from ..exceptions.generator_exceptions import FolderNotFoundError
from ..exceptions.generator_exceptions import PathNotFoundError


class AbstractGenerator(ABC):
    """
    A base generator for all generator classes
    """

    def __init__(self, component: Components, path: Optional[Path]) -> None:
        self.path = path
        if not path:
            self._check_builtin_path_exists(component)
        else:
            if not (Path.cwd() / path).exists():
                raise PathNotFoundError(
                    f"Path {path} does not exist, pleace make sure the provided path is relative to the current working directory"
                )

    def _check_builtin_path_exists(self, component: Components):
        """
        if `--path` was not provided , this will check if the built in path exists or not

        Args:
            component (Components): type of the component , used to fetch the corresponding
            path from built in path constants

        Raises:
            FolderNotFoundError: if the built in folder doesn't exist
        """
        default_path: Path = Path.cwd() / path_constants.__dict__.get(component.value)  # type: ignore
        if not default_path.exists():
            raise FolderNotFoundError(
                f"Folder {component.name}s was not found at path {default_path.absolute()}"
            )

    @abstractmethod
    def generate_component(self, component_name: str):
        ...
