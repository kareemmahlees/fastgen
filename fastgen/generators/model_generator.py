import textwrap
from pathlib import Path

from ..constants import path_constants
from ..enums import generator_enums
from .base_generator import AbstractGenerator


class ModelGenerator(AbstractGenerator):
    """
    Generator for generating model components
    """

    def __init__(
        self,
        component: generator_enums.Components,
        path: Path | None,
        model_type: generator_enums.ModelType,
    ) -> None:
        super().__init__(component, path)
        self.model_type = model_type

    def generate_component(self, component_name: str):
        if self.model_type.value == "sqlalchemy":
            self.generate_sqlalchemy_model(component_name)

        if self.model_type.value == "sqlmodel":
            self.generate_sqlmodel_model(component_name)

    def generate_sqlalchemy_model(self, component_name: str):
        """
        generate sqlalchemy model

        Args:
            component_name (str) : name that will be applied to filename
            and model name
            must be in lowercase so the naming could resolve correctly
        """
        with open(
            Path.cwd() / path_constants.MODEL_FILE_PATH(component_name), "x"
        ) as f:
            f.write(
                textwrap.dedent(
                    f"""
            from sqlalchemy import Column, Integer
            from sqlalchemy.ext.declarative import declarative_base
            Base = declarative_base()

            class {component_name.capitalize()}(Base):
                __table_name__ = "{component_name.lower()}"

                id = Column(Integer,primary_key=True)
                # write your code here

                def __str__(self) -> str:
                # write your code here
                    ...
                                    """
                )
            )
        ...

    def generate_sqlmodel_model(self, component_name: str):
        """
        generate sqlmodel model

        Args:
            component_name (str) : name that will be applied to filename
            and model name
            must be in lowercase so the naming could resolve correctly
        """
        with open(
            Path.cwd() / path_constants.MODEL_FILE_PATH(component_name), "x"
        ) as f:
            f.write(
                textwrap.dedent(
                    f"""
        from sqlmodel import SQLModel,Field,create_engine
        from typing import Optional

        class {component_name.capitalize()}(SQLModel,table=True):
            id : Optional[int] = Field(primary_key=True,default=None)

        def create_tables():
            #                       change this
            engine = create_engine("DATABASE_URL")
            SQLModel.metadata.create_all(engine)

        if __name__ == "__main__":
            create_tables()
                                    """
                )
            )
