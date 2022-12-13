from pathlib import Path

import typer

from ..enums.generator_enums import Components
from ..enums.generator_enums import ModelType
from ..generators import model_generator
from ..generators import router_generator
from ..generators import schema_generator

generator_app = typer.Typer(
    help="Generate new component", pretty_exceptions_show_locals=False
)


@generator_app.command(
    help="Generate new router",
)
def router(
    name: str = typer.Argument(help="name of the router", default=...),
    path: Path = typer.Option(
        default=None, help="relative to current working directory"
    ),
):
    router_gen = router_generator.RouterGenerator(Components.router, path)
    router_gen.generate_component(name)


@generator_app.command(help="Generate new schema")
def schema(
    name: str = typer.Argument(help="name of the schema", default=...),
    path: Path = typer.Option(
        default=None, help="relative to current working directory"
    ),
):
    schema_gen = schema_generator.SchemaGenerator(Components.schema, path)
    schema_gen.generate_component(name)


@generator_app.command(help="Generate new model")
def model(
    name: str = typer.Argument(help="name of the mode", default=...),
    path: Path = typer.Option(
        default=None, help="relative to the current working directory"
    ),
    model_type: ModelType = typer.Option(default=ModelType.sqlalchemy),
):
    model_gen = model_generator.ModelGenerator(Components.model, path, model_type)
    model_gen.generate_component(name)
