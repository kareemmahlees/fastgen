import textwrap
from pathlib import Path
from typing import Optional

from ..constants import path_constants
from ..enums import generator_enums
from .base_generator import AbstractGenerator


class RouterGenerator(AbstractGenerator):
    """
    Generator class for generating router components
    """

    def __init__(
        self, component: generator_enums.Components, path: Optional[Path]
    ) -> None:
        super().__init__(component, path)

    def generate_component(self, component_name: str):
        """
        generate router component

        Args:
            component_name (str) : name that will be applied to filename
            router_prefix and tags
            must be in lowercase so the naming could resolve correctly

        """
        with open(
            Path.cwd() / path_constants.ROUTER_FILE_PATH(component_name)
            if not self.path
            else self.path,
            "x",
        ) as f:
            f.write(
                textwrap.dedent(
                    f"""
            from fastapi import APIRouter

            router = APIRouter(prefix="/{component_name.lower()}",tags=["{component_name.capitalize()}"])
                                    """
                )
            )
