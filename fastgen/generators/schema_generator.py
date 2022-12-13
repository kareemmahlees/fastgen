import textwrap
from pathlib import Path

from ..constants import path_constants
from ..enums import generator_enums
from .base_generator import AbstractGenerator


class SchemaGenerator(AbstractGenerator):
    """
    Generator for generating schema components
    """

    def __init__(
        self, component: generator_enums.Components, path: Path | None
    ) -> None:
        super().__init__(component, path)

    def generate_component(self, component_name: str):
        """
        generate schema component

        Args:
            component_name (str) : name that will be applied to filename
            and schema classes
            must be in lowercase so the nameing could resolve correctly
        """
        with open(
            Path.cwd() / path_constants.SCHEMA_FILE_PATH(component_name), "x"
        ) as f:
            f.write(
                textwrap.dedent(
                    f"""
                    from pydantic import BaseModel

                    class {component_name.capitalize()}In(BaseModel):
                        ...

                    class {component_name.capitalize()}Out(BaseModel):
                        ...
                                    """
                )
            )
