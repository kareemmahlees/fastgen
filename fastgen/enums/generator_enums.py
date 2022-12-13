from enum import Enum


class Components(Enum):
    router = "ROUTERS_DIR"
    schema = "SCHEMAS_DIR"
    model = "MODELS_DIR"


class ModelType(Enum):
    sqlalchemy = "sqlalchemy"
    sqlmodel = "sqlmodel"
